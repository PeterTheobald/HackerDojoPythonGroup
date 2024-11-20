from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

# Configuration
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup - using SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'discussion_board.db')}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Custom UUID type for SQLite
class SqliteUUID(type(String())):
    cache_ok = True
    
    def __init__(self):
        super().__init__(length=36)
        
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value)
        
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(value)

# Database Models
class DBUser(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    topics = relationship("DBTopic", back_populates="created_by")
    comments = relationship("DBComment", back_populates="created_by")

class DBTopic(Base):
    __tablename__ = "topics"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200))
    description = Column(Text)
    created_by_id = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = relationship("DBUser", back_populates="topics")
    comments = relationship("DBComment", back_populates="topic")

class DBComment(Base):
    __tablename__ = "comments"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text)
    topic_id = Column(String(36), ForeignKey("topics.id"))
    created_by_id = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    topic = relationship("DBTopic", back_populates="comments")
    created_by = relationship("DBUser", back_populates="comments")

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    user_id: str

class Token(BaseModel):
    token: str
    user: User

class TopicBase(BaseModel):
    title: str
    description: str

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: uuid.UUID
    created_by: User
    created_at: datetime
    comment_count: int = 0

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: uuid.UUID
    created_by: User
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int

class TopicList(PaginatedResponse):
    topics: List[Topic]

class CommentList(PaginatedResponse):
    comments: List[Comment]

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# FastAPI app
app = FastAPI(title="Hacker Dojo Python Discussion Board API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your front-end's domain for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow specific methods or "*" for all
    allow_headers=["*"],  # Allow specific headers or "*" for all
)

# Auth endpoints
@app.post("/auth/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(DBUser).filter(DBUser.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(DBUser).filter(DBUser.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f'/auth/register: {db_user}')
    return db_user

@app.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print('IN AUTH/LOGIN')
    user = db.query(DBUser).filter(DBUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        print(f'/auth/login: failed')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(data={"user_id": user.id})
    print(f'/auth/login: success token={token}, user={user}')
    return {"token": token, "user": user}

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    return None

# Topic endpoints
@app.get("/topics", response_model=TopicList)
async def list_topics(
    page: int = 1,
    limit: int = 20,
    sort: str = "newest",
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    total = db.query(DBTopic).count()
    
    query = db.query(DBTopic)
    if sort == "newest":
        query = query.order_by(DBTopic.created_at.desc())
    elif sort == "most_active":
        query = query.order_by(DBTopic.created_at.desc())
    
    topics = query.offset(offset).limit(limit).all()
    
    for topic in topics:
        topic.comment_count = db.query(DBComment).filter(DBComment.topic_id == topic.id).count()
    
    return {
        "topics": topics,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@app.post("/topics", response_model=Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic: TopicCreate,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_topic = DBTopic(**topic.dict(), created_by_id=current_user.id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    db_topic.comment_count = 0
    return db_topic

@app.get("/topics/{topic_id}", response_model=Topic)
async def get_topic(
    topic_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    topic = db.query(DBTopic).filter(DBTopic.id == str(topic_id)).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    topic.comment_count = db.query(DBComment).filter(DBComment.topic_id == str(topic_id)).count()
    return topic

# Comment endpoints
@app.get("/topics/{topic_id}/comments", response_model=CommentList)
async def list_comments(
    topic_id: uuid.UUID,
    page: int = 1,
    limit: int = 50,
    sort: str = "newest",
    db: Session = Depends(get_db)
):
    topic = db.query(DBTopic).filter(DBTopic.id == str(topic_id)).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    offset = (page - 1) * limit
    total = db.query(DBComment).filter(DBComment.topic_id == str(topic_id)).count()
    
    query = db.query(DBComment).filter(DBComment.topic_id == str(topic_id))
    if sort == "newest":
        query = query.order_by(DBComment.created_at.desc())
    elif sort == "oldest":
        query = query.order_by(DBComment.created_at.asc())
    
    comments = query.offset(offset).limit(limit).all()
    
    return {
        "comments": comments,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@app.post("/topics/{topic_id}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    topic_id: uuid.UUID,
    comment: CommentCreate,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    topic = db.query(DBTopic).filter(DBTopic.id == str(topic_id)).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db_comment = DBComment(
        **comment.dict(),
        topic_id=str(topic_id),
        created_by_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Create tables
Base.metadata.create_all(bind=engine)

