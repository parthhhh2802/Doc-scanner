# Real-Time Document Scanner

A robust, real-time desktop application built with Python, OpenCV, and PySide6 that detects paper boundaries, corrects perspective distortion, and generates clean scanned documents directly from your webcam. It also includes specialized color-extraction features to isolate blue signatures and red ink stamps.

## Features

- **Live GUI**: A complete PySide6 desktop interface for a fluid camera experience.
- **Dynamic Camera Selection**: Multiple virtual/physical camera support via a dropdown menu.
- **Robust Auto-Detection**: Uses Auto-Canny edge detection and dynamic morphological operations to detect bent or slightly curved paper in varying lighting conditions.
- **Perspective Rectification (Homography)**: Converts angled shots into flat, upright digital scans.
- **Adaptive Enhancement**: Cleans up shadows and uneven lighting for maximum legibility.
- **Color Extractor**: Automatically separates and exports red and blue ink marks (like signatures or stamps).

## Installation

This project uses Python. Ensure you have Python 3.10+ installed.

1. **Clone or Download the Repository**
2. **Create a Virtual Environment**:
   ```powershell
   python -m venv .venv
   ```
3. **Activate the Environment**:
   - Windows: `.\.venv\Scripts\Activate.ps1`
   - Mac/Linux: `source .venv/bin/activate`
4. **Install Requirements**:
   ```powershell
   pip install opencv-python numpy PySide6
   ```

## How to Use

1. **Launch the App**:
   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```
2. **Select Your Camera**: 
   Use the dropdown menu at the bottom of the window to select your active webcam (useful if you have virtual cameras installed like OBS).
3. **Scan a Document**:
   - Hold a document up to the camera. For best results, place it against a contrasting background (e.g., white paper on a dark desk).
   - Wait for the **Green Box** to appear around the document edges in the Live Feed. The right pane will display a live preview of the flattened, scanned document.
4. **Capture & Save**:
   - When the green box is visible and the document looks correct, click **Capture Photo**.
   - Review the freeze-frame. If satisfied, click **Save Outputs**.
   - If no document was detected (no green box), clicking capture will simply take a standard raw photo.
5. **View Outputs**:
   - All scans and masks are saved with timestamped filenames in the automatically generated `output/` folder inside the project directory.

## Output Files

When you save a valid document scan, the application generates several artifacts:
- `*_rectified.png`: The raw, flattened color scan of the document.
- `*_gray.png`: The grayscale version of the scan.
- `*_enhanced.png`: A high-contrast adaptive threshold version (best for reading text).
- `*_blue_marks.png` / `*_red_marks.png`: The extracted isolated blue and red ink components (e.g., signatures or stamps).
