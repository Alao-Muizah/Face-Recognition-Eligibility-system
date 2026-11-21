import sqlite3 

connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()

def mark_sign_in_attendance(session_id, student_id):

    cursor.execute("""
        INSERT OR IGNORE INTO Attendance
        (session_id, student_id)
        VALUES (?, ?)
    """, (session_id, student_id))

    connection.commit()
    
    # To ensure that the sign in is recorded only once for each student in a session
    if cursor.rowcount == 1:
        print(f"Sign-in recorded for {student_id}")
        return True

    print(f"Sign-in already recorded for {student_id}")
    return False


def mark_sign_out_attendance(session_id, student_id):

    cursor.execute("""
        UPDATE Attendance
        SET sign_out_time = CURRENT_TIMESTAMP
        WHERE session_id = ?
        AND student_id = ?
        AND sign_out_time IS NULL
    """, (session_id, student_id))

    connection.commit()

    if cursor.rowcount == 1:
        print(f"Sign-out recorded for {student_id}")
        return True

    print(f"No outstanding sign-in record found for {student_id}")
    return False



