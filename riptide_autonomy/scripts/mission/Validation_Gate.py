#!/usr/bin/env python
import smach
import smach_ros
import rospy
import robosub
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

state_image = None
overlay_pub = None
bridge = CvBridge()

#Part of Validation_Gate_SM
class Validation_Gate_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'])
        self.subscriber = rospy.Subscriber("/sim_view", Image, self.imageCallback, queue_size = 1)
        overlay_pub = rospy.Publisher("/output", Image, queue_size = 1)
   
    def imageCallback(self,image_data):
        if not isActive:
            return
        #rospy.loginfo("ApproachGate: Received image message")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
            state_image = cv_image
        except CvBridgeError, e:
            print e


    def execute(self, userdata):
        #Run code to move through validation gate
        while 1:
            if state_image is not None:
                overlay = state_image.copy()
                robosub.findGate(state_image.copy(), None, None, True, overlay)

                pub.publish(bridge.cv2_to_imgmsg(overlay, "bgr8"))

        #Then return outcome
        return 'proceed_ML'

class Validation_Gate_SM(smach.StateMachine):


    def __init__(self):

        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
