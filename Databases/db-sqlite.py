import sqlite3

ng.config.autoreload = False

def main():
  # Connect to SQLite database
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()

  # Create a table
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        grade INTEGER
    );
    ''')

  # Insert data THE BAD DANGEROUS WAY
  cursor.execute('''
        INSERT INTO students (name, grade) VALUES('Bobby Tables', 64)
    ''')
  # Insert data the SAFE WAY with placeholders
  cursor.execute(
    '''
      INSERT INTO students (name, grade) VALUES(?, ?)
  ''', ('Bobby Tables', 64))

  # Insert data
  students_data = [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
  cursor.executemany("INSERT INTO students (name, grade) VALUES (?, ?);",
                     students_data)
  conn.commit()

  # Query data
  cursor.execute("SELECT * FROM students;")
  rows = cursor.fetchall()
  print("Students Data:")
  for row in rows:
    print(row)

  # Update data
  cursor.execute("UPDATE students SET grade = 91 WHERE name = 'Bob';")
  conn.commit()

  # Delete data
  cursor.execute("DELETE FROM students WHERE name = 'Charlie';")
  conn.commit()

  # Query data after updates
  cursor.execute("SELECT * FROM students;")
  rows = cursor.fetchall()
  print("\nStudents Data after updates:")
  for row in rows:
    print(row)

  # Close the cursor and connection
  cursor.close()
  conn.close()


def with_example():
  with sqlite3.connect('mydb.db') as conn:
    pass
    # do stuff

  with open('file', 'r') as f:
    pass
    # do stuff with f


if __name__ == "__main__":
  main()
