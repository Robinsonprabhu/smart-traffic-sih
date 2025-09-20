import cv2
from ultralytics import YOLO
import os
import time

# === CONFIG ===
IMAGE_FOLDER = r"C:\Users\rajiv\Documents\NorthFolder\north"
SAVE_FOLDER = os.path.join(IMAGE_FOLDER, "results")
os.makedirs(SAVE_FOLDER, exist_ok=True)

MODEL_PATH = "yolov8m.pt"  # Medium YOLOv8 model for better accuracy
CONFIDENCE_THRESHOLD = 0.5  # 50% confidence
IGNORE_CLASSES = ["person"]  # classes to ignore

# Load YOLO model
model = YOLO(MODEL_PATH)

# Loop through images in folder
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(IMAGE_FOLDER, filename)
        img = cv2.imread(image_path)

        results = model(img)[0]  # detect objects
        boxes, labels, scores = [], [], []

        # Filter results
        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            label = model.names[int(cls)]
            if label not in IGNORE_CLASSES and conf >= CONFIDENCE_THRESHOLD:
                boxes.append(box)
                labels.append(label)
                scores.append(conf)

        # Annotate image
        annotated_img = img.copy()
        counts = {}
        for box, label in zip(boxes, labels):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated_img, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )
            counts[label] = counts.get(label, 0) + 1

        # Display counts on frame
        y_offset = 30
        for vehicle, count in counts.items():
            cv2.putText(
                annotated_img, f"{vehicle}: {count}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )
            y_offset += 40

        # Show frame
        cv2.imshow("Vehicle Detection", annotated_img)
        cv2.waitKey(10000)  # display for 10 seconds

        # Save annotated image
        save_path = os.path.join(SAVE_FOLDER, filename)
        cv2.imwrite(save_path, annotated_img)

cv2.destroyAllWindows()
print(f"Detection complete! Results saved in: {SAVE_FOLDER}")