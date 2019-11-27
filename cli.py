"""
Reference:
https://github.com/googleapis/google-cloud-python/tree/master/vision
"""
import argparse
from pathlib import Path
from pprint import pprint

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson

data_path = Path("resources")
if not data_path.exists():
    data_path.mkdir()


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="gcs link or local file path")
    parser.add_argument("--mode", "m", type=str, default="text",
                        help="text or document detection default(=text)")
    _args = parser.parse_args()
    return _args


def is_support_audio_encoding(audio_config, input_config):
    for ac in audio_config:
        if ac.name.lower() == input_config.lower():
            return True
    return False


def detection(mode):
    if mode == "text":
        text_detection()
    else:
        document_detection()


def text_detection():
    pass


def document_detection():
    pass


def main():
    args = get_arguments()
    detect_mode = args.mode
    if detect_mode in {"text", "document"}:
        raise ValueError("{} not supported".format(detect_mode))

    gcs_prefix = "gs://"
    file_path = Path(args.path)

    client = vision.ImageAnnotatorClient()
    if args.path.startswith(gcs_prefix):
        image = vision.types.Image()
        image.source.image_uri = str(file_path)
        print('Waiting for operation to complete...')
        response = client.text_detection(image=image)
        # https://github.com/googleapis/google-cloud-python/issues/3485
        serialized = MessageToJson(response)
        with open("text_detection_result.json", "w", encoding="utf-8") as f:
            f.write(serialized)
    else:
        if not file_path.exists():
            raise FileExistsError("{} not exist".format(file_path))
        else:
            with file_path.open("rb") as image_file:
                content = image_file.read()
            image = types.Image(content=content)
            print('Waiting for operation to complete...')
            response = client.text_detection(image=image)
            pprint(response)
            # https://github.com/googleapis/google-cloud-python/issues/3485
            serialized = MessageToJson(response)
            with open("text_detection_result.json", "w", encoding="utf-8") as f:
                f.write(serialized)


if __name__ == '__main__':
    main()
