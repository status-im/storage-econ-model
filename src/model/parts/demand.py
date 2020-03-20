import networkx as nx
import numpy as np

def demand_function(params, substep, state_history, prev_state):
    # new_message = 1
    new_message_size = np.random.randint(1,200)
    new_message = [id(new_message_size), new_message_size, 1]



    return {'new_message': new_message, 'new_message_size': new_message_size}


def demand_current(params, substep, state_history, prev_state, policy_input):
    key = 'demand'
    # value = prev_state[key]
    value = policy_input['new_message']
    return (key, value)


def arrival_function(params, substep, state_history, prev_state):
    # new_message = 1
    new_message_size = np.random.randint(1,100)
    new_message = [id(new_message_size), new_message_size, 1]

    return {'new_arrival': new_message, 'new_arrival_size': new_message_size}


def arrival_current(params, substep, state_history, prev_state, policy_input):
    key = 'arrival'
    # value = prev_state[key]
    value = policy_input['new_arrival']
    return (key, value)

