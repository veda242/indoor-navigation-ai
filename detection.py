from ultralytics import YOLO

model = YOLO("yolov8n.pt")

important_classes = [
    "person", "chair", "table", "sofa", "bed",
    "refrigerator", "tv"
]

priority = {
    "person": 3,
    "chair": 2,
    "table": 2,
    "sofa": 1,
    "bed": 1,
    "refrigerator": 2,
    "tv": 1
}


def detect_objects(frame):
    results = model(frame)

    best_object = None
    best_score = 0

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in important_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                width = x2 - x1

                score = width * priority.get(label, 1)

                if score > best_score:
                    best_score = score
                    best_object = (label, x1, y1, x2, y2)

    return best_object