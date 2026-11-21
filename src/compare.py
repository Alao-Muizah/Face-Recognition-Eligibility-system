import cv2 as cv 
import numpy as np 
import winsound 
from datetime import datetime
import sqlite3

connection = sqlite3.connect("database\\exam_database.db")
cursor = connection.cursor()


# winsound.Beep(Requency in Hertz, duration in milliseconds)
def eligible_sound():
  winsound.Beep(1000, 300) 

def not_eligible_sound():
    winsound.Beep(400, 700)
 
# Load trained LBPH model
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read("models/trainer.yml")

# Load student label mapping 
label_map = np.load("models/Label_map.npy", allow_pickle=True).item()

# load face detection classifier
face_detector = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")


def compare_face():
    
    # For opening the pcs' webcam
    camera = cv.VideoCapture(0)
    
    student_id = None
    confidence = None

    while True:
        # Captures a frame from the webcam
        successful, frame = camera.read()
        
        if not successful:
            print("Could not access webcam")
            break 
        
        # convert the frame to gray scale 
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # detect face in frame
        detected_faces = face_detector.detectMultiScale(
            gray, 
            scaleFactor = 1.1, 
            minNeighbors=5, 
            minSize=(100, 100)
        )
        
        # process each detected faces 
        for (x, y, w, h) in detected_faces:
            
            # extract the face from the frame and resize to match training image dimensions 
            face = gray[y:y + h, x: x +w]
            face = cv.resize(face, (255, 255))
            
            # comparing face with trained model 
            label, confidence = recognizer.predict(face)
            
            # Retrieve the corresponding student ID
            student_id = label_map.get(label, "Unknown")
            
            
            # Display the prediction
            text = f"{student_id} | Distance: {confidence:.2f}"

            cv.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv.putText(
                frame,
                text,
                (x, y-10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        # Display the webcam feed
        cv.imshow("Face Recognition", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # print(f"Predicted label: {label}")
    # print(f"Confidence distance: {confidence:.2f}")
    # print(f"Student id: {student_id}")

    # Release webcam resources
    camera.release()
    cv.destroyAllWindows()

    # Fetching students info 
    
    THRESHOLD = 50

    if confidence is None:
        return None, None

    if confidence < THRESHOLD:
        return student_id, confidence

    return "Unknown", confidence

    