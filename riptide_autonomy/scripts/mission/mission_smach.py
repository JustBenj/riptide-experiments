#!/usr/bin/env python

import rospy
import smach
import smach_ros
from riptide_constants import RiptideConstants
from Validation_Gate import *
#from Set_Sail import *
#from Navigation_Pass import *
from Pinger import *

def main():
    #High Level state machine
    mission_sm = smach.StateMachine(outcomes=['succeeded_MS','failed_MS'])

    #Userdata:
    #Status of certain tasks (needed for Path_Marker_SM and Pinger_SM)
    #0 = not completed, 1 = completed
    mission_sm.userdata.set_sail_status_SM = 0;
    mission_sm.userdata.navigate_pass_status_SM = 0;
    mission_sm.userdata.squid_status_SM = 0;
    mission_sm.userdata.pearl_status_SM = 0;
    mission_sm.userdata.collect_status_SM = 0;

    with mission_sm:
        # mission_sm.StateMachine.add('INITIALIZE', Initialize(),
        #                         transitions={'proceed_HL':'VALIDATION_GATE_SM'})
        smach.StateMachine.add('VALIDATION_GATE_SM', Validation_Gate_SM(),
                    transitions={'proceed_HL':'succeeded_MS'})

        #smach.StateMachine.add('PATH_MARKER_SM', Path_Marker_SM(),
        #            transitions={'set_sail_HL':'SET_SAIL_SM',
        #                        'navigate_pass_HL':'NAVIGATE_PASS_SM'},
        #            remapping={'set_sail_status_ST':'set_sail_status_SM'})

        #smach.StateMachine.add('SET_SAIL_SM', Set_Sail_SM(),
        #            transitions={'proceed_HL':'PATH_MARKER_SM'},
        #           remapping={'set_sail_status_ST':'set_sail_status_SM'})

        #smach.StateMachine.add('NAVIGATE_PASS_SM', NAVIGATE_PASS_SM(),
        #            transitions={'proceed_HL':'PINGER_SM'},
        #            remapping={'navigate_pass_status_ST':'navigate_pass_status_SM'})

        #smach.StateMachine.add('PINGER_SM', Pinger_SM,
        #            transitions={'battle_a_squid_HL':'BATTLE_A_SQUID_SM',
        #                        'cultivate_pearls_HL': 'CULTIVATE_PEARLS_SM',
        #                        'collect_and_classify_HL':'COLLECT_AND_CLASIFY_SM'},
        #            remapping={'squid_status_ST':'squid_status_SM',
        #                        'pearl_status_ST':'pearl_status_SM',
        #                        'collect_status_ST':'collect_status_SM'})

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
    
    rospy.set_param("constants/LINEAR_X_ACCEL", RiptideConstants.LINEAR_X_ACCEL)
    rospy.set_param("constants/LINEAR_Y_ACCEL", RiptideConstants.LINEAR_Y_ACCEL)
    rospy.set_param("constants/LINEAR_Z_ACCEL", RiptideConstants.LINEAR_Z_ACCEL)

    rospy.set_param("constants/ANGULAR_X_ACCEL", RiptideConstants.ANGULAR_X_ACCEL)
    rospy.set_param("constants/ANGULAR_Y_ACCEL", RiptideConstants.ANGULAR_Y_ACCEL)
    rospy.set_param("constants/ANGULAR_Z_ACCEL", RiptideConstants.ANGULAR_Z_ACCEL)

    rospy.set_param("constants/COMMAND_TRANSLATE_X_POS", RiptideConstants.COMMAND_TRANSLATE_X_POS)
    rospy.set_param("constants/COMMAND_TRANSLATE_Y_POS", RiptideConstants.COMMAND_TRANSLATE_Y_POS)
    rospy.set_param("constants/COMMAND_TRANSLATE_Z_POS", RiptideConstants.COMMAND_TRANSLATE_Z_POS)
    
    rospy.set_param("constants/COMMAND_ROTATE_X_CW", RiptideConstants.COMMAND_ROTATE_X_CW)
    rospy.set_param("constants/COMMAND_ROTATE_Y_CW", RiptideConstants.COMMAND_ROTATE_Y_CW)
    rospy.set_param("constants/COMMAND_ROTATE_Z_CW", RiptideConstants.COMMAND_ROTATE_Z_CW)

    rospy.set_param("constants/COMMAND_TRANSLATE_X_NEG", RiptideConstants.COMMAND_TRANSLATE_X_NEG)
    rospy.set_param("constants/COMMAND_TRANSLATE_Y_NEG", RiptideConstants.COMMAND_TRANSLATE_Y_NEG)
    rospy.set_param("constants/COMMAND_TRANSLATE_Z_NEG", RiptideConstants.COMMAND_TRANSLATE_Z_NEG)

    rospy.set_param("constants/COMMAND_ROTATE_X_CCW", RiptideConstants.COMMAND_ROTATE_X_CCW)
    rospy.set_param("constants/COMMAND_ROTATE_Y_CCW", RiptideConstants.COMMAND_ROTATE_Y_CCW)
    rospy.set_param("constants/COMMAND_ROTATE_Z_CCW", RiptideConstants.COMMAND_ROTATE_Z_CCW)

    main()
