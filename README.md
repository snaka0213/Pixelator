# Retro Game Picture Converter in Python

A python retro game picture converter

## How to Use

Module: `Pillow`, `scikit-learn`

Put `main.py` and the original picture in the same directory (supported formats -> [Pillow - Image file formats](https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html)).

```bash
python main.py
```

##  How it Works

1. Convert the original picture to a mosaic picture:

|Input| |Mosaic|
|---|---|---|
|<img src = "https://github.com/snaka0213/dot_converter/blob/images/before.png" width = "200x200">| → |<img src = "https://github.com/snaka0213/dot_converter/blob/images/mosaic.png" width = "200x200">|

(In this example, the `filter_size` is assumed to be `5` pixel.)

2. Do color reduction processing via k-means clustering of colors which is used in the mosaic picture:

|Mosaic| |Output|
|---|---|---|
|<img src = "https://github.com/snaka0213/dot_converter/blob/images/mosaic.png" width = "200x200">| → |<img src = "https://github.com/snaka0213/dot_converter/blob/images/after.png" width = "200x200">|

(In this example, the `k = num_of_colors` is assumed to be `16`.)
