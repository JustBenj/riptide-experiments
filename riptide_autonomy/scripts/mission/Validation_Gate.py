#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Validation Gate State
class Validation_Gate_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'])

    def execute(self, userdata):
        #Run code to move through validation gate


        #Return outcome to lead towards Path Marker
        return 'proceed_ML'

#Validation Gate State Machine
class Validation_Gate_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])

        #Add states
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
