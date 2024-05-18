import cv2

def capture_image():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")

    ret, frame = video_capture.read()
    if not ret:
        raise Exception("Failed to capture image")

    video_capture.release()
    return frame

def save_image(image, filename):
    cv2.imwrite(filename, image)
