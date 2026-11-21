import sqlite3

connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()


def get_eligible_students(course_code):

    cursor.execute("""
        SELECT
            Eligible_Students.student_id,
            Eligible_Students.full_name,
            Eligible_Students.matric_number,
            Eligible_Students.department,
            Course_Eligibility.course_code

        FROM Eligible_Students

        JOIN Course_Eligibility
        ON Eligible_Students.student_id =
           Course_Eligibility.student_id

        WHERE Course_Eligibility.course_code = ?
    """, (course_code,))

    eligible_students = cursor.fetchall()

    return eligible_students


def is_eligible(student_id, course_code):

    cursor.execute("""
        SELECT student_id
        FROM Course_Eligibility
        WHERE student_id = ?
        AND course_code = ?
    """, (student_id, course_code))

    result = cursor.fetchone()

    return result is not None


