#!/usr/bin/env python3
from pickletools import uint8
import rospy
import actionlib
import sys
import cv2
import cv2.aruco as aruco
from coordi_msgs.msg import coordi
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from std_msgs.msg import Int8
import spycode as sp

img=Image()
bridge=CvBridge()
def img_call(data):
    global img 
    try:
     img = bridge.imgmsg_to_cv2(data, "bgr8")
     return img
    except CvBridgeError as e:
      print(e)

rospy.init_node("mynode")
arcpub=rospy.Publisher('/aruco',Int8,queue_size=1,latch=True)
rospy.Subscriber('/camera/color/image_raw',Image,img_call,queue_size=1)
navclient=actionlib.SimpleActionClient('move_base',MoveBaseAction)
navclient.wait_for_server()
goal=MoveBaseGoal()

def active_cb():
  rospy.loginfo("Goal being processed")
def feedback_cb(feedback):
#  rospy.loginfo("Current="+str(feedback))
  pass
def done_cb(status,result):
  if status==3:
     rospy.loginfo("Goal reached")
  elif status==2 or status==8:
     rospy.loginfo("Goal cancelled")
  elif status==4:
     rospy.loginfo("Goal aborted")

def findArucoMarkers(img, markerSize = 4, totalMarkers=1000, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    aruco.drawDetectedMarkers(img, corners)
    cv2.imshow("img",img)
    cv2.waitKey(3000)
    return ids[0][0]

def get_img():
   
   data = rospy.wait_for_message("/camera/color/image_raw",Image)
   try:
     img = bridge.imgmsg_to_cv2(data, "bgr8")
     return img
   except CvBridgeError as e:
      print(e)

def move(gx,gy,ox,oy,oz,ow):
 goal.target_pose.pose.position.x = gx
 goal.target_pose.pose.position.y = gy
 goal.target_pose.pose.orientation.z = oz
 goal.target_pose.pose.orientation.x = ox
 goal.target_pose.pose.orientation.y = oy
 goal.target_pose.pose.orientation.w = ow
 navclient.send_goal(goal,done_cb,active_cb,feedback_cb) 
 finished=navclient.wait_for_result()

 if not finished:
  rospy.logerr("Action server not avalaible")
  sys.exit()
 else:
  rospy.loginfo(navclient.get_result())


goal.target_pose.header.seq = 1
goal.target_pose.header.stamp = rospy.Time.now()
goal.target_pose.header.frame_id = "map"
goal.target_pose.pose.orientation.x = 0.0
goal.target_pose.pose.orientation.y = 0.0

def total():
  #  img=get_img()
   cv2.imshow('img1',img)
   cv2.waitKey(3000)
   cv2.destroyAllWindows()
   id=findArucoMarkers(img)
   print("Publishing",id)
   arcpub.publish(id)
   arcpub.publish(id)
   arcpub.publish(id)
   arcpub.publish(id)
   tl=rospy.wait_for_message("/terrorist_location",coordi)
   ori=tl.orientation
   print(tl.orientation)
   flatimg=np.array(tl.image)
   img3=flatimg.reshape(379,1049,3)
   img3=img3.astype(np.uint8)
  #  cv2.imshow('reshaped',img3)
   ans=sp.decode(img3)
   coor=ans.split(',')
   print(coor)
   print("About to move")
   move(float(coor[0]),float(coor[1]),ori[0],ori[1],ori[2],ori[3])
try:
   rospy.sleep(1)
   total()
   total()
except KeyboardInterrupt:
    print("Shutting down")
