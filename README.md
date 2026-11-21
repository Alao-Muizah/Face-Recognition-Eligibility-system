
# Face Recognition-Based Examination Verification System

A Python-based examination verification system that uses face recognition to identify students, verify their eligibility for a selected course, and record their examination sign-in and sign-out times.

## Overview

The system is designed to simplify student verification during examinations by combining facial recognition with a database-driven course eligibility system.

Instead of manually checking student identities against course eligibility lists, an examination officer selects a course, and students verify their identities through a webcam.

The system checks whether the recognised student is eligible for the selected course before recording their examination entry or exit.

## Features

- **Face Detection:** Detects faces using OpenCV's Haar Cascade Classifier.
- **Face Recognition:** Uses the Local Binary Patterns Histograms (LBPH) algorithm to recognise registered students.
- **Student Face Capture:** Captures and stores multiple face images for each student.
- **Model Training:** Trains an LBPH face recognition model using the collected face images.
- **Course Eligibility Verification:** Checks whether a recognised student is eligible to sit for a selected course.
- **Examination Session Management:** Creates examination sessions using the selected course and examination date.
- **Sign-In Recording:** Records the time a verified student enters an examination.
- **Sign-Out Recording:** Updates the student's existing attendance record with their departure time.
- **Database Management:** Stores student information, course eligibility, examination sessions and attendance records using SQLite.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Face detection and recognition |
| LBPH | Face recognition algorithm |
| NumPy | Numerical operations and label mapping |
| SQLite | Database management |
| Haar Cascade | Face detection |
| Winsound | Audio feedback on Windows |

## System Architecture

The project is organised into separate modules, each responsible for a specific task.

```text
Face_Recognition/
│
├── database/
│   └── create_database.py
│   └── insert_data.py
│   └── exam_database.db
│
├── dataset/
│   └── Student face images
│
├── models/
│   ├── trainer.yml
│   └── Label_map.npy
│
├── src/
│   ├── capture_faces.py
│   ├── train_model.py
│   ├── compare.py
│   ├── check_eligibility.py
│   └── record_attendance.py
│
├── main.py
├── README.md
└── requirements.txt
```

### Module Description

| File | Responsibility |
|---|---|
| `create_database.py` | Creates the database. |
| `insert_data.py` | Inserts data in the database (The file contains mock data). |
| `capture_faces.py` | Captures and stores student face images. |
| `train_model.py` | Trains the LBPH recognition model. |
| `compare.py` | Captures faces and compares them against the trained model. |
| `check_eligibility.py` | Retrieves eligible students and verifies course eligibility. |
| `record_attendance.py` | Records examination sign-in and sign-out timestamps. |
| `main.py` | Coordinates the examination verification workflow. |

## How It Works

1. The examination officer enters the course code.
2. The system retrieves the students eligible for that course.
3. An examination session is created and the examination date is recorded.
4. The officer selects either Sign In or Sign Out.
5. The student presents their face to the webcam.
6. The system compares the captured face against the trained recognition model.
7. The recognised student's eligibility for the selected course is checked.
8. If eligible, the system records the sign-in time or updates the existing record with the sign-out time.
9. The officer can end the examination session.

## Database Design

The system uses SQLite to manage its records.

The main database tables include:

- **Eligible_Students:** Stores registered student information.
- **Course_Eligibility:** Stores the relationship between students and the courses they are eligible to take.
- **Exam_Sessions:** Stores examination session details, including course code, examination date, start time and end time.
- **Attendance:** Stores each student's examination sign-in and sign-out timestamps.

Each student has one attendance record per examination session. Signing out updates the existing record rather than creating another one.

## Installation and Setup

### Prerequisites

Before installing the project, ensure you have:

- Python 3 installed.
- A webcam.
- Windows operating system (required for the current Winsound implementation).

### 1. Clone the repository

```bash
git clone https://github.com/Alao-Muizah/Face-Recognition-Eligibility-system.git Face_Recognition
```

### 2. Navigate into the project directory

```bash
cd Face_Recognition
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Before running the system:

- Run the  `create_database.py` to create the database
- Run `insert_data.py` to insert mock data (you can also change the contents accordingly )

### 5. Capture student face images

Run the face capture script:

```bash
python src/capture_faces.py
```

During image capture, slightly vary your head position and facial orientation to collect 25 different face images.

This helps the model learn variations in the student's appearance.

**Note:** Face image collection is required before model training. Repeat the process for each student who needs to be registered.

### 6. Train the recognition model

After capturing the required student images, train the LBPH recognition model:

```bash
python src/train_model.py
```

This generates the trained model and label mapping required for face recognition.

### 7. Run the examination verification system

```bash
python main.py
```

## Requirements

The project requires:

- Python 3
- OpenCV with contrib modules (`opencv-contrib-python`)
- NumPy
- SQLite (included with Python)
- A webcam
- Windows operating system for the current Winsound implementation

## Limitations

- Recognition accuracy depends on the quality and variation of the training images.
- Lighting conditions and face positioning can affect recognition performance.
- The current system uses a configurable LBPH confidence-distance threshold.
- The current implementation uses a webcam for face capture and verification.
- Face recognition may produce incorrect or uncertain results, so manual verification may be required.
- The system is currently a prototype and requires further testing before deployment in actual examination environments.

## Future Improvements

- Develop a graphical user interface for examination officers.
- Improve recognition performance under different lighting conditions.
- Introduce additional verification mechanisms.
- Generate downloadable examination attendance reports.
- Improve database management and student registration workflows.


