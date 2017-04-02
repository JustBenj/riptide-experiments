#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Part of Set_Sail_SM
class Set_Sail_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML'])

    def execute(self, userdata):
        #Run code to move through set sail


        #Then return outcome
        return 'proceed_ML'

class Set_Sail_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])
        with self:
            smach.StateMachine.add('SET_SAIL_ST', Set_Sail_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
