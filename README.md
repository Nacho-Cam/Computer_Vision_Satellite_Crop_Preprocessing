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

This solution is designed so that users simply add their images into the provided `test_images` folder and run the script without needing to create additional directories manually.

## Features

- **Dynamic Preprocessing:** Automatically adjusts gamma and equalization based on image statistics.
- **Smart Thresholding:** Chooses the appropriate thresholding method according to image contrast.
- **Robust Morphological Filtering:** Uses closing and opening to remove noise and link broken segments.
- **Contour Analysis:** Extracts and filters contours by area and calculates useful metrics such as circularity and aspect ratio.
- **Easy-to-Use Structure:** Place your test images in the `test_images` folder and run the script. All outputs are saved automatically in the `results` folder.

## Installation

1. **Clone the repository:**

    git clone https://github.com/Nacho-Cam/Computer_Vision_Satellite_Crop_Preprocessing.git  
    cd Computer_Vision_Satellite_Crop_Preprocessing

2. **Install dependencies:**

    (Make sure you have Python 3 installed)
    
    pip install opencv-python numpy

## Usage

1. **Prepare your images:**  
   Copy your satellite crop images into the `test_images` folder in the project directory. Supported formats include PNG, JPG, JPEG, BMP, and TIFF.

2. **Run the script:**  
   From the project folder, execute:
    
    python main.py

3. **Review output:**  
   The script processes each image and saves output in the `results` folder. Each image gets its own subfolder containing:
   - `original.jpg` – the original image.
   - `canal_h_norm.jpg` – the normalized H channel.
   - `gauss.jpg` – the Gaussian smoothed image.
   - `preproc.jpg` – the preprocessed image (after gamma correction/equalization).
   - `bin_<method>.jpg` – the binary image produced via thresholding (with the method name indicated).
   - `morph.jpg` – the morphed binary image.
   - `contours_detected.jpg` – visualization of detected contours.
   - `contours_analysis.jpg` – annotated image with contour analysis.

## Pipeline Details

1. **Image Loading:**  
   Images are loaded from the `test_images` folder and processed automatically.

2. **Color Space Conversion and Normalization:**  
   The image is converted to HSV and the H channel is normalized to a 0–255 range to enhance color differences.

3. **Gaussian Smoothing:**  
   A Gaussian blur is applied to the normalized image to reduce noise.

4. **Adaptive Preprocessing:**  
   The pipeline analyzes the image’s mean and standard deviation. Based on these values:
   - Gamma Correction is applied if the image is too dark (mean < 60) or too bright (mean > 190).
   - Histogram equalization is applied if the contrast is low (standard deviation < 30).

5. **Dynamic Thresholding:**  
   The pipeline selects either Otsu's thresholding or adaptive thresholding based on the image’s standard deviation and the ratio of white pixels in the binary image. Fallbacks are implemented if the white pixel ratio is not within acceptable bounds.

6. **Morphological Operations:**  
   Closing (to fill in gaps) and opening (to remove small artifacts) operations are applied to the binary image.

7. **Contour Extraction and Analysis:**  
   Contours are extracted from the processed binary image using `cv2.findContours`. Small contours are filtered out using a dynamically calculated area threshold. For each significant contour, metrics such as area, perimeter, circularity, and aspect ratio are calculated. Minimum area rectangles are drawn and annotated.

## Output Files

For each processed image, a folder in the `results` directory will contain:

- **original.jpg:** The original satellite image.
- **canal_h_norm.jpg:** Normalized H channel image.
- **gauss.jpg:** Gaussian smoothed image.
- **preproc.jpg:** Image after adaptive preprocessing.
- **bin_<method>.jpg:** Binary image after thresholding (where `<method>` indicates the method used).
- **morph.jpg:** Binary image after morphological processing.
- **contours_detected.jpg:** Image with detected contours drawn in green.
- **contours_analysis.jpg:** Image with annotated contour analysis (minimum area rectangles and labels).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

- [OpenCV Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [GaussianBlur Documentation](https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html)
- [Otsu's Thresholding](https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html)
- [Morphological Operations in OpenCV](https://docs.opencv.org/master/d9/d61/tutorial_py_morphological_ops.html)
