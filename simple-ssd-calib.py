import numpy as np
import datetime
import time
import cv2
import os
import shelve
from config import x, y, h, w, shift, syh, syl, ds, duration, shot_time
from config import X, Y, H, W, extra
from funcs import *
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)

black = (0,0,0); white = (255,0,0)

print("Please, target webcam to empty display and than press Q")

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray,(X,Y),(X+W,Y+H),black,3)
    cv2.rectangle(gray,(x,y),(x+w,y+h),white,3)

    cv2.line(gray,(x,y+syh),(x+w,y+syh),black,1)
    cv2.line(gray,(x,y+syl),(x+w,y+syl),black,1)

    cv2.line(gray,(x+0*w//4+shift,y),(x+0*w//4+shift,y+h),black,1)
    cv2.line(gray,(x+1*w//4+shift,y),(x+1*w//4+shift,y+h),black,1)
    cv2.line(gray,(x+2*w//4+shift,y),(x+2*w//4+shift,y+h),black,1)
    cv2.line(gray,(x+3*w//4+shift,y),(x+3*w//4+shift,y+h),black,1)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
crop_x1 = gray[y+syh-2:y+syh+3, x:x+w]
crop_x2 = gray[y+syl-2:y+syl+3, x:x+w]
crop_y1 = gray[y:y+h, x+0*w//4+shift-2:x+0*w//4+shift+3]
crop_y2 = gray[y:y+h, x+1*w//4+shift-2:x+1*w//4+shift+3]
crop_y3 = gray[y:y+h, x+2*w//4+shift-2:x+2*w//4+shift+3]
crop_y4 = gray[y:y+h, x+3*w//4+shift-2:x+3*w//4+shift+3]
#cv2.imwrite('test.png',crop_y2)

xx, lx1 = profile_x(crop_x1)
xx, lx2 = profile_x(crop_x2)

yy, ly1 = profile_y(crop_y1)
yy, ly2 = profile_y(crop_y2)
yy, ly3 = profile_y(crop_y3)
yy, ly4 = profile_y(crop_y4)

plt.plot(xx,lx1,"go")
plt.plot(xx,lx2,"bo")
plt.show()
plt.clf()
plt.plot(yy,ly1,"go")
plt.plot(yy,ly2,"bo")
plt.plot(yy,ly3,"ro")
plt.plot(yy,ly4,"yo")
plt.show()

empty_data = shelve.open("empty.shelve","n")
empty_data["x_empty"] = xx
empty_data["y_empty"] = yy
empty_data["lx1_empty"] = lx1
empty_data["lx2_empty"] = lx2
empty_data["ly1_empty"] = ly1
empty_data["ly2_empty"] = ly2
empty_data["ly3_empty"] = ly3
empty_data["ly4_empty"] = ly4
empty_data.close()

cap.release()
cv2.destroyAllWindows()

