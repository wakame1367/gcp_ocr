from pathlib import Path

from google.cloud import vision
from google.cloud.vision import types

from cli import detection


def run():
    root_path = Path("resources/ocr")
    client = vision.ImageAnnotatorClient()
    for image_path in root_path.glob("*.jpg"):
        with image_path.open("rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        serialized = detection(mode="document", client=client, image=image)
        json_file_path = "document_detection_result" \
                         "_{}.json".format(str(image_path.stem))
        with open(json_file_path, "w", encoding="utf-8") as f:
            f.write(serialized)


if __name__ == '__main__':
    run()
