#!/usr/bin/env python

import smach
import smach_ros
from smach import Concurrence
from mission import mission_sm
from safety import safety_sm

#Preempt all other states if Safety SM flags an emergency
def child_term_cb(outcome_map):
    if outcome_map['SAFETY_SM'] == 'emergency_HL':
        return True
    elif outcome_map['MISSION_SM'] == 'succeeded_MS' || outcome_map['MISSION_SM'] == 'failed_MS':
        return True

    return False

#input_keys or output_keys??
cc = Concurrence(outcomes = ['succeeded', 'emergency'],
                 default_outcome = 'emergency',
                 outcome_map = {'succeeded':{'MISSION_SM':'succeeded_MS'},
                                'emergency':{'MISSION_SM':'failed_MS'}
                                'emergency':{'SAFETY_SM':'emergency_HL'}})
with cc:
    Concurrence.add('SAFETY_SM', safety_sm)
    Concurrence.add('MISSION_SM', mission_sm)
