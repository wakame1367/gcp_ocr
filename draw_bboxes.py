"""
References:
    https://a244.hateblo.jp/entry/2018/04/22/222515
    https://a244.hateblo.jp/entry/2018/06/02/224659
    https://medium.com/searce/tips-tricks-for-using-google-vision-api-for-text-detection-2d6d1e0c6361
"""

import argparse
import json
from enum import Enum
from pathlib import Path

from PIL import Image, ImageDraw
from google.cloud.vision import types
from google.protobuf import json_format


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color, width=5):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
    return image


def get_document_bounds(response, feature):
    document = response.full_text_annotation
    bounds = []
    for i, page in enumerate(document.pages):
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)
                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)
    return bounds


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=str, help="json file path")
    parser.add_argument("image_path", type=str, help="json file path")
    parser.add_argument("--text_structure", "-t", type=int, default=2,
                        help="Hierarchy of extracted text structure"
                             "(https://cloud.google.com/vision/docs/features-list)"
                             " default(=2(BLOCK))")
    _args = parser.parse_args()
    return _args


def main():
    args = get_arguments()
    json_file_path = Path(args.json_path)
    image_file_path = Path(args.image_path)
    ts = FeatureType(args.text_structure)
    with open(json_file_path, "r")as f:
        _json = json.load(f)
    # parse json
    response = json_format.Parse(json.dumps(_json),
                                 types.AnnotateImageResponse())

    image = Image.open(image_file_path)
    bounds = get_document_bounds(response, feature=ts)
    new_image = draw_boxes(image, bounds, 'yellow')
    new_image.save("result.jpg")


if __name__ == '__main__':
    main()
