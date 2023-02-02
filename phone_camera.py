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

# While loop to continuously fetching data from the Url
while True:
	img_resp = requests.get(url)
	img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
	img= cv2.imdecode(img_arr, -1)
	img= imutils.resize(img, width=1000, height=1800)
	cv2.imshow('My webcam',img)
	# Press Esc key to exit
	if cv2.waitKey(1) == 27:
		break
    
cv2.destroyAllWindows()

