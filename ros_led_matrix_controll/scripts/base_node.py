#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from click import edit
import rospy
import yaml
import sys
import roslib.packages

from std_msgs.msg import *
from geometry_msgs.msg import *
import time

class BaseNode():
    def __init__(self):
        self.pkg_name = 'ros_led_matrix_controll'
        self.import_config()
        self.pub = rospy.Publisher('/pub', String, queue_size=1)

    def import_config(self):
        try:
            with open(roslib.packages.get_pkg_dir(self.pkg_name)+'/config.yaml') as yml:
                config = yaml.safe_load(yml)
            rospy.loginfo('load config.yaml')
            #rospy.loginfo(config)
            contents_num = len(config)
        #     if(style=='single'):
        #         type = config['disp1']['type']
        #         if(type=='topic'):
        #             topic_type = globals()[config['disp1']['trigger']['topic_type']]
        #             topic_name = config['disp1']['trigger']['topic_name']
        #             rospy.loginfo('trig1 attached topic: '+topic_name)
        #             self.sub = rospy.Subscriber(topic_name, topic_type, self.callback1)

        #         elif(type=='service'):
        #             rospy.loginfo('trig1 is service')

        #         else:
        #             rospy.logerr('Unexpected value specified at "config.yaml disp1 type"')
        #     elif(style=='multi'):
        #         a

        except Exception as e:
            rospy.logerr('Exception occurred while loading YAML...')
            rospy.signal_shutdown('Error')
        
        for i in range(contents_num):
            position = config[i]['position']
            type = config[i]['type']
            if(type == 'topic'):
                topic_name = config[i]['trigger']['topic_name']
                topic_type = globals()[config[i]['trigger']['topic_type']]
                rospy.loginfo('trigger'+str(i)+' attached topic: '+topic_name+' type: '+str(topic_type))
                if (i == 0):
                    self.sub = rospy.Subscriber(topic_name, topic_type, self.callback0)
                if (i == 1):
                    self.sub = rospy.Subscriber(topic_name, topic_type, self.callback1)

            elif(type == 'service'):
                service_name = config[i]['trigger']['service_name']
                service_type = globals()[config[i]['trigger']['service_type']]
                rospy.loginfo('trigger'+str(i)+' attached service: '+service_name)
            else:
                rospy.logerr('Unexpected value specified at "config.yaml type"')

    def callback0(self, data):
        self.publish(str(data))
        

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