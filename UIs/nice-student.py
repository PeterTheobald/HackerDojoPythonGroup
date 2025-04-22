import sqlite3
from nicegui import ui


# Initialize or create the database and table
def initialize_db():
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
  conn.commit()
  conn.close()


# Function to get data from the database
def get_students():
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM students')
  rows = cursor.fetchall()
  conn.close()
  return rows


# Function to insert a new student
def add_student():
  name = name_input.value
  grade = grade_input.value

  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  cursor.execute('INSERT INTO students (name, grade) VALUES (?, ?)',
                 (name, grade))
  conn.commit()
  conn.close()
  ui.notify('Student added successfully')
  ui.reload()


# Function to update a student
def update_student(id, name, grade):
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  cursor.execute('UPDATE students SET name=?, grade=? WHERE id=?',
                 (name, grade, id))
  conn.commit()
  conn.close()
  ui.notify('Student updated successfully')
  ui.reload()


# Function to delete a student
def delete_student(id):
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  cursor.execute('DELETE FROM students WHERE id=?', (id, ))
  conn.commit()
  conn.close()
  ui.notify('Student deleted successfully')
  ui.reload()


@ui.page('/')
def page():

  # Create inputs for new student details
  name_input = ui.input(label='Name')
  grade_input = ui.input(label='Grade')
  ui.button('Add Student', on_click=add_student)

  # Display the table of students
  mytable = ui.table(get_students(), ['ID', 'Name', 'Grade'])
  mytable.on('edit', update_student)
  mytable.on('delete', delete_student)


def main():
  # Setup the database
  initialize_db()
  # Start the UI
  ui.run()


main()
