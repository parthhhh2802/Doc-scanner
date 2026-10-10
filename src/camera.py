import cv2

class Camera:
    def __init__(self, camera_id=0):
        self.cap = None
        self.open_camera(camera_id)
        
    def open_camera(self, camera_id):
        if self.cap is not None:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened() or not self.cap.read()[0]:
            self.cap.release()
            self.cap = cv2.VideoCapture(camera_id)
        
        # Set resolution explicitly to fix some Windows camera issues
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
    def read_frame(self):
        if not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        return frame if ret else None
        
    def release(self):
        self.cap.release()
