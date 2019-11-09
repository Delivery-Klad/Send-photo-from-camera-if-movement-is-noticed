import time
import smtplib
from email.contentmanager import subtype
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
import numpy as np

password = "sender password"
login2 = "sender email"
url = "smtp.mail.ru"
server = smtplib.SMTP_SSL(url, 465)
target = "target email"
title = "message title"
text = "message text"
filename0 = 'try.jpg'
filename1 = 'try2.jpg'
msg = MIMEMultipart()
msg['Subject'] = title
msg['From'] = login2
body = text
acceptable_value_min = 0
acceptable_value_max = 0
start = True

cam = cv2.VideoCapture(0)
time.sleep(10)

ret, start_photo = cam.read()
cv2.imwrite('try.jpg', start_photo)
cv2.imshow('try.jpg', start_photo)

time.sleep(1)
img1 = cv2.imread(filename0)
while True:
    can = True
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    cv2.imwrite('try2.jpg', frame)
    img2 = cv2.imread(filename1)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    y, x = np.unravel_index(result.argmax(), result.shape)
    if start:
        acceptable_value_min = result - 0.04
        acceptable_value_max = result + 0.04
        start = False
        print(acceptable_value_max, acceptable_value_min)
    if result < acceptable_value_min or result > acceptable_value_max:
        print(result)
        if can:
            can = False
            fp = open(filename1, 'rb')
            att = MIMEApplication(fp.read(), _subtype=subtype)
            fp.close()
            att.add_header('Content-Disposition', 'attachment', filename=filename1)
            msg.attach(att)
            msg.attach(MIMEText(body, 'plain'))
            # server.login(login2, password)
            # server.sendmail(login2, target, msg.as_string())
            print("take a photo")
    else:
        can = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

img1.close()
cam.release()
cv2.destroyAllWindows()
