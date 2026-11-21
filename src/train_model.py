import cv2 as cv 
import os 
import numpy as np 
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)


dataset_path = "dataset"
faces = []
labels = []

label_map = {}

current_label = 0 

for student_id in os.listdir(dataset_path):
    student_path = os.path.join(dataset_path, student_id)
    
    if not os.path.isdir(student_path): 
        continue 
    
    current_label += 1 
    label_map[current_label] = student_id 
    
    for image_name in os.listdir(student_path):
        image_path = os.path.join(student_path, image_name)
        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        
        if image is None:
            print(f"Could not read image: {image_path}")
            continue 
        
        faces.append(image)
        labels.append(current_label)
        
labels = np.array(labels, dtype=np.int32)

# creating the LBPH face recognizer
recognizer = cv.face.LBPHFaceRecognizer_create(radius =1, 
                                               neighbors = 8,
                                               grid_x = 8,
                                               grid_y = 8)

# Train recognizer 
recognizer.train(faces, labels)
recognizer.write(os.path.join(MODEL_DIR, "trainer.yml"))
    
np.save(os.path.join(MODEL_DIR, "Label_map.npy"), label_map)

print("Training completed")
print(f"Number of face images: {len(faces)}")
print(f"Number of students: {len(label_map)}")


