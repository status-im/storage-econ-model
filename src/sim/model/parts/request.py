import networkx as nx
import numpy as np
from .message import message_list_updater

from ..utils import *

def p_new_message(params, substep, state_history, prev_state):
    '''
    New message creation.
    In the format: [message id (hash), size, frequency]
    Message size created by random integer 1-100
    Token commitment random for now, to be updated with informed models
    '''
    new_message_size = np.random.randint(1,100)
    value = [id(new_message_size), new_message_size, 1]
    # commitment in tokens
##########################################################################################
    # random for now, MAKE as DECISION by ENTITY INFORMED by SYSTEM
   
    message_token = float(new_message_size)  * float(params['message_base_cost']) * float(np.abs(np.random.normal(1,params['utility_cost_volatility'])))
    storage_token = float(new_message_size) * float(params['storage_base_cost'])

    token = int(message_token + storage_token)
##########################################################################################    
    return {'new_event': value, 'commitment': token}
    
def s_new_message(params, substep, state_history, prev_state, policy_input):
    key = 'message_arrival'
    new_message_size = np.random.randint(1,100)
    value = [id(new_message_size), new_message_size, 1]
    # Not used
    # new_event = Event(size =new_message_size, hash_file= id(new_message_size),block_init= prev_state['timestep'])
    # new_event.initiate(size =new_message_size, hash_file= id(new_message_size),block_init= prev_state['timestep'])
    # prev_state['history'].add_to_active(new_event)
    return (key, value)


# only for testing
def s_mirror_message(params, substep, state_history, prev_state, policy_input):
    '''
    Testing of new message event
    '''
    key = 'mirror'
    print(policy_input)
    value = policy_input['new_event'] 
    return (key, value)


def s_network_request(params, substep, state_history, prev_state, policy_input):
    '''
    Tokens removed from requester wallet
    ORIGINAL REQUIREMENT. NOW tokens are removed from wallet upon posting of batched proven routes.
    '''
    key = 'network'
    value = prev_state['network']
    tokens = policy_input['commitment']
    # convert to array for subtracting commitment amount
    wallet = np.array(value.nodes['i']['wallet'])
    wallet -= tokens
    value.nodes['i']['wallet'] = wallet
    return (key, value)


def s_event(params, substep, state_history, prev_state, policy_input):
    '''
    Message event created from p_new_message policy message size, message file, block at initialization, escrowed token amount.
    '''
    key = 'event'
    event = policy_input['new_event'] 
    token = policy_input['commitment'] 
    value = Event(size =event[1], hash_file= event[0] ,block_init= prev_state['timestep'], escrow = token)
    
    # new_message_size = np.random.randint(1,100)
    # new_message = [id(new_message_size), new_message_size, 1]
    # value.initiate(size =event[1], hash_file= event[0] ,block_init= prev_state['timestep'])  
    return (key, value)

def s_history_active(params, substep, state_history, prev_state, policy_input):
    '''
    History active list updated with activated event.
    '''
    key = 'history'
 
    prev_state['history'].add_to_active(prev_state['event'])
    value = prev_state['history']
    return (key, value)