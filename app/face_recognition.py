import face_recognition
import cv2
from .models import Student

def capture_face(image):
    rgb_frame = image[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_frame)
    if len(face_encodings) == 0:
        return None
    return face_encodings[0]

def recognize_faces(image):
    rgb_frame = image[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_frame)
    recognized_students = []
    students = Student.query.all()

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([student.face_encoding for student in students], face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            recognized_students.append(students[first_match_index])
    return recognized_students
