#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Navigate Pass State
class Navigate_Pass_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'],
                            output_keys=['navigate_pass_status_ST'])

    def execute(self, userdata):
        #Run code to move through navigate pass


        #Update navigate pass status return outcome to lead towards Pinger
        userdata.navigate_pass_status_ST = 1
        return 'proceed_ML'

#Navigate Pass State Machine
class Navigate_Pass_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])

        #Add states
        with self:
            smach.StateMachine.add('NAVIGATE_PASS_ST', Navigate_Pass_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
