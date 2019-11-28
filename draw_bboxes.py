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


def draw_boxes(image, bounds, color, confidences=None, width=5):
    draw = ImageDraw.Draw(image)
    if confidences:
        for confidence, bound in zip(confidences, bounds):
            confidence = confidence * 100
            base_x = bound.vertices[0].x
            base_y = bound.vertices[0].y - 10
            if base_x < 0:
                base_x = 0
            if base_y < 0:
                base_y = 0
            draw.line([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y,
                bound.vertices[0].x, bound.vertices[0].y],
                fill=color, width=width)
            draw.text((base_x, base_y), "{} %".format(round(confidence)),
                      (201, 34, 34))
    return image


def get_document_bounds(response, feature, use_confidence=False):
    document = response.full_text_annotation
    bounds = []
    confidences = []
    for page in document.pages:
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)
                if use_confidence:
                    confidences.append(block.confidence)
            for paragraph in block.paragraphs:
                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                    if use_confidence:
                        confidences.append(paragraph.confidence)
                for word in paragraph.words:
                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)
                        if use_confidence:
                            confidences.append(word.confidence)
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)
                            if use_confidence:
                                confidences.append(symbol.confidence)
    return bounds, confidences


def get_bounds(response):
    # only use text_annotations
    text_annotations = response.text_annotations
    bounds = [text_annotation.bounding_poly
              for text_annotation in text_annotations]
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
    bounds, confidences = get_document_bounds(response,
                                              feature=ts, use_confidence=True)
    # bounds = get_bounds(response)
    new_image = draw_boxes(image, bounds, 'yellow', confidences)
    new_image.save("result.jpg")


if __name__ == '__main__':
    main()
