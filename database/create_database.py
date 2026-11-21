import sqlite3

connection = sqlite3.connect('database\\exam_database.db')
cursor = connection.cursor()

# To Enable foreign key relationships 
connection.execute("PRAGMA foreign_keys = ON")
# Eligibled students 
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Eligible_Students(
                   student_id TEXT PRIMARY KEY,
                   full_name TEXT NOT NULL, 
                   matric_number TEXT UNIQUE NOT NULL, 
                   department TEXT NOT NULL,
                   face_image_path TEXT)""")

# Course eligibilty table 
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Course_Eligibility(
               student_id TEXT NOT NULL,
               course_code TEXT NOT NULL, 
               PRIMARY KEY (student_id, course_code),
               FOREIGN KEY (student_id) REFERENCES Eligible_Students(student_id))""")

# Exam sessions 

cursor.execute("""
               CREATE TABLE IF NOT EXISTS Exam_Sessions (
                   session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   course_code TEXT NOT NULL,
                   exam_date DATE NOT NULL,
                   start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                   end_time DATETIME)""")

# Attendance 
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Attendance (
               attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
               session_id INTEGER NOT NULL,
               student_id TEXT NOT NULL, 
               sign_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
               sign_out_time DATETIME,
               
               UNIQUE(session_id, student_id),
               
               FOREIGN KEY (session_id)
               REFERENCES Exam_Sessions(session_id),
               
               FOREIGN KEY (student_id)
               REFERENCES Eligible_Students(student_id))""")



connection.commit()
connection.close()

print("Database and tables created succesfully")


