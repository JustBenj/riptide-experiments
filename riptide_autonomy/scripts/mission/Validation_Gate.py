#!/usr/bin/env python
import smach
import smach_ros
import rospy
import robosub
from riptide_constants import RiptideConstants
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

#Validation Gate State
class Validation_Gate_ST(smach.State):
    state_image = None
    overlay_pub = None
    command_pub = None
    bridge = CvBridge()

    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'])
        rospy.init_node("Validation_Gate_ST", anonymous=True)
        self.subscriber = rospy.Subscriber("/sim_view", Image, self.imageCallback, queue_size = 1)
        self.overlay_pub = rospy.Publisher("/output", Image, queue_size = 1)
        self.command_pub = rospy.Publisher("/command/command", String, queue_size = 1)

    def imageCallback(self,image_data):
        #print("ApproachGate: Received image message")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
            self.state_image = cv_image
        except CvBridgeError, e:
            print e

    def approach(self):
        self.command_pub.publish(RiptideConstants.COMMAND_TRANSLATE_X_POS)

    def align(self):
        max_y_error = 1
        max_z_error = 1
        max_theta_error = 0.5

        if self.state_image is not None:
            overlay = self.state_image.copy()
            (y, z, theta) = robosub.findGate(self.state_image.copy(), None, None, True, overlay, True)
            self.overlay_pub.publish(self.bridge.cv2_to_imgmsg(overlay, "bgr8"))
            print (-y)
            print (z)
            print (theta)
            print ("\n")
            # TODO: Potential infinite loop. Add timeout or something....!
            #TODO: If can't see anything, return outcome of failure

            #Y values are flipped.. (Y = -Y)
            if y is not None and y >= max_y_error:
                self.command_pub.publish(RiptideConstants.COMMAND_TRANSLATE_Y_POS)
                print "Translate +Y"
            elif y is not None and y < -max_y_error:
                self.command_pub.publish(RiptideConstants.COMMAND_TRANSLATE_Y_NEG)
                print "Translate -Y"
            elif z is not None and z > max_z_error:
                self.command_pub.publish(RiptideConstants.COMMAND_TRANSLATE_Z_NEG)
                print "Translate -Z"
            elif z is not None and z < -max_z_error:
                self.command_pub.publish(RiptideConstants.COMMAND_TRANSLATE_Z_POS)
                print "Translate +Z"
            elif theta is not None and theta > max_theta_error:
                self.command_pub.publish(RiptideConstants.COMMAND_ROTATE_Z_CCW)
                print "Rotate -Z (CCW)"
            elif theta is not None and theta < -max_theta_error:
                self.command_pub.publish(RiptideConstants.COMMAND_ROTATE_Z_CW)
                print "Rotate +Z (CW)"
            # It should be impossible for theta to be None at this point
            elif theta is not None:
                return True

            return False

    def execute(self, userdata):
        rateInt = 10
        rate = rospy.Rate(rateInt)
        timer = 0
        approachTimeout =  3 * rateInt #seconds * rate
        isAligned = False

        #Run code to move through validation gate

        while not rospy.is_shutdown():
            if (timer < approachTimeout):
                self.approach()
            elif not isAligned:
                isAligned = self.align()
            else:
                self.approach()
                print("Aligned, approach")

            timer += 1;
            rate.sleep();
        #Then return outcome
        return 'proceed_ML'

#Validation Gate State Machine
class Validation_Gate_SM(smach.StateMachine):


    def __init__(self):

        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])

        #Add states
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
