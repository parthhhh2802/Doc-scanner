import os
import cv2
from datetime import datetime

def save_capture(capture_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(output_dir, ts)
    
    saved_files = []
    
    def try_save(name, img):
        if img is not None:
            path = f"{base}_{name}.png"
            cv2.imwrite(path, img)
            saved_files.append(path)

    if capture_data.get('warped') is not None:
        try_save("rectified", capture_data.get('warped'))
        try_save("enhanced", capture_data.get('binary'))
        try_save("gray", capture_data.get('gray'))
        try_save("blue_mask", capture_data.get('blue_mask'))
        try_save("red_mask", capture_data.get('red_mask'))
        try_save("blue_marks", capture_data.get('blue_marks'))
        try_save("red_marks", capture_data.get('red_marks'))
    else:
        try_save("raw_photo", capture_data.get('frame'))
    
    return saved_files
