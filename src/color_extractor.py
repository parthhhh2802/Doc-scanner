import cv2
import numpy as np

def extract_color_marks(warped_bgr):
    hsv = cv2.cvtColor(warped_bgr, cv2.COLOR_BGR2HSV)
    
    # Blue mask
    lower_blue = np.array([90, 50, 40])
    upper_blue = np.array([140, 255, 255])
    mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Red mask
    lower_red1 = np.array([0, 50, 40])
    upper_red1 = np.array([10, 255, 255])
    mask_r1 = cv2.inRange(hsv, lower_red1, upper_red1)
    
    lower_red2 = np.array([160, 50, 40])
    upper_red2 = np.array([180, 255, 255])
    mask_r2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    mask_r = cv2.bitwise_or(mask_r1, mask_r2)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask_b = cv2.morphologyEx(mask_b, cv2.MORPH_OPEN, kernel)
    mask_r = cv2.morphologyEx(mask_r, cv2.MORPH_OPEN, kernel)
    
    marks_b = cv2.bitwise_and(warped_bgr, warped_bgr, mask=mask_b)
    marks_r = cv2.bitwise_and(warped_bgr, warped_bgr, mask=mask_r)
    
    return {
        'blue_mask': mask_b,
        'red_mask': mask_r,
        'blue_marks': marks_b,
        'red_marks': marks_r
    }
