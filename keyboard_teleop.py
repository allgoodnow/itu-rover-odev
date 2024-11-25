#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard
#kutuphaneler

linear_velocity = 0.0
angular_velocity = 0.0
#robotun hareketinde kullanılacak degiskenler

def publish_velocity():
    twist = Twist()
    twist.linear.x = linear_velocity
    twist.angular.z = angular_velocity
    pub.publish(twist)
#robotun hareketini bildiren fonksiyon

def on_press(key):
    global linear_velocity, angular_velocity
    try:
        if key.char == 'w':
            linear_velocity += 0.2
            rospy.loginfo("going forward")
        elif key.char == 's':
            linear_velocity -= 0.2
            rospy.loginfo("going backwards")
        elif key.char == 'a':
            angular_velocity += 0.1
            rospy.loginfo("turning left")
        elif key.char == 'd':
            angular_velocity -= 0.1
            rospy.loginfo("turning right")
        elif key.char == 'x':
            linear_velocity = 0.0
            angular_velocity = 0.0
            rospy.loginfo("movement stopped")
    except AttributeError:
        pass
    publish_velocity()
#pynput ile key pressleri alip robotun hareketini saglayan bolum

def timer_callback(_):
    rospy.loginfo("60 seconds elapsed, shutting down")
    rospy.signal_shutdown("60 seconds elapsed")
#60sn gectikten sonra node'u kapatan fonksiyon

if __name__ == '__main__':
    rospy.init_node('keyboard_teleop_node')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.loginfo("keyboard teleop node has started")

    rospy.Timer(rospy.Duration(60), timer_callback, oneshot=True)
    #timer

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    #keyboard inputlarini dinleyen fonksiyon

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
    #rospy.spin'i kullandigimda looptan cikmiyordu be sekilde sorun cozuldu