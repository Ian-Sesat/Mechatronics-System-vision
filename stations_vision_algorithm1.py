# Import essential libraries
import requests
import cv2
import numpy as np
import imutils

#getting the IP address from IPWebcam
ip_address=input('Enter your IP address: ')
url = "http://"+ip_address+"/shot.jpg"
print (url)
img1=None
numberOfContours1=None
step=0
# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img= cv2.imdecode(img_arr, -1)
    img= imutils.resize(img, width=1000, height=1800)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(21,21),0)
    #Increasing accuracy of feature detection:
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #smoothening the image for easier motion detection:
    blur=cv2.GaussianBlur(gray,(21,21),0)
    if img1 is None:
        img1=gray
    delta_frame=cv2.absdiff(img1,gray)
    #(score, diff) = compare_ssim(gray, frame1, full=True)
    #diff = (diff * 255).astype("uint8")
    #print("SSIM: {}".format(diff))

    thresh=cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
    dilate=cv2.dilate(thresh,None,iterations=2)
    (cntrs,_)=cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contourArea=[]
    for contour in cntrs:
        myContourArea=cv2.contourArea(contour)
        if myContourArea>1500:
            contourArea.append(myContourArea)
            cv2.drawContours(img,cntrs,-1,(0,0,255),1)
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

    img1=gray
    cv2.imshow('My WEBCAM',img)
    if cv2.waitKey(1)&0xff==ord('q'):
        break


cv2.destroyAllWindows()


