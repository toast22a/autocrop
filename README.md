# Autocrop

Using facial detection via Haar cascade classifier to automatically extract profile pictures from images.

## Dependencies
- **OpenCV** must be installed on the system.
- Python dependencies are frozen in `requirements.txt`.

This project contains two scripts:

## auto.py
The automatic profile picture extractor itself. `auto.py` reads raw images from directory `raw` and outputs cropped images into directory `cropped`. Desired pixel dimensions are currently hardcoded as constants in the script.

## manual.py
A typical cropping tool. Drag the cursor on the image to form the desired bounding box. Dimensions are currently hardcoded as constants in the script.
