from config import peak_pos_x, peak_pos_y, search_window

def get_sign(ss):
    if ss[1] == 1:
        return "-"
    return "+"

def get_value(ss):
    if ss == (0,0,0,0,0,0,0):
        return "0"
    if ss == (1,0,1,1,1,1,1):
        return "0"
    if ss == (0,0,0,0,1,0,1):
        return "1"
    if ss == (1,1,1,0,1,1,0):
        return "2"
    if ss == (1,1,1,0,1,0,1):
        return "3"
    if ss == (0,1,0,1,1,0,1):
        return "4"
    if ss == (1,1,1,1,0,0,1):
        return "5"
    if ss == (1,1,1,1,0,1,1):
        return "6"
    if ss == (1,0,0,0,1,0,1):
        return "7"
    if ss == (1,1,1,1,1,1,1):
        return "8"
    if ss == (1,1,1,1,1,0,1):
        return "9"
    return "-1"

def profile_x(crop_img2):
    lx1=[]; px = []
    for l in range(63*4):
        px.append( l )
        lx = 0.
        for p in range(0,5):
            lx += crop_img2[p,l]
        lx1.append( int(lx/5.) )
    return(px,lx1)

def profile_y(crop_img2):
    lx1=[]; px = []
    for p in range(100):
        px.append( p )
        lx = 0.
        for l in range(0,5):
            lx += crop_img2[p,l]
        lx1.append( int(lx/5.) )
    return(px,lx1)


def conv(l,le,aa):
    for i in range(len(l)):
        l[i]= -(l[i]-le[i])
    for i in range(len(l)):
        if l[i]>20:
            l[i]=l[i]
        else:
            l[i]=0
    peaks = []
    m = 0; a=0
    for i in range(len(l)):
        if l[i]==0 and m!=0:
            peaks.append( a )
            m=0
            a=0
        else:
            if l[i]>m:
                m=l[i]
                a=aa[i]
    return(peaks)    

def peaks_x(px):
    s1=0;s2=0;s3=0
    s4=0;s5=0;s6=0
    s7=0;s8=0
    for p in px:
        if p>peak_pos_x[0]-search_window and p<peak_pos_x[0]+search_window  : s1=1
        if p>peak_pos_x[1]-search_window and p<peak_pos_x[1]+search_window  : s2=1
        if p>peak_pos_x[2]-search_window and p<peak_pos_x[2]+search_window  : s3=1
        if p>peak_pos_x[3]-search_window and p<peak_pos_x[3]+search_window  : s4=1
        if p>peak_pos_x[4]-search_window and p<peak_pos_x[4]+search_window  : s5=1
        if p>peak_pos_x[5]-search_window and p<peak_pos_x[5]+search_window  : s6=1
        if p>peak_pos_x[6]-search_window and p<peak_pos_x[6]+search_window  : s7=1
        if p>peak_pos_x[7]-search_window and p<peak_pos_x[7]+search_window  : s8=1

    return( (s1,s2,s3,s4,s5,s6,s7,s8) )

def peaks_y(py):
    s1=0;s2=0;s3=0
    for p in py:
        if p>peak_pos_y[0]-search_window and p<peak_pos_y[0]+search_window  : s1=1
        if p>peak_pos_y[1]-search_window and p<peak_pos_y[1]+search_window  : s2=1
        if p>peak_pos_y[2]-search_window and p<peak_pos_y[2]+search_window  : s3=1
    return( (s1,s2,s3) )

def find_val(sx1,sx2,sy1,sy2,sy3,sy4):
    ss1 = ( sy1[0], sy1[1], sy1[2], sx1[0], sx1[1], sx2[0], sx2[1] )
    ss2 = ( sy2[0], sy2[1], sy2[2], sx1[2], sx1[3], sx2[2], sx2[3] )
    ss3 = ( sy3[0], sy3[1], sy3[2], sx1[4], sx1[5], sx2[4], sx2[5] )
    ss4 = ( sy4[0], sy4[1], sy4[2], sx1[6], sx1[7], sx2[6], sx2[7] )
    answer = ""
    answer += get_sign(ss1)
    answer += get_value(ss2) + "."
    answer += get_value(ss3)
    answer += get_value(ss4)
    return( answer )
