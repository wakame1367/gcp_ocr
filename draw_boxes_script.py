import json
from pathlib import Path

from PIL import Image
from google.cloud.vision import types
from google.protobuf import json_format

from draw_bboxes import draw_boxes, get_document_bounds, FeatureType


def run():
    image_root_path = Path("resources/ocr/images")
    json_root_path = Path("resources/ocr/json")
    for image_path, json_path in zip(image_root_path.glob("*"),
                                     json_root_path.glob("document_*.json")):
        print(image_path, json_path)
        with open(str(json_path), "r")as f:
            _json = json.load(f)
        response = json_format.Parse(json.dumps(_json),
                                     types.AnnotateImageResponse())
        image = Image.open(image_path)
        bounds, confidences = get_document_bounds(response,
                                                  feature=FeatureType(5),
                                                  use_confidence=True)
        new_image = draw_boxes(image, bounds, 'yellow', confidences)
        filename = "symbol_{}.jpg".format(image_path.stem)
        new_image.save(filename)


if __name__ == '__main__':
    run()
