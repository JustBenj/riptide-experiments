#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Part of Path_Marker_SM
class Path_Marker_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['proceed_ML'],
                            input_keys=['set_sail_status', 'navigate_pass_status'])

    def execute(self, userdata):
        #Run code to follow path marker towards next task


        #Then return outcome
        return 'proceed_ML'

class Path_Marker_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['set_sail', 'navigate_pass'])
        self.userdata.set_sail_status
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                                transitions={'proceed_ML':'proceed_HL'})
