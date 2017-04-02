#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Path Marker State
class Path_Marker_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['set_sail_ML', 'navigate_pass_ML'],
                            input_keys=['set_sail_status_ST'])

    def execute(self, userdata):
        #Run code to follow path marker towards next task
        if userdata.set_sail_status_ST == 0: #Set Sail incomplete
            #Run code to follow path marker towards Set Sail task


            #Return outcome to lead towards Set Sail task
            return 'set_sail_ML'

        else: #Set Sail completed
            #Run code to follow path marker towards Navigate Pass task


            #Return outcome to lead towards Navigate Pass task
            return 'navigate_pass_ML'

#Path Marker State Machine
class Path_Marker_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['set_sail', 'navigate_pass'])

        #Add states
        with self:
            smach.StateMachine.add('VALIDATION_GATE_ST', Validation_Gate_ST(),
                        transitions={'set_sail_ML':'set_sail_HL',
                                    'navigate_pass_ML':'navigate_pass_HL'})
