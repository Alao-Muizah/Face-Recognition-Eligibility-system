import sqlite3
from datetime import date

from src.compare import (
    compare_face,
    eligible_sound,
    not_eligible_sound
)

from src.check_eligibility import (
    get_eligible_students,
    is_eligible
)

from src.record_attendance import (
    mark_sign_in_attendance,
    mark_sign_out_attendance
)


# Connecting to the examination database
connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()


def create_exam_session(course_code, exam_date):

    cursor.execute("""
        INSERT INTO Exam_Sessions (course_code, exam_date)
        VALUES (?, ?)
    """, (course_code, exam_date))

    connection.commit()

    session_id = cursor.lastrowid

    print("\nExamination session created successfully.")

    return session_id


def end_exam_session(session_id):

    cursor.execute("""
        UPDATE Exam_Sessions
        SET end_time = CURRENT_TIMESTAMP
        WHERE session_id = ?
        AND end_time IS NULL
    """, (session_id,))

    connection.commit()

    print("\nExamination session ended.")


def main():

    print("===== EXAMINATION VERIFICATION SYSTEM =====")

    # 1. Get course code
    course_code = input("\nEnter course code: ").strip().upper()

    # 2. Get examination date
    exam_date = date.today().strftime("%Y-%m-%d")

    # 3. Check whether the course has eligible students
    eligible_students = get_eligible_students(course_code)

    if not eligible_students:
        print("No eligible students found for this course.")
        return

    print(f"\nEligible students for {course_code}:")

    for student in eligible_students:
        print(f"{student[0]} - {student[1]}")

    # 4. Create examination session
    session_id = create_exam_session(course_code, exam_date)

    # 5. Begin examination verification
    while True:

        print("\n===== EXAMINATION MENU =====")
        print("1. Sign In")
        print("2. Sign Out")
        print("3. End Examination Session")

        choice = input("\nSelect an option: ").strip()

        if choice == "3":
            end_exam_session(session_id)
            break

        elif choice not in ("1", "2"):
            print("Invalid option.")
            continue

        if choice == "1":
            action = "Sign In"
        else:
            action = "Sign Out"

        print(f"\nSelected action: {action}")
        print("Position your face in front of the camera.")
        print("Press Q when you want to finish scanning.")

        # 6. Compare the captured face
        student_id, confidence = compare_face()

        if student_id is None:
            print("No face was detected.")
            continue

        if student_id == "Unknown":
            print("Face could not be confidently recognised.")
            continue

        print(f"\nRecognised Student: {student_id}")
        print(f"Confidence distance: {confidence:.2f}")

        # 7. Check course eligibility
        if not is_eligible(student_id, course_code):

            print(f"Student {student_id} is not eligible for {course_code}.")
            not_eligible_sound()
            continue

        print(f"Student {student_id} is eligible for {course_code}.")

        # 8. Record the selected action
        if choice == "1":

            recorded = mark_sign_in_attendance(
                session_id,
                student_id
            )

        else:

            recorded = mark_sign_out_attendance(
                session_id,
                student_id
            )

        # 9. Give feedback
        if recorded:
            eligible_sound()


    connection.close()
    print("\nSystem closed.")


if __name__ == "__main__":
    main()

