import cv2
import numpy as np

def empty(img):
    pass
cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar",600,300)
cv2.createTrackbar("hue_min","TrackBar",0,179,empty)
cv2.createTrackbar("hue_max","TrackBar",179,179,empty)
cv2.createTrackbar("sat_min","TrackBar",0,255,empty)
cv2.createTrackbar("sat_max","TrackBar",255,255,empty)
cv2.createTrackbar("val_min","TrackBar",0,255,empty)
cv2.createTrackbar("val_max","TrackBar",255,255,empty)


def find_color_range(image) :
    hav=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # _, hav = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('image',hav)
    hue_min=cv2.getTrackbarPos("hue_min","TrackBar")
    hue_max=cv2.getTrackbarPos("hue_max","TrackBar")
    sat_min=cv2.getTrackbarPos("sat_min","TrackBar")
    sat_max=cv2.getTrackbarPos("sat_max","TrackBar")
    val_min=cv2.getTrackbarPos("val_min","TrackBar")
    val_max=cv2.getTrackbarPos("sat_max","TrackBar")
    # mask_red=cv2.inRange(hav,np.array([0,50,20]),np.array([5,255,255])) //red
    lower=np.array([hue_min,sat_min,val_min])
    upper=np.array([hue_max,sat_max,val_max])
    mask_red=cv2.inRange(hav,lower,upper)
    
    cv2.imshow('red_mask',mask_red)
    # print(lower,upper)
    k = cv2.waitKey(1)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask_red, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours: 
        M = cv2.moments(c)
        if M["m00"]>500:
            print(len(get_borders(c)))
    if k==32:    
        string = input("Enter the color: ")
        print(lower,upper)
        val[string]=[[hue_min,sat_min,val_min],[hue_max,sat_max,val_max]]
    elif k==27:
        print(val)
        cv2.destroyAllWindows()
        exit()


val={
    'GreenArrow': [[ 53, 177,  155],[ 74, 255, 255]], 
    'YellowChand': [[ 27, 176,  70], [ 41, 255, 255]],
    'BlueChand': [[88, 41, 178], [137, 255, 255]],
    'RedArrow&Moon': [[0, 194, 150], [0, 255, 255]], 
    'RedSquare': [[132, 168, 115], [179, 255, 187]], 
    'GreenChand': [[44, 95, 131], [71, 186, 255]],
    'BlueSquare': [[70, 203, 134], [140, 255, 255]], 
    'SpecialRed': [[0, 220, 60], [75, 255, 150]]
}
st = {
    "RA":"0",
    "LA":"1",
    "TA":"2",
    "DA":"3",
    "GC":"4",
    "YC":"5",
    "RS":"6",
    "BC":"7",
    "RC":"8",
    "BS":"9",
    "ST":".",
    "SS":"-",
    "SC":",",
}
def get_borders(contour):
    """
    Returns the borders of a given contour.
    """
    approx = cv2.approxPolyDP(
        contour, 0.03 * cv2.arcLength(contour, True), True)
    return approx

def find_tip(points,i):
    arr=[]
    avoid=[]
    for p in points:
        val = True
        for a in arr:
            if abs(p[0][i]-a)<20:
                val = False
                avoid.append(a)
                break
        if val:
            arr.append(p[0][i])
    for a in arr:
        if(a not in avoid):
            return a

def decode(img):
    """
    Decodes a given image.
    """
    to_sort=[]
    hav=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for k in val.keys():
        # hav = cv2.blur(hav, [9,9])
        lower = np.array(val[k][0])
        upper = np.array(val[k][1])
        mask = cv2.inRange(hav, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        # mask = cv2.blur(mask, [5,5])
        # cv2.imshow(k, mask)
        # cv2.waitKey(1000)
        # cv2.destroyWindow(k)
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            M = cv2.moments(cnt)
            extTop = tuple(cnt[cnt[:, :, 1].argmin()][0])
            extLeft = tuple(cnt[cnt[:, :, 0].argmin()][0])
            extRight = tuple(cnt[cnt[:, :, 0].argmax()][0])
            extBottom = tuple(cnt[cnt[:, :, 1].argmax()][0])
            if M["m00"]>500:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                approx = get_borders(cnt)
                print(k," **********")
                print("Coords: ",[x,y])
                print("Borders: ",len(approx))
                if k=="GreenArrow":
                    if(x<find_tip(approx,0)):
                        to_sort.append([x,"RA"])
                    else:
                        to_sort.append([x,"LA"])
                if ("RedArrow" in k):
                    if (len(approx)==7):
                        if(y<find_tip(approx,1)):
                            to_sort.append([x,"DA"])
                        else:
                            to_sort.append([x,"TA"])
                    else: to_sort.append([x,"RC"])
                if k=="SpecialRed":
                    if(len(approx)==3):
                        to_sort.append([x,"ST"])
                    elif(len(approx)==4):
                        to_sort.append([x,"SS"])
                    else:
                        to_sort.append([x,"SC"])
                if k == "GreenChand": to_sort.append([x,"GC"])
                if k == "YellowChand": to_sort.append([x,"YC"])
                if k == "BlueChand": to_sort.append([x,"BC"])
                if k == "RedSquare": to_sort.append([x,"RS"])
                if k == "BlueSquare": to_sort.append([x,"BS"])
    to_sort.sort()
    print(to_sort)
    ans=""
    for k in to_sort:
        ans+=st[k[1]]
    return ans



# while True:
#     img=cv2.imread('image/final.png')
#     find_color_range(img)

img=cv2.imread('/home/sandeepan/catkin_ws/src/Labyrinth-Practice-ROS-Package/spy/src/images/image1.png')
ans=decode(img)
print(ans)
# img=cv2.imread('image/q2.png')
# decode(img)
# img=cv2.imread('image/q1.png')
# decode(img)
    