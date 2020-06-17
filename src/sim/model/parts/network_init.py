import networkx as nx
from ..utils import *
from ..sys_params import sys_params

# here for now, move to sys_params later
aware = 4
peer_i = 4
peer_j = 4
peer_k = 4
peer_p = 4
aware_r = 4

# LIST VERSION
def init_control_surface(network, own_node):
    """
    Initiate trust scores for each node in network 
    [node_name , trust_score, event success rate historical, ping frequency]
    """
    # network.nodes[own_node]['control'] = []
    control = []
    for node in network:
        print(node)
        if own_node != node: 
            trust = 1        
            success = 1
            ping = 0
            control.append([node, trust, success, ping]) 

            # network.nodes[own_node]['control'].append([node, trust, success, ping]) 
        # print(node,dist)
    # return network.nodes[own_node]['control']
    print('control',control)
    return control

# DICTIONARY VERSION
def init_control_dict(network, own_node):
    """
    Initiate trust scores for each node in network 
    [node_name , trust_score, event success rate historical, ping frquency]
    """
    # network.nodes[own_node]['control'] = []
    control = {}
    for node in network:
        print(node)
        if own_node != node: 
            trust = 1        
            # success = 1
            # ping = 0
            control[node] = trust

            # network.nodes[own_node]['control'].append([node, trust, success, ping]) 
        # print(node,dist)
    # return network.nodes[own_node]['control']
    print('control',control)
    return control

def init_network():
    '''
    Initialize new id, distance, routing table for each monte carlo run in the network.
    '''
    ## Message List Initialization ###################################
    message_list = [None] *3
    message_list = [message_list]*2

    ## Network Initialization #######################################
    network = nx.DiGraph()
    # Empty List for file storage 3 x 2
    # [id, size, frequency]
    file_list =  [None] *3
    # Make send None row for dimensionality
    file_list = [file_list] * 2
    ##### Initial Memory of Stored Files
    size = 0
    # Message History Initialization 
    # # [id, size, freq] 
    message_i = message_list.copy()
    message_j = message_list.copy()
    message_k = message_list.copy()
    message_p = message_list.copy()
    message_r = message_list.copy()

    # Neighbor Estimate for each Node, neighbor_estimate
    i_est = {'j_avail_to_i': sys_params['j_avail_to_i'], 'k_avail_to_i': sys_params['k_avail_to_i'], 'p_avail_to_i': sys_params['p_avail_to_i'],'messages from k': 0, 'messages from i': 0}
    j_est = {'storage from i': 0, 'storage from k': 0, 'messages from i': 0, 'messages from k': 0}
    k_est = {'storage from i': 0,'messages from i': 0,'j_avail_to_k':  sys_params['j_avail_to_k']}
    p_est = {'messages from i': 0,'messages from k': 0}
    r_est = {'messages from i': 0,'messages from k': 0}

    # ADD NODES
    network.add_node('i', neighbor_estimate= i_est, storage_capacity=sys_params['i_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['i_in_bandwidth'],\
        outband=sys_params['i_out_bandwidth'], message_history = message_i, control=[], wallet = sys_params['i_wallet'], role = 'i')
    network.add_node('j', neighbor_estimate= j_est, storage_capacity=sys_params['j_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['j_in_bandwidth'],\
        outband=sys_params['j_out_bandwidth'], message_history = message_j, control=[], wallet = sys_params['j_wallet'], role = 'j')
    network.add_node('k', neighbor_estimate= k_est, storage_capacity=sys_params['k_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['k_in_bandwidth'],\
        outband=sys_params['k_out_bandwidth'], message_history = message_k, control=[], wallet = sys_params['k_wallet'], role = 'k')
    network.add_node('p', neighbor_estimate= p_est, storage_capacity=sys_params['p_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['p_in_bandwidth'],\
        outband=sys_params['p_out_bandwidth'], message_history = message_p, control=[], wallet = sys_params['p_wallet'], role = 'p')
    network.add_node('r', neighbor_estimate= r_est, storage_capacity=sys_params['r_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['r_in_bandwidth'],\
        outband=sys_params['r_out_bandwidth'], message_history = message_r, control=[], wallet = sys_params['r_wallet'], role = 'r')

    # ADD EDGES
    network.add_edge('i',"j")
    network.add_edge('i',"k")
    network.add_edge('i',"p")
    network.add_edge('k',"j")
    network.add_edge('k',"i")
    network.add_edge('k',"p")
    network.add_edge('j',"p")
    network.add_edge('j',"i")
    network.add_edge('j',"k")
    network.add_edge('j',"r")
    network.add_edge('k',"r")
    network.add_edge('r',"j")
    network.add_edge('i',"r")
    network.add_edge('i',"i")
    network.add_edge('r',"i")
    network.add_edge('r',"k")
    network.add_edge('r',"p")

    # Add initial history of traffic between nodes
    network['i']["j"]['traffic'] = 0
    network['i']["k"]['traffic'] = 0
    network['k']["j"]['traffic'] = 0
    network['j']["p"]['traffic'] = 0
    network['i']["p"]['traffic'] = 0
    network['k']["r"]['traffic'] = 0
    network['k']["p"]['traffic'] = 0
    network['k']["i"]['traffic'] = 0
    network['r']["j"]['traffic'] = 0
    network['i']["r"]['traffic'] = 0
    network['i']["i"]['traffic'] = 0

    # Add initial local trust estimate directed from one node to another
    network['i']["j"]['trust'] = 1
    network['i']["k"]['trust'] = 1
    network['k']["j"]['trust'] = 1
    network['j']["i"]['trust'] = 1
    network['j']["p"]['trust'] = 1
    network['j']["k"]['trust'] = 1
    network['j']["r"]['trust'] = 1
    network['i']["p"]['trust'] = 1
    network['k']["r"]['trust'] = 1
    network['k']["p"]['trust'] = 1
    network['k']["i"]['trust'] = 1
    network['r']["j"]['trust'] = 1
    network['i']["r"]['trust'] = 1
    network['i']["i"]['trust'] = 1
    network['r']["i"]['trust'] = 1
    network['r']["k"]['trust'] = 1
    network['r']["p"]['trust'] = 1
    # ROUTING TABLE INITIALIZATION

    for node in network:
        network.nodes[str(node)]['id']  = np.random.randint(0,16)   
    network.nodes['i']['routing_table'] = []
    network.nodes['j']['routing_table'] = []
    network.nodes['k']['routing_table'] = []
    network.nodes['p']['routing_table'] = []
    network.nodes['r']['routing_table'] = []

    network.nodes['i']['routing_table'] = route_table_peer(network, 'i')
    network.nodes['j']['routing_table'] = route_table_peer(network, 'j')
    network.nodes['k']['routing_table'] = route_table_peer(network, 'k')
    network.nodes['p']['routing_table'] = route_table_peer(network, 'p')
    network.nodes['r']['routing_table'] = route_table_peer(network, 'r')
    # print('in network init i', network.nodes['i']['routing_table'])

    for i in range(peer_i):
        network.add_node('k_P_'+str(i), neighbor_estimate= k_est, storage_capacity=sys_params['k_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['k_in_bandwidth'],\
            outband=sys_params['k_out_bandwidth'], message_history = message_k, control=[], wallet = sys_params['k_wallet'],  role = 'k')
        network.add_edge('i','k_P_'+str(i))
        network['i']['k_P_'+str(i)]['traffic'] = 0
        network['i']['k_P_'+str(i)]['trust'] = 1

        network.add_node('j_P_'+str(i), neighbor_estimate= j_est, storage_capacity=sys_params['j_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['j_in_bandwidth'],\
            outband=sys_params['j_out_bandwidth'], message_history = message_j, control=[], wallet = sys_params['j_wallet'], role = 'j')
        network.add_edge('k','j_P_'+str(i))
        network['k']['j_P_'+str(i)]['traffic'] = 0
        network['k']['j_P_'+str(i)]['trust'] = 1


    for node in network:
        network.nodes[str(node)]['id']  = np.random.randint(0,16)

    # # ROUTING TABLE INITIALIZATION
    # network.nodes['i']['routing_table'] = []
    # network.nodes['j']['routing_table'] = []
    # network.nodes['k']['routing_table'] = []
    # network.nodes['p']['routing_table'] = []
    # network.nodes['r']['routing_table'] = []

    # network.nodes['i']['routing_table'] = route_table(network, 'i', 'k')
    # network.nodes['j']['routing_table'] = route_table(network, 'j', 'k')
    # network.nodes['k']['routing_table'] = route_table(network, 'k', 'j')
    # network.nodes['p']['routing_table'] = route_table(network, 'p', 'j')
    # network.nodes['r']['routing_table'] = route_table(network, 'r', 'k')

    # Init Aware Set of Nodes for role i
    for i in range(aware):
        network.add_node('i_A_'+str(i), neighbor_estimate= i_est, storage_capacity=sys_params['i_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['i_in_bandwidth'],\
            outband=sys_params['i_out_bandwidth'], message_history = message_i, control=[], wallet = sys_params['i_wallet'])

        network.add_node('j_A_'+str(i), neighbor_estimate= j_est, storage_capacity=sys_params['j_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['j_in_bandwidth'],\
            outband=sys_params['j_out_bandwidth'], message_history = message_j, control=[], wallet = sys_params['j_wallet'])
        
        network.add_node('k_A_'+str(i), neighbor_estimate= k_est, storage_capacity=sys_params['k_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['k_in_bandwidth'],\
            outband=sys_params['k_out_bandwidth'], message_history = message_k, control=[], wallet = sys_params['k_wallet'])
        
        network.add_node('p_A_'+str(i), neighbor_estimate= p_est, storage_capacity=sys_params['p_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['p_in_bandwidth'],\
            outband=sys_params['p_out_bandwidth'], message_history = message_p, control=[], wallet = sys_params['p_wallet'])
        
        network.add_node('r_A_'+str(i), neighbor_estimate= r_est, storage_capacity=sys_params['r_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['r_in_bandwidth'],\
            outband=sys_params['r_out_bandwidth'], message_history = message_r, control=[], wallet = sys_params['r_wallet'])
    
    # Control Trust for all nodes
    # Node name, Local Trust Score, Event Completion, Ping
    # network.nodes['i']['control'] = init_control_surface(network, 'i')
    # network.nodes['j']['control'] = init_control_surface(network, 'j')
    # network.nodes['k']['control'] = init_control_surface(network, 'k')
    # network.nodes['p']['control'] = init_control_surface(network, 'p')
    # network.nodes['r']['control'] = init_control_surface(network, 'r')

    network.nodes['i']['control'] = init_control_dict(network, 'i')
    network.nodes['j']['control'] = init_control_dict(network, 'j')
    network.nodes['k']['control'] = init_control_dict(network, 'k')
    network.nodes['p']['control'] = init_control_dict(network, 'p')
    network.nodes['r']['control'] = init_control_dict(network, 'r')


    return network

# NOT neeeded now, Incorporated into init_network function
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
