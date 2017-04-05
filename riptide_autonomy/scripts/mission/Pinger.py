#!/usr/bin/env python
import smach
import smach_ros
import rospy

#Pinger State
class Pinger_ST(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                    outcomes=['battle_a_squid_ML','cultivate_pearls_ML',
                                'collect_and_classify_ML'],
                    input_keys=['squid_ST','pearl_status_ST',
                                'collect_status_ST'])

    def execute(self, userdata):
        #Run code to follow pinger towards next task
        if userdata.squid_status_ST == 0: #Battle a Squid incomplete
            #Run code to follow pinger towards Battle a Squid task


            #Return outcome to lead towards Battle a Squid task
            return 'battle_a_squid_ML'

        elif userdata.pearl_status_ST == 0: #Battle a Squid complete
            #Run code to follow pinger towards Cultivate Pearls task


            #Return outcome to lead towards Cultivate Pealrs task
            return 'cultivate_pearls_ML'

        else: #Battle a Squid and Cultivate Pearls both complete
            #Run code to follow pinger towards Collect and Classify task


            #Return outcome to lead towards Collect and Classify task
            return 'collect_and_classify_ML'

#Pinger State Machine
class Path_Marker_SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['set_sail', 'navigate_pass'])

        #Add states
        with self:
            smach.StateMachine.add('PINGER_ST', Pinger_ST(),
                        transitions={'battle_a_squid_ML':'battle_a_squid_HL',
                                    'cultivate_pearls_ML':'cultivate_pearls_HL',
                                    'collect_and_classify_ML':'collect_and_classify_HL'})
