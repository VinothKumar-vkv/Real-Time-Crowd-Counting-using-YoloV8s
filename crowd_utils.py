from ultralytics import YOLO
import cv2
import numpy as np
from itertools import combinations

model = YOLO("yolov8s.pt")  # Load the YOLOv8 model

def process_frame(frame, distance_threshold=100, show_lines=True):
    results = model(frame)
    annotated_frame = results[0].plot()

    boxes_data = results[0].boxes
    centroids = []

    if boxes_data and boxes_data.xyxy is not None:
        boxes = boxes_data.xyxy.cpu().numpy()
        classes = boxes_data.cls.cpu().numpy()

        for i, cls in enumerate(classes):
            if int(cls) == 0:  # class 0 is "person"
                x1, y1, x2, y2 = boxes[i]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                centroids.append((cx, cy))

        violation_count = 0
        # Draw social distance lines
        if show_lines:
            for (p1, p2) in combinations(centroids, 2):
                distance = np.linalg.norm(np.array(p1) - np.array(p2))
                if distance < distance_threshold:
                    color = (0, 0, 255)  # Red line for violation
                    violation_count += 1
                else:
                    color = (0, 255, 0)  # Green line for safe
                cv2.line(annotated_frame, p1, p2, color, 2)
    else:
        violation_count = 0

    return annotated_frame, len(centroids), violation_count
