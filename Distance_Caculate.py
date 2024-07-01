import cv2
import time
import imutils
from yoloDet import YoloTRT
import serial

# Constants
OBJECT_WIDTH = 19.5  # cm (The actual width of the motorcycle Wave S)
FOCAL_LENGTH = 435  # pre-determined focal length

# Function to estimate distance
def estimate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

# Function to send data over serial
def send_data(data):
    data_str = f"{data}\n"
    ser.write(data_str.encode())

# Initialize serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Load YOLOv5 model with TensorRT
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/yolov5n.engine", conf=0.25, yolo_ver="v5")

# Function to detect objects and get their widths in pixels
def get_object_width_in_image(image):
    detections, _ = model.Inference(image)
    data_list = []
    for obj in detections:
        class_name = obj['class']
        confidence = obj['conf']
        box = obj['box']

        if confidence >= 0.5:  # Confidence threshold and specific object
            x1, y1, x2, y2 = map(int, box)
            width = x2 - x1
            data_list.append([class_name, width, (x1, y1)])
            print(f"Class: {class_name}, Width: {width}")

            # Draw rectangle and label on the object
            color = (0, 255, 0)  # Green color for detected object
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    return data_list

# Function to calculate distance
def distance_finder(focal_length, real_object_width, width_in_frame):
    if width_in_frame == 0:
        return 0
    return (real_object_width * focal_length) / width_in_frame

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Open a file to write the data
with open('Dynamic_experiment.txt', 'w') as file:  # Use 'w' mode to write to the file
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame to 640x640
        frame = imutils.resize(frame, height=640, width=640)

        # Detect objects in the frame
        detected_objects = get_object_width_in_image(frame)

        for obj in detected_objects:
            distance = distance_finder(FOCAL_LENGTH, OBJECT_WIDTH, obj[1])
            send_data(distance)
            x, y = obj[2]
            cv2.putText(frame, f"Distance: {round(distance, 3)} cm", (int(x), int(y) - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0), 2)
            
            # Write the data to file
            file.write(f"{round(distance, 2)}\n")
            
            # Send the distance data over serial
            # send_data(distance)
   

        # Display the frame
        cv2.imshow("Webcam", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

