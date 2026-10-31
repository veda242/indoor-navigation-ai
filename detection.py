from ultralytics import YOLO

model = YOLO("yolov8n.pt")

important_classes = [
    "person", "chair", "table", "sofa", "bed",
    "refrigerator", "tv"
]

def detect_objects(frame):
    """Return every detected obstacle, not just one - the caller (which has
    depth info) decides which is most urgent to act on."""
    results = model(frame)

    objects = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in important_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                objects.append((label, x1, y1, x2, y2))

    return objects