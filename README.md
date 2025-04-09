# Computer Vision Satellite Crop Preprocessing

This repository contains an adaptive image processing pipeline for satellite crop imagery using OpenCV and Python. The project focuses on preprocessing satellite images for crop segmentation and analysis. The pipeline dynamically adjusts preprocessing parameters based on image characteristics, allowing it to adapt to variations in brightness, contrast, and resolution among input images.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Output Files](#output-files)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Overview

Satellite images often vary significantly in terms of brightness, contrast, and noise. This project implements an adaptive pipeline that preprocesses satellite images to improve segmentation of crop areas. The pipeline includes several steps:
- **Color Space Conversion and Channel Normalization:** Convert images to HSV and normalize the H channel.
- **Gaussian Smoothing:** Reduce noise while preserving important edges.
- **Adaptive Preprocessing:** Apply gamma correction and histogram equalization dynamically based on the image’s brightness and contrast.
- **Dynamic Thresholding:** Choose between Otsu’s and adaptive thresholding methods, based on image statistics, to produce a clean binary image.
- **Morphological Operations:** Clean up the binary image using closing and opening.
- **Contour Extraction and Analysis:** Detect and filter significant contours, and generate visualizations with annotated crop areas.

This solution is designed so that users simply drop their images into the provided folder and run the script without needing to create additional directories manually.

## Features

- **Dynamic Preprocessing:** Automatically adjusts gamma and equalization based on image statistics.
- **Smart Thresholding:** Chooses the appropriate thresholding method according to image contrast.
- **Robust Morphological Filtering:** Uses closing and opening to remove noise and link broken segments.
- **Contour Analysis:** Extracts and filters contours by area and calculates useful metrics, such as circularity and aspect ratio.
- **Easy-to-Use Structure:** Place your test images in the `test_images` folder and run the script. All outputs are saved automatically in the `results` folder.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Nacho-Cam/Computer_Vision_Satellite_Crop_Preprocessing.git
   cd Computer_Vision_Satellite_Crop_Preprocessing
Install dependencies:

Make sure you have Python 3 installed. Then run:

bash
Copiar
pip install opencv-python numpy
Usage
Prepare your images:

Copy your satellite crop images into the test_images folder. Supported formats include PNG, JPG, JPEG, BMP, and TIFF.

Run the script:

From the repository root, run:

bash
Copiar
python main.py
Review output:

The script processes each image and saves output in the results folder. Each image gets its own subfolder containing:

original.jpg – the original image.

canal_h_norm.jpg – the normalized H channel.

gauss.jpg – the Gaussian smoothed image.

preproc.jpg – the preprocessed image (after gamma correction/equalization).

bin_<method>.jpg – the binary image produced via thresholding (with method name).

morph.jpg – the morphed binary image.

contours_detected.jpg – visualization of detected contours.

contours_analysis.jpg – annotated image with contour analysis.

Pipeline Details
Image Loading:
Images are loaded from the test_images folder and processed automatically.

Color Space Conversion and Normalization:
The image is converted to HSV; the H channel is then normalized to enhance color differences.

Gaussian Smoothing:
A Gaussian blur is applied to the normalized image to reduce noise.

Adaptive Preprocessing:
The pipeline analyzes the image’s mean and standard deviation. Based on these values:

Gamma Correction is applied if the image is too dark (<60) or too bright (>190).

Histogram equalization is applied if the contrast is low (std < 30).

Dynamic Thresholding:
Depending on the standard deviation, the pipeline selects either Otsu's thresholding or adaptive thresholding. The white pixel ratio is verified to decide on a fallback if necessary.

Morphological Operations:
Closing (to fill in gaps) and opening (to remove small artifacts) are applied to the binary image.

Contour Extraction and Analysis:
Contours are extracted and filtered by area (relative to the total image area). For each contour, key metrics are calculated, and minimum area rectangles are drawn and annotated.

Output Files
For each processed image, a folder in the results directory will contain:

original.jpg: The original satellite image.

canal_h_norm.jpg: Normalized H channel image.

gauss.jpg: Gaussian smoothed image.

preproc.jpg: Image after adaptive preprocessing.

bin_<method>.jpg: Binary image after thresholding (where <method> indicates the thresholding method used).

morph.jpg: Binary image after morphological processing.

contours_detected.jpg: Image with detected contours drawn in green.

contours_analysis.jpg: Image with annotated contour analysis (rectangles and labels).

Contributing
Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

References
OpenCV Python Tutorials

GaussianBlur Documentation

Otsu's Thresholding

Morphological Operations in OpenCV