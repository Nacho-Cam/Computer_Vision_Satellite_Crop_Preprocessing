import os
import cv2
import numpy as np

# Get the absolute path of the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def adaptive_preprocessing(image):
    """
    Receives a grayscale image and applies:
     - Gamma Correction if the mean is out of a specific range.
     - Histogram equalization if the standard deviation is low.
    Returns the preprocessed image.
    """
    gray = image.copy()
    mean_val = np.mean(gray)
    std_val = np.std(gray)

    # 1) Gamma Correction if the image is too dark or too bright
    #   For example:
    #   - if mean < 60, increase gamma
    #   - if mean > 190, decrease gamma
    gamma = 1.0
    if mean_val < 60:
        gamma = 1.5
    elif mean_val > 190:
        gamma = 0.7
    
    # Apply Gamma Correction if it's different from 1.0
    if abs(gamma - 1.0) > 0.01:
        gray_float = gray.astype(np.float32) / 255.0
        gray_corrected = cv2.pow(gray_float, gamma)
        gray = (gray_corrected * 255).astype(np.uint8)

    # 2) If the standard deviation is very low (low contrast), equalize the histogram
    if std_val < 30:
        gray = cv2.equalizeHist(gray)

    return gray

def adaptive_threshold(gray):
    """
    Applies a dynamic thresholding method.
    - If std > 30, use Otsu.
    - If std <= 30, use adaptive thresholding.
    - Verify the percentage of white pixels.
      If it is too high/low, fallback to the other method.
    Returns the binary image and the method used ("otsu" or "adapt").
    """
    std_val = np.std(gray)
    
    def ratio_of_white(binary_img):
        white_pixels = np.count_nonzero(binary_img)
        total_pixels = binary_img.size
        return white_pixels / total_pixels

    if std_val > 30:
        # Try Otsu's method
        _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ratio_otsu = ratio_of_white(bin_otsu)
        # If the white pixel ratio is in a reasonable range (e.g., 1% - 70%), use Otsu
        if 0.01 < ratio_otsu < 0.70:
            return bin_otsu, "otsu"
        else:
            # fallback to adaptive thresholding
            bin_adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
            return bin_adapt, "adapt_fallback"
    else:
        # Try adaptive thresholding
        bin_adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
        ratio_adapt = ratio_of_white(bin_adapt)
        if 0.01 < ratio_adapt < 0.70:
            return bin_adapt, "adapt"
        else:
            # fallback to Otsu's method
            _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return bin_otsu, "otsu_fallback"

def process_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return

    base_name = os.path.basename(image_path)
    name_no_ext, _ = os.path.splitext(base_name)
    output_dir = os.path.join(BASE_DIR, "results", name_no_ext)
    os.makedirs(output_dir, exist_ok=True)

    # Save original image
    cv2.imwrite(os.path.join(output_dir, "original.jpg"), img)

    # 1. Convert to HSV and normalize the H channel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_channel = hsv[:, :, 0]
    norm_h = cv2.normalize(h_channel, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite(os.path.join(output_dir, "canal_h_norm.jpg"), norm_h)

    # 2. Gaussian smoothing
    gauss = cv2.GaussianBlur(norm_h, (5, 5), 0)
    cv2.imwrite(os.path.join(output_dir, "gauss.jpg"), gauss)

    # 3. Adaptive preprocessing (gamma correction, optional equalization)
    preproc = adaptive_preprocessing(gauss)
    cv2.imwrite(os.path.join(output_dir, "preproc.jpg"), preproc)

    # 4. Dynamic thresholding
    bin_img, method_used = adaptive_threshold(preproc)
    cv2.imwrite(os.path.join(output_dir, f"bin_{method_used}.jpg"), bin_img)

    # 5. Morphological operations
    # Adjust kernel according to the image resolution
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(os.path.join(output_dir, "morph.jpg"), opened)

    # 6. Contour extraction
    contours, _ = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h, w = opened.shape[:2]
    total_area = float(h * w)

    # Define min_area as a % of the total area; adjust this factor as needed
    min_area_factor = 0.00005
    min_area = total_area * min_area_factor

    # Filter contours
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # 7. Visualization
    # Convert the preprocessed image to BGR to draw contours
    preproc_bgr = cv2.cvtColor(preproc, cv2.COLOR_GRAY2BGR)
    drawing_contours = preproc_bgr.copy()
    cv2.drawContours(drawing_contours, filtered_contours, -1, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(output_dir, "contours_detected.jpg"), drawing_contours)

    # (Optional) Analyze each contour and draw minimum area rectangles
    results = []
    analysis_img = preproc_bgr.copy()
    for i, cnt in enumerate(filtered_contours):
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        circ = 4.0 * np.pi * area / (perimeter**2) if perimeter != 0 else 0
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect).astype(np.int32)
        center, (rw, rh), angle = rect

        results.append({
            'id': i,
            'area': area,
            'perimeter': perimeter,
            'circularity': circ,
            'center': center,
            'width': rw,
            'height': rh,
            'aspect_ratio': max(rw, rh) / (min(rw, rh) + 1e-9),
            'angle': angle
        })

        cv2.drawContours(analysis_img, [box], 0, (0, 0, 255), 2)
        cv2.putText(analysis_img, f"#{i}", (int(center[0]), int(center[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imwrite(os.path.join(output_dir, "contours_analysis.jpg"), analysis_img)
    print(f"[OK] Processed: {image_path} (Method = {method_used}). "
          f"Detected {len(filtered_contours)} significant contours.")

def main():
    input_dir = os.path.join(BASE_DIR, "test_images")
    if not os.path.exists(input_dir):
        print("Input folder does not exist:", input_dir)
        return

    for file in os.listdir(input_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            path_img = os.path.join(input_dir, file)
            process_image(path_img)

if __name__ == "__main__":
    main()
