# gcp_ocr
This repository is **GCP Vision API(Text/Document Detection) Python Sample**

## Before you start

**Setup Project** and **export GOOGLE_APPLICATION_CREDENTIALS**, **Install Cloud SDK**
[Cloud Vision API - Detect text in images](https://cloud.google.com/vision/docs/ocr)

## Installing

Use [Github - pipenv](https://github.com/pypa/pipenv)

```
git clone https://github.com/wakamezake/gcp_ocr.git
pipenv install
```

## How to use

```
python cli.py  path/to/file or gcs://path/to/file
```

```

```

## Detection results

|image_description|text_detection|document_text_detection|
|---|:---:|---:|
|original|中央揃え|右寄せ|
|detection_block|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/text_detection_block.jpg)|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/document_detection_block.jpg)|
|detection_paragraph|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/text_detection_para.jpg)|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/document_detection_para.jpg)|
|detection_word|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/text_detection_word.jpg)|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/document_detection_word.jpg)|
|detection_symbol|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/text_detection_symbol.jpg)|![](https://raw.githubusercontent.com/wakamezake/gcp_ocr/master/sample/document_detection_symbol.jpg)|