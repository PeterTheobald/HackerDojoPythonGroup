# Discussion Board REST API Specification

## Base URL
`https://api.discussionboard.com/v1`

## Authentication
- Uses JWT (JSON Web Tokens) for authentication
- Token must be included in Authorization header: `Authorization: Bearer <token>`

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
```
Request body:
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```
Response (201 Created):
```json
{
    "id": "uuid",
    "username": "string",
    "email": "string",
    "created_at": "timestamp"
}
```

#### Login
```
POST /auth/login
```
Request body:
```json
{
    "email": "string",
    "password": "string"
}
```
Response (200 OK):
```json
{
    "token": "string",
    "user": {
        "id": "uuid",
        "username": "string",
        "email": "string"
    }
}
```

#### Logout
```
POST /auth/logout
```
Response (204 No Content)

### Topics

#### List Topics
```
GET /topics
```
Query parameters:
- page (integer, default: 1)
- limit (integer, default: 20)
- sort (string, enum: ["newest", "most_active"], default: "newest")

Response (200 OK):
```json
{
    "topics": [
        {
            "id": "uuid",
            "title": "string",
            "description": "string",
            "created_by": {
                "id": "uuid",
                "username": "string"
            },
            "created_at": "timestamp",
            "comment_count": "integer",
            "last_activity": "timestamp"
        }
    ],
    "pagination": {
        "total": "integer",
        "page": "integer",
        "limit": "integer",
        "total_pages": "integer"
    }
}
```

#### Create Topic
```
POST /topics
```
Request body:
```json
{
    "title": "string",
    "description": "string"
}
```
Response (201 Created):
```json
{
    "id": "uuid",
    "title": "string",
    "description": "string",
    "created_by": {
        "id": "uuid",
        "username": "string"
    },
    "created_at": "timestamp"
}
```

#### Get Topic Details
```
GET /topics/{topic_id}
```
Response (200 OK):
```json
{
    "id": "uuid",
    "title": "string",
    "description": "string",
    "created_by": {
        "id": "uuid",
        "username": "string"
    },
    "created_at": "timestamp",
    "comment_count": "integer",
    "last_activity": "timestamp"
}
```

### Comments

#### List Comments for Topic
```
GET /topics/{topic_id}/comments
```
Query parameters:
- page (integer, default: 1)
- limit (integer, default: 50)
- sort (string, enum: ["newest", "oldest"], default: "newest")

Response (200 OK):
```json
{
    "comments": [
        {
            "id": "uuid",
            "content": "string",
            "created_by": {
                "id": "uuid",
                "username": "string"
            },
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    ],
    "pagination": {
        "total": "integer",
        "page": "integer",
        "limit": "integer",
        "total_pages": "integer"
    }
}
```

#### Create Comment
```
POST /topics/{topic_id}/comments
```
Request body:
```json
{
    "content": "string"
}
```
Response (201 Created):
```json
{
    "id": "uuid",
    "content": "string",
    "created_by": {
        "id": "uuid",
        "username": "string"
    },
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

## Error Responses

All error responses follow this format:
```json
{
    "error": {
        "code": "string",
        "message": "string"
    }
}
```

Common HTTP status codes:
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Server error

## Rate Limiting
- API is rate limited to 100 requests per minute per user
- Rate limit headers included in all responses:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

