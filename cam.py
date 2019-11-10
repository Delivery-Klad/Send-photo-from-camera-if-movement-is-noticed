import time
import smtplib
from email.contentmanager import subtype
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
import numpy as np

password = "sender password"  # пароль почты, с которой производится отправка
login2 = "sender email"  # логин почты, с которой производится отправка
url = "smtp.mail.ru"  # mail / yandex / gmail и т.д
server = smtplib.SMTP_SSL(url, 465)
target = "target email"  # целевая почта для отправки
title = "message title"  # тема сообщения
text = "message text"  # текст сообщения
NormalState = 'NormalState.jpg'
UnNormalState = 'UnNormalState.jpg'
msg = MIMEMultipart()
msg['Subject'] = title
msg['From'] = login
body = text
acceptable_value_min = 0  # минимальное значение погрешности
acceptable_value_max = 0  # максимальное значение погрешности
start = True

cam = cv2.VideoCapture(0)
time.sleep(10)

ret, start_photo = cam.read()
cv2.imwrite(NormalState, start_photo)  # сохранение начального состояния
cv2.imshow(NormalState, start_photo)  # отображение начального состояния

time.sleep(1)
NormalImg = cv2.imread(NormalState)  # начальное состояние
while True:
    can = True
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # преобразование в оттенки серого (не используется)
    cv2.imshow('frame', gray)  # отображение текущего состояния
    cv2.imwrite(UnNormalState, frame)  # сохранение текущего состояния
    CurrentImg = cv2.imread(UnNormalState)  # текущее состояние
    result = cv2.matchTemplate(NormalImg, CurrentImg, cv2.TM_CCOEFF_NORMED)  # сравнение начального состояния с текущим
    y, x = np.unravel_index(result.argmax(), result.shape)
    if start:  # рассчет погрешности
        acceptable_value_min = result - 0.04  # мин. погрешность
        acceptable_value_max = result + 0.04  # макс. погрешность
        start = False
        print(acceptable_value_max, acceptable_value_min)
    if result < acceptable_value_min or result > acceptable_value_max:  # выход за пределы допустимых значений
        print(result)
        if can:  # отправка сообщения
            can = False
            UnNormalState = open(UnNormalState, 'rb')
            att = MIMEApplication(UnNormalState.read(), _subtype=subtype)
            UnNormalState.close()
            att.add_header('Content-Disposition', 'attachment', filename=UnNormalState)
            msg.attach(att)
            msg.attach(MIMEText(body, 'plain'))
            server.login(login, password)
            server.sendmail(login, target, msg.as_string())
            print("take a photo")
    else:
        can = True
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

NormalImg.close()
cam.release()
cv2.destroyAllWindows()  # закрытие всех окон

