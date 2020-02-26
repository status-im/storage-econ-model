
from datetime import timedelta

from ...sim.sim_setup import DAYS_PER_TIMESTEP

# DAYS_PER_TIMESTEP = 1

def p_time(params, substep, state_history, prev_state):
    value = DAYS_PER_TIMESTEP
    return {'delta': value}

def s_days_passed(params, substep, state_history, prev_state, policy_input):
    key = 'days_passed'
    value = prev_state[key] + policy_input['delta']
    return (key, value)

def s_time(params, substep, state_history, prev_state, policy_input):
    key = 'timestamp'
    value = prev_state[key] + timedelta(days=policy_input['delta'])
    return (key, value)