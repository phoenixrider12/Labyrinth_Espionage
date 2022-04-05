import cv2
import numpy as np
import math

val={
    'Green': [[ 41, 8,  17],[ 82, 255, 255],[1,0,0],[0,0,0]], 
    'YellowChand': [[ 13, 148,  160], [ 54, 255, 255],[1,0,0],[0,0,0]],
    'BlueChand': [[77, 15, 178], [114, 116, 255],[1,0,0],[0,0,0]],
    'Red': [[0, 255, 182], [30, 255, 255],[151,255,182],[179,255,255]], 
    'PinkiSquare': [[163, 84, 164], [179, 139, 255],[1,0,0],[0,0,0]], 
    'BlueSquare': [[102, 175, 73], [116, 255, 163],[1,0,0],[0,0,0]], 
    'SpecialRed': [[147, 255, 40], [179, 255, 157],[0,236,35],[0,255,131]]
}
st = {
    "RA":"0",
    "LA":"1",
    "TA":"2",
    "DA":"3",
    "GC":"4",
    "YC":"5",
    "PS":"6",
    "BC":"7",
    "RC":"8",
    "BS":"9",
    "ST":".",
    "SS":"-",
    "SC":",",
}

def dist(a,b):
   return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def decode(img):
    """
    Decodes a given image.
    """
    to_sort=[]
    hav=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for k in val.keys():
        # hav = cv2.blur(hav, [9,9])
        lower1 = np.array(val[k][0])
        lower2 = np.array(val[k][2])
        upper1 = np.array(val[k][1])
        upper2 = np.array(val[k][3])
        mask1 = cv2.inRange(hav, lower1, upper1)
        mask2 = cv2.inRange(hav, lower2, upper2)
        mask=mask1+mask2
        kern1 = np.ones((5, 5), np.uint8)
        kern2 = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kern2)
        mask = cv2.dilate(mask, kern1)
        imggreen = cv2.bitwise_and(img, img, mask)
        imggreen[mask == 0] = (255, 255, 255)
        mask = cv2.GaussianBlur(mask, (3,3),0)
        img2=img.copy()
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if cv2.contourArea(cnt)>100:
                ep = 0.048 * cv2.arcLength(cnt, True) - 0.3
                app = cv2.approxPolyDP(cnt, ep, True)
                x, y, w, h = cv2.boundingRect(app)
                cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
                pt = tuple(cnt[cnt[:, :, 1].argmin()][0])
                pl = tuple(cnt[cnt[:, :, 0].argmin()][0])
                pr = tuple(cnt[cnt[:, :, 0].argmax()][0])
                pb = tuple(cnt[cnt[:, :, 1].argmax()][0])
                cv2.circle(img2,pl,3,(255,0,0),-1)
                cv2.circle(img2,pt,3,(0,255,0),-1)
                cv2.circle(img2,pr,3,(0,0,255),-1)
                cv2.circle(img2,pb,3,(255,255,255),-1)
                # cv2.imshow(k, img2)
                print(k," **********")
                print("Coords: ",[x+w/2,y+h/2])
                print("Points: ",len(app))
                # print(pt,pb)
                if k=="Green":
                    print(pt,pb,pl,pr)
                    if abs(pt[0]-pb[0])<15 and (pr[0]-pt[0]<pt[0]-pl[0]):
                       if (dist(pt,pr)<15 or dist(pb,pr)<15):
                         to_sort.append([x+w/2,"GC"])
                       else:
                          to_sort.append([x+w/2,"RA"])
                    elif abs(pt[0]-pb[0])<15 and (pr[0]-pt[0]>pt[0]-pl[0]):
                        to_sort.append([x+w/2,"LA"])
                if k=="Red":
                    print(pt,pb,pl,pr)
                    if (dist(pt,pr)<15 or dist(pb,pr)<15):
                         to_sort.append([x+w/2,"RC"])
                    else:
                      if abs(pl[1]-pr[1])<15 and (pb[1]-pr[1]>pr[1]-pt[1]):
                          to_sort.append([x+w/2,"TA"])
                      elif abs(pl[1]-pr[1])<15 and (pb[1]-pr[1]<pr[1]-pt[1]):
                        to_sort.append([x+w/2,"DA"])
                if k=="SpecialRed":
                    if(len(app)==3):
                        to_sort.append([x,"ST"])
                    elif(len(app)==4):
                        to_sort.append([x,"SS"])
                    else:
                        to_sort.append([x,"SC"])
                if k == "YellowChand": to_sort.append([x,"YC"])
                if k == "BlueChand": to_sort.append([x,"BC"])
                if k == "PinkiSquare": to_sort.append([x,"PS"])
                if k == "BlueSquare": to_sort.append([x,"BS"])
        # cv2.waitKey(10000)
    to_sort.sort()
    print(to_sort)
    ans=""
    for k in to_sort:
        ans+=st[k[1]]
    return ans


# img=cv2.imread('/home/sandeepan/catkin_ws/src/Labyrinth-Practice-ROS-Package/spy/src/images/image1.png')
# ans=decode(img)
# ans2=ans.split(',')
# print(ans2)
# print(ans2[0])
# print(ans2[1])
    