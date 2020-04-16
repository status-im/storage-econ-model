import networkx as nx
import numpy as np
from .message import message_list_updater

from ..utils import *

def demand_function(params, substep, state_history, prev_state):
    """
    Policy for generating new demand for file storage.
    """
    
    new_message_size = np.random.randint(1,200)
    new_message = [id(new_message_size), new_message_size, 1]

    return {'new_message': new_message, 'new_message_size': new_message_size}


def demand_current(params, substep, state_history, prev_state, policy_input):
    """
    State for tracking demand policy.
    """
    key = 'demand'
    # value = prev_state[key]
    value = policy_input['new_message']
    return (key, value)


def arrival_function(params, substep, state_history, prev_state):
    """
    Policy for generating new arrival for node participation.
    """

    new_message_size = np.random.randint(1,100)
    new_message = [id(new_message_size), new_message_size, 1]

    return {'new_arrival': new_message, 'new_arrival_size': new_message_size}


def arrival_current(params, substep, state_history, prev_state, policy_input):
    """
    State for tracking arrival policy.
    """
    key = 'arrival'
    # value = prev_state[key]
    value = policy_input['new_arrival']
    return (key, value)

