# Adaptive Satellite Image Preprocessing and Segmentation

This project implements an adaptive image processing pipeline using OpenCV and Python designed for satellite images. It dynamically adjusts preprocessing parameters based on the image statistics (e.g., mean and standard deviation) to choose the best thresholding method (Otsu or adaptive thresholding) and filters contours accordingly.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Description](#pipeline-description)
- [Output Files](#output-files)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Overview

This project provides an adaptive pipeline for preprocessing satellite images. The pipeline consists of:
- Converting images to HSV and normalizing the H channel.
- Applying Gaussian smoothing.
- Adaptive preprocessing using gamma correction and histogram equalization.
- Dynamic thresholding using Otsu's method or adaptive thresholding based on image contrast.
- Morphological operations to clean up the binary image.
- Extraction of significant contours along with analysis and annotation.

The goal is to improve segmentation performance across images that may vary widely in brightness, contrast, and resolution.

## Features

- **Adaptive Preprocessing:**  
  Adjusts image brightness using gamma correction and applies histogram equalization when necessary.
- **Dynamic Thresholding:**  
  Automatically selects between Otsu’s global thresholding and adaptive thresholding based on image contrast.
- **Morphological Operations:**  
  Uses closing and opening to refine the binary segmentation.
- **Contour Extraction & Analysis:**  
  Filters and analyzes contours based on dynamically set area thresholds and draws minimum area rectangles around significant contours.
- **Simple Integration:**  
  Simply add your test images to the `test_images` folder and run the script.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_project.git
   cd your_project
Install required packages:

Ensure you have Python 3 installed. Then, install the necessary dependencies:

bash
Copiar
pip install opencv-python numpy
Usage
Add your images:
Place your satellite test images into the test_images folder in the project directory. Supported formats are PNG, JPG, JPEG, BMP, and TIFF.

Run the script:

From the project folder, execute:

bash
Copiar
python main.py
Review the results:
The script creates a results folder where each image gets its own subfolder containing the following files:

original.jpg: The original image.

canal_h_norm.jpg: The normalized H channel from HSV.

gauss.jpg: The Gaussian smoothed image.

preproc.jpg: The image after adaptive preprocessing.

bin_<method>.jpg: The binary image produced using the selected thresholding method.

morph.jpg: The binary image after morphological operations.

contours_detected.jpg: Visualization of detected contours.

contours_analysis.jpg: The image with drawn minimum area rectangles and annotated contours.

Pipeline Description
Image Loading:
The script loads each image from the test_images folder. No manual folder creation is required—just add your images.

Conversion to HSV & Normalization:
Converts the image to HSV and normalizes the H channel to a 0–255 range.

Gaussian Smoothing:
A Gaussian blur is applied to reduce noise.

Adaptive Preprocessing:
Uses the adaptive_preprocessing function to:

Apply gamma correction if the image is too dark (<60 mean) or too bright (>190 mean).

Perform histogram equalization if the image has low contrast (standard deviation < 30).

Dynamic Thresholding:
The adaptive_threshold function chooses:

Otsu’s method if the standard deviation is higher (good contrast).

Adaptive thresholding if the standard deviation is low. It verifies the ratio of white pixels and may fallback if the result is not within acceptable bounds.

Morphological Operations:
Performs morphological closing and opening on the binary image to clean it up.

Contour Extraction & Analysis:
Extracts contours using cv2.findContours and filters out small contours based on a dynamically calculated area threshold. Each significant contour is analyzed and annotated.

Output Files
Within each subfolder in the results directory, you will find:

original.jpg: The original satellite image.

canal_h_norm.jpg: Normalized H channel image.

gauss.jpg: Gaussian smoothed image.

preproc.jpg: Preprocessed image (after adaptive gamma correction and/or histogram equalization).

bin_<method>.jpg: Binary image from thresholding (method indicated in the filename).

morph.jpg: Morphologically processed binary image.

contours_detected.jpg: Image showing detected contours in green.

contours_analysis.jpg: Image with minimum area rectangles and contour labels drawn in red.

Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

License
This project is released under the MIT License. See the LICENSE file for more details.

References
OpenCV Python Tutorials

GaussianBlur Documentation

Otsu's Thresholding

Morphological Operations in OpenCV