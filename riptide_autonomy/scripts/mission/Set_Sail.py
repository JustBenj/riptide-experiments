#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Set Sail State
class Set_Sail_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['proceed_ML']
                            output_keys=['set_sail_status_ST'])

    def execute(self, userdata):
        #Run code to move through set sail


        #Update set_sail_status_sm, return outcome to lead towards Path Marker
        userdata.set_sail_status_ST = 1
        return 'proceed_ML'

#Set Sail State Machine
class Set_Sail_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['proceed_HL'])

        #Add states
        with self:
            smach.StateMachine.add('SET_SAIL_ST', Set_Sail_ST(),
                            transitions={'proceed_ML':'proceed_HL'})
