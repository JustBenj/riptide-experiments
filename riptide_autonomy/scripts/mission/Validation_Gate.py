#!/usr/bin/env python
import smach
import smach_ros
import rospy
import robosub
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#Part of Validation_Gate_SM
class Validation_Gate_ST(smach.State):
    state_image = None
    overlay_pub = None
    bridge = CvBridge()

    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'])
        rospy.init_node("Validation_Gate_ST", anonymous=True)
        self.subscriber = rospy.Subscriber("/sim_view", Image, self.imageCallback, queue_size = 1)
        self.overlay_pub = rospy.Publisher("/output", Image, queue_size = 1)

    def imageCallback(self,image_data):
        #print("ApproachGate: Received image message")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
            self.state_image = cv_image
        except CvBridgeError, e:
            print e


    def execute(self, userdata):
        rate = rospy.Rate(10)
        #Run code to move through validation gate
        while not rospy.is_shutdown():
            if self.state_image is not None:
                overlay = self.state_image.copy()
                robosub.findGate(self.state_image.copy(), None, None, True, overlay)

                self.overlay_pub.publish(self.bridge.cv2_to_imgmsg(overlay, "bgr8"))
                rate.sleep();

        #Then return outcome
        return 'proceed_ML'

class Validation_Gate_SM(smach.StateMachine):


    def __init__(self):

        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
