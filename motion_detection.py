#from skimage.metrics import structural_similarity as compare_ssim
import cv2
cam=cv2.VideoCapture(0)
frame1=None
numberOfContours1=None
step=0
while True:
    ignore,frame=cam.read()
    #Increasing accuracy of feature detection:
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #smoothening the image for easier motion detection:
    blur=cv2.GaussianBlur(gray,(21,21),0)
    if frame1 is None:
        frame1=gray
    delta_frame=cv2.absdiff(frame1,gray)
    #(score, diff) = compare_ssim(gray, frame1, full=True)
    #diff = (diff * 255).astype("uint8")
    #print("SSIM: {}".format(diff))

    thresh=cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
    dilate=cv2.dilate(thresh,None,iterations=2)
    (cntrs,_)=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contourArea=[]
    for contour in cntrs:
        myContourArea=cv2.contourArea(contour)
   
        if myContourArea>1000:
            contourArea.append(myContourArea)
            cv2.drawContours(frame,cntrs,-1,(0,0,255),1)
        #(x,y,w,h)=cv2.boundingRect(contour)
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    numberOfContours=len(contourArea)
    if numberOfContours1==None:
        numberOfContours1=numberOfContours
    deltaContours=numberOfContours-numberOfContours1
    if deltaContours<0:
        deltaContours=0
        step=step+1
    print(step)
    numberOfContours1=numberOfContours

    frame1=gray
    cv2.imshow('My WEBCAM',frame)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()


         
         