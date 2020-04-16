import numpy as np

from ..utils import *

def m_gross_storage(params, substep, state_history, prev_state, policy_input):
    '''
    Metric for computing the gross sum of message history sizes.
    Upper bound of every message taking up storage on every node.
    '''
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
    '''
    Metric for computing the least possible amount of message history sizes.
    Lower bound of only 1 node stores each file.
    '''
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


def m_transit(params, substep, state_history, prev_state, policy_input):
    '''
    Metric for computing the tokens locked in escrow.
    Uses starting tokens contained in node i and the treasury account as the initial amount.
    Node wallets (not i) are subtracted from this amount.
    '''
    key = 'transit'

    network = prev_state['network']
    running_wallet_sum = 0

    for node in network:
        node_wallet =  np.array(network.nodes[str(node)]['wallet'], dtype = 'float')
  
        running_wallet_sum += node_wallet
    
    treasury = prev_state['treasury']

    locked = treasury + running_wallet_sum
    locked = locked[0]
    starting_value = params['i_wallet'] + params['starting_treasury']
    value = starting_value - locked

    return (key, value)