import cv2
cap = cv2.VideoCapture(0) #0 or -1

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'H264'), 20, (width, height))
while True:
    ret, img = cap.read()
    writer.write(img)
    
    cv2.imshow('camera-0', img)
    if cv2.waitKey(1) & 0xFF == 27: #esc
        break
cap.release()
writer.release()
cv2.destroyAllwindows()
