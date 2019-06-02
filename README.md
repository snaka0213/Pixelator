# Retro Game Picture Converter in Python

A python retro game picture converter from image

## How to Use

using module: `Pillow`, `scikit-learn`

1. Put `main.py` and the original picture in the same directory (supported formats -> [Pillow - Image file formats](https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#image-file-formats)).

2. Do
```bash
python main.py
```

##  How it Works

1. Convert the original picture to a mosaic picture.

2. Do color reduction processing via k-means clustering of colors used in the mosaic picture. 
