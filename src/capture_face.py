
import cv2 as cv
import os
import sqlite3
import time

connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()

# Getting student ID
student_id = input("Enter student ID: ")

# Folder to save captured faces
folder = f"dataset/{student_id}"
os.makedirs(folder, exist_ok=True)

# Loading webcam
camera = cv.VideoCapture(0)

# Loading face detection model
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

TARGET_IMAGES = 25

print("Position your face in front of the camera")
print("Press 'S' once to capture 25 images")
print("Press 'Q' to quit")


while True:

    success, frame = camera.read()

    if not success:
        print("Could not access webcam")
        break

    # Convert frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    # To Draw rectangle around the detected face
    for x, y, w, h in faces:

        cv.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv.imshow("Face Recognition", frame)

    key = cv.waitKey(1) & 0xFF

    if key == ord('s'):

        if len(faces) != 1:
            print("Please ensure exactly one face is visible.")
            continue

        print("\nStarting automatic face capture...")

        saved_images = 0

        while saved_images < TARGET_IMAGES:

            success, frame = camera.read()

            if not success:
                print("Could not capture frame.")
                break

            gray_frame = cv.cvtColor(
                frame,
                cv.COLOR_BGR2GRAY
            )

            faces = face_cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            # Capture only when exactly one face is detected
            if len(faces) == 1:

                x, y, w, h = faces[0]

                face = gray_frame[y:y+h, x:x+w]

                saved_images += 1

                image_path = os.path.join(
                    folder,
                    f"face_{saved_images}.jpg"
                )

                cv.imwrite(image_path, face)

                print(
                    f"Captured image {saved_images}/{TARGET_IMAGES}"
                )

                # Short interval between captures
                time.sleep(0.4)

            else:
                print("Face not detected clearly. Adjust your position.")

        if saved_images > 0:

            # Update student database
            cursor.execute("""
                UPDATE Eligible_Students
                SET face_image_path = ?
                WHERE student_id = ?
            """, (folder, student_id))

            connection.commit()

            if cursor.rowcount == 1:
                print("\nStudent face registration successful!")
                print(f"Total images captured: {saved_images}")

            else:
                print("Student ID not found in database.")

        if saved_images < TARGET_IMAGES:
            print("Capture incomplete. You can press S to try again.")

    elif key == ord('q'):

        print("Closing camera...")
        break


camera.release()
cv.destroyAllWindows()

cursor.close()
connection.close()
