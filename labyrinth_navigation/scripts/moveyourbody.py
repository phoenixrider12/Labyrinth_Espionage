#!/usr/bin/env python3
import rospy
import actionlib
import roslib
import sys
import cv2
import cv2.aruco as aruco
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal

rospy.init_node("mynode")
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

try:
   move(3.026603937149048,-4.435586929321289,0,0,0,1)
except KeyboardInterrupt:
    print("Shutting down")