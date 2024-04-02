from ultralytics import YOLO

model = YOLO("best.pt")


def detect(image_path):
    try:
        model.predict(
            source=image_path,
            save=True,
            conf=0.25,
            project=".",
            name="results",
            exist_ok=True,
        )
        return True
    except Exception as e:
        print(e)
        return False
