import networkx as nx
from ..utils import *

def init_node_i(params, substep, state_history, prev_state, policy_input):
    '''
    Initialize new id, distance, routing table for each monte carlo run in the network.
    '''
    key = 'network'
    ij = prev_state['network']
    if prev_state['timestep'] == 0:
        for node in ij:
            ij.nodes[str(node)]['id']  = np.random.randint(0,16)

        # ROUTING TABLE INITIALIZATION
        ij.nodes['i']['routing_table'] = []
        ij.nodes['j']['routing_table'] = []
        ij.nodes['k']['routing_table'] = []
        ij.nodes['p']['routing_table'] = []
        ij.nodes['r']['routing_table'] = []

        ij.nodes['i']['routing_table'] = route_table(ij, 'i')
        ij.nodes['j']['routing_table'] = route_table(ij, 'j')
        ij.nodes['k']['routing_table'] = route_table(ij, 'k')
        ij.nodes['p']['routing_table'] = route_table(ij, 'p')
        ij.nodes['r']['routing_table'] = route_table(ij, 'r')

    value = ij
    return (key, value)

# Not used, taken care of in config.py for loop
def s_init_treasury(params, substep, state_history, prev_state, policy_input):
    '''
    Initialize starting treasury
    '''
    key = 'treasury'
    value = prev_state['treasury']
    if prev_state['timestep'] == 0:
        initial_tokens = params['starting_treasury']
        value += initial_tokens
    else:
        initial_tokens = 0
        value = prev_state['treasury']
 
    return (key, value)
