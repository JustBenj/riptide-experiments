#!/usr/bin/env python

import rospy
import smach
import smach_ros
from Validation_Gate import *

def main():
    #High Level state machine
    mission_sm = smach.StateMachine(outcomes=['succeeded_MS','failed_MS'])

    #Userdata:
    #Status of certain tasks (needed for Path_Marker_SM and Pinger_SM)
    mission_sm.userdata.set_sail_status = 0;
    mission_sm.userdata.navigate_pass_status = 0;
    mission_sm.userdata.squid_status = 0;
    mission_sm.userdata.cultivate_pearls_status = 0;
    mission_sm.userdata.collect_and_classify_status = 0;

    with mission_sm:
        # mission_sm.StateMachine.add('INITIALIZE', Initialize(),
        #                         transitions={'proceed_HL':'VALIDATION_GATE_SM'})
        smach.StateMachine.add('VALIDATION_GATE_SM', Validation_Gate_SM(),
                                 transitions={'proceed_HL':'succeeded_MS'})
        mission_sm.StateMachine.add('PATH_MARKER_SM', Path_Marker_SM,
                                transitions={'set_sail':'SET_SAIL_SM',
                                            'navigate_pass':'NAVIGATE_PASS_SM'},
                                remapping={'set_sail_status':'set_sail_status',
                                            'navigate_pass_status':'navigate_pass_status'})
        mission_sm.StateMachine.add('SET_SAIL_SM', Set_Sail_SM,
                                transitions={'proceed_HL':'PATH_MARKER_SM',
                                            'misaligned_HL':'PATH_MARKER_SM'})
        # mission_sm.StateMachine.add('NAVIGATE_PASS_SM', NAVIGATE_PASS_SM,
        #                         transitions={'proceed_HL':'PINGER_SM',
        #                                     'misaligned_HL':'PATH_MARKER_SM'})
        # mission_sm.StateMachine.add('PINGER_SM', Pinger_SM,
        #                         transitions={'squid_pearls':'BATTLE_A_SQUID_SM',
        #                                     'collect_and_classify':'COLLECT_AND_CLASIFY_SM'})
        # mission_sm.StateMachine.add('BATTLE_A_SQUID_SM', Battle_A_Squid_SM,
        #                         transitions={'proceed_HL':'PINGER_SM',
        #                                     'proximity_far_HL':'PINGER_SM'})
        # mission_sm.StateMachine.add('CULTIVATE_PEARLS_SM', Cultivate_Pearls_SM,
        #                         transitions={'proceed_HL':'PINGER_SM',
        #                                     'proximity_far_HL':'PINGER_SM'})
        # mission_sm.StateMachine.add('COLLECT_AND_CLASIFY_SM', Collect_And_Classify_SM,
        #                         transitions={'proximity_far_HL':'PINGER_SM',
        #                                     'end_of_mission_HL':'succeeded_MS',
        #                                     'failed_HL':'failed_MS'})
    outcome = mission_sm.execute()


if __name__ == '__main__':
    main()
