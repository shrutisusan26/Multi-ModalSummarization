from tkinter.messagebox import RETRY
import cv2

def check_face_loc(img_h,img_w,x,y,w,h):
    x_center, y_center = img_w/2,img_h/2
    img_center = x+w/2,y+h/2
    bounds = x_center-img_w/4,x_center+img_w/4,y_center-img_h/4,y_center+img_h/4

    if img_center[0]>=bounds[0] and img_center[0]<=bounds[1] and img_center[1]>=bounds[2] and img_center[1]<=bounds[3]:
        return True
    else:
        return False

def face_detector(img,threshold=0.2):
    face_cascade = cv2.CascadeClassifier(r'E:\Multi-Modal Summarization\VideoSummarization\face_detector.xml')

    if type(img)==str:
        img = cv2.imread(img)
    img_h,img_w,_ = img.shape
    original_area = img_h*img_w

    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    
    if len(faces)==0:
        return False
    
    else:
        face_area = 0
        for (x, y, w, h) in faces:
            if check_face_loc(img_h,img_w,x,y,w,h):
                return True
            face_area+=w*h 
        area_occupied = face_area/original_area
        #print(area_occupied)
        return face_area
            


if __name__=="__main__":
    for i in range(1,4):
        face_detector(f"face_{i}.png",0.05)