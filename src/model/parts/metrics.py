import numpy as np

from ..utils import *

def m_gross_storage(params, substep, state_history, prev_state, policy_input):
    key = 'gross_storage_demand'

    if prev_state['timestep'] > 1:
        # Filter out the none entries in the message list
        message_list = list(filter(any, prev_state['message_list'])) 
        # convert to array
        message_array = np.array(message_list)
        #print(message_array)
        # Mutltiply Message Size by Frequency in message List to get product of size*messages
        value = np.nansum(np.multiply(message_array[:,1], message_array[:,2]))

    else:
        value = 0

    return (key, value)

def m_least_storage(params, substep, state_history, prev_state, policy_input):
    key = 'least_storage_demand'

    if prev_state['timestep'] > 1:
        # Filter out the none entries in the message list
        message_list = list(filter(any, prev_state['message_list'])) 
        # convert to array
        message_array = np.array(message_list)
        #print(message_array)
        # sum of sizes of messages without repeats representing the lower bound, if every node only stored the file once
        value = np.nansum(message_array[:,1])

    else:
        value = 0

    return (key, value)

    
def m_po(params, substep, state_history, prev_state, policy_input):
    key = 'PO'

    own_bin = prev_state['network'].nodes['i']['routing_table'][0][2]
    neighbor_bin = prev_state['network'].nodes['j']['routing_table'][1][2]
    value = shared_prefix([own_bin,neighbor_bin])

    # network.nodes[own_node]['routing_table'][name, bin(id), id,  distance]
    

    return (key, value)