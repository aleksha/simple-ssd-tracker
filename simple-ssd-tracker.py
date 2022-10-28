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


black = (0,0,0); white = (255,0,0)

cap = cv2.VideoCapture(1)

empty_data = shelve.open("empty.shelve","r")
lx1_e = empty_data["lx1_empty"]
lx2_e = empty_data["lx2_empty"]
ly1_e = empty_data["ly1_empty"]
ly2_e = empty_data["ly2_empty"]
ly3_e = empty_data["ly3_empty"]
ly4_e = empty_data["ly4_empty"]


print("Duration: " + str(duration) )
print("Delta   : " + str(shot_time   ) )

prev_time  = time.time()
start_time = prev_time

out_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S%z")
os.mkdir(out_dir)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    crop_img = gray[Y:Y+H, X:X+W]
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    now_time = time.time()
    if (now_time - start_time)>duration:
        break
    if (now_time - prev_time)>shot_time:
        prev_time = now_time
        c_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S%z")
        cv2.imwrite(out_dir +'/frame_'+c_time+'.png',crop_img)
        #--- CROPING 
        crop_x1 = gray[y+syh-2:y+syh+3, x:x+w]
        crop_x2 = gray[y+syl-2:y+syl+3, x:x+w]
        crop_y1 = gray[y:y+h, x+0*w//4+shift-2:x+0*w//4+shift+3]
        crop_y2 = gray[y:y+h, x+1*w//4+shift-2:x+1*w//4+shift+3]
        crop_y3 = gray[y:y+h, x+2*w//4+shift-2:x+2*w//4+shift+3]
        crop_y4 = gray[y:y+h, x+3*w//4+shift-2:x+3*w//4+shift+3]

        xx, lx1 = profile_x(crop_x1)
        xx, lx2 = profile_x(crop_x2)
        yy, ly1 = profile_y(crop_y1)
        yy, ly2 = profile_y(crop_y2)
        yy, ly3 = profile_y(crop_y3)
        yy, ly4 = profile_y(crop_y4)

        px1=conv(lx1,lx1_e,xx)
        px2=conv(lx2,lx2_e,xx)
        py1=conv(ly1,ly1_e,yy)
        py2=conv(ly2,ly2_e,yy)
        py3=conv(ly3,ly3_e,yy)
        py4=conv(ly4,ly4_e,yy)

        sx1 = peaks_x(px1)
        sx2 = peaks_x(px2)
        sy1 = peaks_y(py1)
        sy2 = peaks_y(py2)
        sy3 = peaks_y(py3)
        sy4 = peaks_y(py4)
        found_value = find_val(sx1,sx2,sy1,sy2,sy3,sy4)
        print( c_time +"    "+found_value)

empty_data.close()
cap.release()
cv2.destroyAllWindows()

