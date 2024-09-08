import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*

model=YOLO('yolov8s.pt')



def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('veh1.mp4')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0

tracker=Tracker()

cy1=281
cy2=374
offset = 3
waiting_car = set()
detect_car = False


while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
   

    results=model.predict(frame)
 #   print(results)

    

    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")

    list=[]
             
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
            list.append([x1,y1,x2,y2])

    bbox_id=tracker.update(list)
    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        
        if cy1<(cy+offset) and cy1>(cy-offset) and cx > 530:
            waiting_car.add(id)
        
        elif cy2+offset<cy and cx >530:
            if id in waiting_car:
                waiting_car.remove(id)

        if cy1 - offset <= cy <= cy2 + offset:
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
            cv2.putText(frame, str(id), (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        print("waiting_car",len(waiting_car)," :", waiting_car)


    cv2.line(frame,(356,cy1),(715,cy1),(255,255,255),1)
    cv2.putText(frame,str("Enter"),(382, 277),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

    cv2.line(frame,(143,cy2),(922,cy2),(255,255,255),1)
    cv2.putText(frame,str("Exit"),(183, 369),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
