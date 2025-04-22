from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///my_database.db')

with engine.connect() as con:

  result = con.execute(text("select * from students"))
  print(result.all())

###########
print()
print()

with engine.connect() as con:

  con.execute(
    text("insert into students (name, grade) values (:name, :grade)"),
    [{
      'name': 'Zenia',
      'grade': 99
    }, {
      'name': 'Yannis',
      'grade': 14
    }])
  con.commit()

  result = con.execute(text("select * from students"))

for row in result:
  print(row)

####
print()
print()

with engine.connect() as con:
  result = con.execute(
    text(
      "delete from students where name = 'Zenia' or name = 'Yannis' or name = 'Winona'"
    ))
  con.commit()

with engine.connect() as con:
  result = con.execute(text("select * from students"))
  for row in result:
    print(row)

####

with engine.begin() as con:
  con.execute(
    text("insert into students (name, grade) values (:name, :grade)"),
    [{
      'name': 'Xerxes',
      'grade': 300
    }])

with engine.connect() as con:
  result = con.execute(text("select * from students"))
  for row in result:
    print(f"name: {row.name}  grade: {row.grade}")

    ####

    from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
    from sqlalchemy.sql import select, insert
    from sqlalchemy.orm import Session

    # Create an engine (assume a valid URL)
    engine = create_engine(
      'sqlite:///:memory:')  # Example for SQLite in-memory DB

    # Initialize MetaData instance
    metadata = MetaData()

    # Define the structure of the table
    students_table = Table('students', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String), Column('grade', Integer))

    # Create the table in the database
    metadata.create_all(engine)

    with engine.connect() as con:
      # Insert a record into the table
      insert_query = insert(students_table).values(name="Winona", grade=76)
      con.execute(insert_query)

      # Select records from the table
      select_query = select(students_table)
      result = con.execute(select_query)
      for row in result:
        print(row)
