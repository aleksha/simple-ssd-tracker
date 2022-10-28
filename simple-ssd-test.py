import numpy as np
import datetime
import time
import cv2
import os
import shelve
from config import x, y, h, w, shift, syh, syl, ds, duration, shot_time
from config import X, Y, H, W, extra
from config import peak_pos_x, peak_pos_y, search_window
from funcs import *
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)

black = (0,0,0); white = (255,0,0)

print("Press Q for a test shot" )

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray,(X,Y),(X+W,Y+H),black,3)
    cv2.rectangle(gray,(x,y),(x+w,y+h),white,3)

    cv2.line(gray,(x,y+syh),(x+w,y+syh),black,5)
    cv2.line(gray,(x,y+syl),(x+w,y+syl),black,5)

    cv2.line(gray,(x+0*w//4+shift,y),(x+0*w//4+shift,y+h),black,5)
    cv2.line(gray,(x+1*w//4+shift,y),(x+1*w//4+shift,y+h),black,5)
    cv2.line(gray,(x+2*w//4+shift,y),(x+2*w//4+shift,y+h),black,5)
    cv2.line(gray,(x+3*w//4+shift,y),(x+3*w//4+shift,y+h),black,5)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('frame',gray)
cv2.imwrite('test_frame.png',gray)
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

empty_data = shelve.open("empty.shelve","r")
lx1_e = empty_data["lx1_empty"]
lx2_e = empty_data["lx2_empty"]
ly1_e = empty_data["ly1_empty"]
ly2_e = empty_data["ly2_empty"]
ly3_e = empty_data["ly3_empty"]
ly4_e = empty_data["ly4_empty"]


px1=conv(lx1,lx1_e,xx)
px2=conv(lx2,lx2_e,xx)
py1=conv(ly1,ly1_e,yy)
py2=conv(ly2,ly2_e,yy)
py3=conv(ly3,ly3_e,yy)
py4=conv(ly4,ly4_e,yy)

print(px1)
print(px2)
print(py1)
print(py2)
print(py3)
print(py4)


sx1 = peaks_x(px1)
sx2 = peaks_x(px2)
sy1 = peaks_y(py1)
sy2 = peaks_y(py2)
sy3 = peaks_y(py3)
sy4 = peaks_y(py4)

print(sx1)
print(sx2)
print(sy1)
print(sy2)
print(sy3)
print(sy4)


found_value = find_val(sx1,sx2,sy1,sy2,sy3,sy4)
print(found_value)

plt.plot(xx,lx1,"go")
plt.plot(xx,lx2,"bo")
plt.show()

plt.clf()
plt.plot(yy,ly1,"go")
plt.plot(yy,ly2,"bo")
plt.plot(yy,ly3,"ro")
plt.plot(yy,ly4,"yo")
plt.show()



empty_data.close()
cap.release()
cv2.destroyAllWindows()

