from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            student_class TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Home route to list all students
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add new student
@app.route('/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        student_class = request.form['class']

        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, age, student_class) VALUES (?, ?, ?)',
                     (name, age, student_class))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit student
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        student_class = request.form['class']

        conn.execute('UPDATE students SET name = ?, age = ?, student_class = ? WHERE id = ?',
                     (name, age, student_class, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students WHERE name LIKE ? OR student_class LIKE ?', 
                            ('%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/students')
def view_students():
    conn = get_db_connection()  # Establish a connection with your SQLite database
    students = conn.execute('SELECT * FROM students').fetchall()  # Fetch all students from the table
    conn.close()  # Close the connection to the database
    return render_template('students.html', students=students)  # Pass the data to the HTML template

if __name__ == '__main__':
    app.run(debug=True)
