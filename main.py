from PIL.Image import ImageTransformHandler
import cv2
import numpy as np
import pytesseract
import time
from flask import Flask, render_template, Response

pytesseract.pytesseract.tesseract_cmd="C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"

cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
states={"AN":"Andaman and Nicobar",
    "AP":"Andhra Pradesh","AR":"Arunachal Pradesh",
    "AS":"Assam","BR":"Bihar","CH":"Chandigarh",
    "DN":"Dadra and Nagar Haveli","DD":"Daman and Diu",
    "DL":"Delhi","GA":"Goa","GJ":"Gujarat",
    "HR":"Haryana","HP":"Himachal Pradesh",
    "JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala",
    "LD":"Lakshadweep","MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur",
    "ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa",
    "PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu",
    "TR":"Tripura","UP":"Uttar Pradesh", "WB":"West Bengal","CG":"Chhattisgarh",
    "TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(extract_num(), mimetype='multipart/x-mixed-replace; boundary=frame')


def extract_num():
    img=cv2.VideoCapture(0)


    while(True):
        # Capture image frame-by-frame
        ret, frame = img.read()
        #time.sleep(1)
        success, buffer = cv2.imencode('.jpg', frame)
        fr = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + fr + b'\r\n')
        # Our operations on the frame come here
        #img=cv2.resize(img,None,fx=0.5,fy=0.5)
        #Img To Gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        nplate=cascade.detectMultiScale(gray,1.1,4)
        #crop portion
        for (x,y,w,h) in nplate:
            wT,hT,cT=frame.shape
            a,b=(int(0.02*wT),int(0.02*hT))
            plate=frame[y+a:y+h-a,x+b:x+w-b,:]
            #make the frame more darker to identify LPR
            kernel=np.ones((1,1),np.uint8)
            plate=cv2.dilate(plate,kernel,iterations=1)
            plate=cv2.erode(plate,kernel,iterations=1)
            plate_gray=cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
            (thresh,plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)
            #read the text on the plate
            read=pytesseract.image_to_string(plate)
            read=''.join(e for e in read if e.isalnum())
            print(read)
            stat=read[0:2]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(51,51,255),2)
            cv2.rectangle(frame,(x-1,y-40),(x+w+1,y),(51,51,255),-1)
            cv2.putText(frame,read,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + plate + b'\r\n')
            
            #cv2.imshow("plate",plate)

        # Display the resulting frame
        #cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    if cv2.waitKey(0)==113:
        exit()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",use_reloader=False)