import cv2

def detect_document(edges):
    cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        # Use 0.04 to be much more forgiving of slightly bent/curved edges
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        # Check if it has 4 corners and a reasonable minimum area (2000px)
        if len(approx) == 4 and cv2.contourArea(approx) > 2000:
            return approx.reshape(4, 2)
            
    return None
