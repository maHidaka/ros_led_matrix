#! /usr/bin/env python
# -*- coding: utf-8 -*-

from click import edit
import rospy
import yaml
import sys
import roslib.packages

from std_msgs.msg import String

import time

class BaseNode():
    def __init__(self):
        self.pkg_name = 'ros_led_matrix_controll'
        self.import_yaml()
        self.pub = rospy.Publisher('/test2', String, queue_size=1)

    def import_yaml(self):
        
        try:
            with open(roslib.packages.get_pkg_dir(self.pkg_name)+'/config.yaml') as yml:
                config = yaml.safe_load(yml)
            rospy.loginfo('load config.yaml')
            rospy.loginfo(config)
            if(config['style']=='single'):
                if(config['disp1']['type']=='topic'):
                    type = globals()[config['disp1']['trigger']['topic_type']]
                    rospy.loginfo('trig1 attached topic: '+config['disp1']['trigger']['topic_name'])
                    self.sub = rospy.Subscriber(config['disp1']['trigger']['topic_name'], type, self.callback1)

                elif(config['disp1']['type']=='service'):
                    rospy.loginfo('trig1 is service')

                else:
                    rospy.logerr('Unexpected value specified at "config.yaml disp1 type"')

        except Exception as e:
            rospy.logerr('Exception occurred while loading YAML...')
            rospy.signal_shutdown('Error')

            

        
    

    def callback1(self, data):
        self.publish(data)

    def publish(self, data):
        self.pub.publish(data)


if __name__ == '__main__':
    rospy.init_node('base_node')

    time.sleep(3.0)
    node = BaseNode()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)