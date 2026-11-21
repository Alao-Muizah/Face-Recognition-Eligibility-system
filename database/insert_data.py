import sqlite3 

connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()

# Student records <= Mock data for testing purposes
students = [
    ("STU001", "Alao Muizah", "FUO/23/0032", "Computer Science", None),
    ("STU002", "Ruqsar karrem", "FUO/23/0456", "Computer Science", None),
    ("STU003", "Zakariyah Rosheedah", "FUO/23/0252", "Public health", None),
    ("STU004", "Zara Sidiqui", "FUO/23/0121", "MLS", None),
    ("STU005", "Khabeer Ahmad", "FUO/22/0235", "Nursing", None)
]

# Insert students 
cursor.executemany("""
                   INSERT INTO Eligible_Students
                   (student_id, full_name, matric_number, department, face_image_path) VALUES (?, ?, ?, ?, ?)""",
                   students)


# course eligibilty records 
eligibility = [
    ("STU001", "CSC401"),
    ("STU001", "CSC417"),
    ("STU001", "CSC407"),
    
    ("STU002", "CSC401"),
    ("STU002", "CSC417"),
    
    ("STU003", "CSC413"),
    ("STU003", "CPS415"),
    
    ("STU004", "CSC401"),
    ("STU004", "CSC417"),
    ("STU004", "CSC407"),
    
    ("STU005", "CSC413"),
    ("STU005", "CPS415") 
    
]

# Inserting eligibility records 
cursor.executemany("""
                   INSERT INTO Course_Eligibility
                   (student_id, course_code) VALUES (?, ?)""",
                   eligibility)

connection.commit()
connection.close()

print("Students records inserted successfully")


  