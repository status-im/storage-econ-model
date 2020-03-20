import networkx as nx
import numpy as np
from .message import message_list_updater

def outbound_traffic(node_name):
    '''
    Sweep of adjacent nodes from given node_name, sum of outbound traffic.
    Must have OUTBOUND edges defined with 'traffic' attribute from given node
    '''
    total_traffic = 0
    for nbr, eattr in node_name.items():
        # [1] just for size
        total_traffic += eattr['traffic']

    return total_traffic

def inbound_traffic(out_node_name, in_node_name):
    '''
    Sweep of adjacent nodes from one given node_name, sum of inbound traffic.
    Must have OUTBOUND edges defined with 'traffic' attribute from given node
    Convert to a sweep of all nodes, with identified inbound node.
    '''
    total_traffic = 0
    for nbr, eattr in out_node_name.items():
        # [1] just for size
        if nbr == in_node_name:
            total_traffic += eattr['traffic']

    return total_traffic

def s_new_message(params, substep, state_history, prev_state, policy_input):
    key = 'message_arrival'
    new_message_size = np.random.randint(1,100)
    value = [id(new_message_size), new_message_size, 1]
  
    return (key, value)


# SEND from i
def p_send_i(params, substep, state_history, prev_state):
    # desired outbound route size
    #policy_input['new_arrival_size']

    #total existing outbound routing to all adjacent neighbors
    outgoing_traffic = outbound_traffic(prev_state['network'].adj['i'])
    
    # constraint on outbound routing
    out_constraint = prev_state['network'].nodes['i']['outband']
    sent_node = []
    if outgoing_traffic + prev_state['message_arrival'][1] < out_constraint[0]:
        # send is possible
        sent_message = prev_state['message_arrival']
        
        for n in range(len(prev_state['network'].nodes['i']['routing_table'])):
            if prev_state['network'].nodes['i']['routing_table'][n][3] < params['depth']:
                # send 
                # send to max node 
                sent_node.append(prev_state['network'].nodes['i']['routing_table'][n][0])
    else:
        # send fails on oubound constraint
        print('Send from i fails due to upload bandwidth constraint')
        # Count of [0,0,x] messages is the number of failed messages
        sent_message = [0, 0, 1]
 
    return {'message_from_i': sent_message, 'message_to_via_i': sent_node}



def p_send_kj(params, substep, state_history, prev_state):
    # desired outbound route size
    #policy_input['new_arrival_size']

    #total existing outbound routing to all adjacent neighbors
    outgoing_traffic = outbound_traffic(prev_state['network'].adj['k'])
    sent_node = [] 
    # constraint on outbound routing
    out_constraint = prev_state['network'].nodes['k']['outband']

    if outgoing_traffic + prev_state['message_arrival'][1] < out_constraint[0]:
        # route from k to j is possible
        sent_message = prev_state['message_arrival']

        for n in range(len(prev_state['network'].nodes['k']['routing_table'])):
            if prev_state['network'].nodes['k']['routing_table'][n][3] < params['depth']:
                # send 
                # send to max node 
                sent_node.append(prev_state['network'].nodes['i']['routing_table'][n][0])
                
    else:
        # send fails on oubound constraint
        print('Send from k fails due to upload bandwidth constraint')
        # Count of [0,0,x] messages is the number of failed messages
        sent_message = [0, 0, 1]

    return {'message_from_k': sent_message,  'message_to_via_k': sent_node}

def sent_list(params, substep, state_history, prev_state, policy_input):
    key = 'test'
    # value = prev_state[key]
    messages_sent =  len(policy_input['message_to_via_i'])
    message_size = policy_input['message_from_i'][1]
    first = messages_sent * message_size
    messages_sent =  len(policy_input['message_to_via_k'])
    message_size = policy_input['message_from_k'][1]
    second = messages_sent * message_size

    value = first + second
    # value = policy_input['message_to_via_i']
    return (key, value)

# Forwarding Kademlia
def send_closest(network, sending_node):
    """
    Using PO in routing table, select closest node (excluding self)
    """
    PO_list = [row[4] for row in network.nodes[sending_node]['routing_table']]
    # need to select closest node that has second max to disregard self
    first_max = max(PO_list[0],PO_list[1])
    second_max=min(PO_list[0],PO_list[1]) 
    
    for i in range(2,len(PO_list)): 
        if PO_list[i] > first_max: 
            second_max = first_max
            first_max=PO_list[i] 
        else: 
            if PO_list[i]>second_max: 
                second_max=PO_list[i]
               
    # get position of receiving node            
    closest_node = PO_list.index(second_max)
    # gets the row in the routing table, which is the receiving node  
    receiving_node = network.nodes[sending_node]['routing_table'][closest_node]
    # receiving node name [0]
    return receiving_node[0]

def s_send_i_to_closest(params, substep, state_history, prev_state, policy_input):
    key = 'network'
    value = prev_state['network']

    # Route Receive from i to closest
    receiving_node_name = send_closest(value, 'i')
    print(receiving_node_name)
    # INCOMING Messages Subject to inbound constraint
    in_constraint = prev_state['network'].nodes[receiving_node_name]['inband']
    # CONVERT TO SWEEP OF ALL INCOMING NODES TO J (NEED TO EITHER SWITCH TO MULTI GRAPH)
    # INBOUND EDGES FROM I AND K = inbound bandwidth to j
    in_traffic = inbound_traffic(value.adj['i'], receiving_node_name) #+ inbound_traffic(value.adj['k'], receiving_node_name)
    current_store_j = value.nodes[receiving_node_name]['current_capacity']
    new_storage_j = current_store_j + policy_input['message_from_i'][1]
    constraint_j = prev_state['network'].nodes[receiving_node_name]['storage_capacity']
    existing_message_list_j = prev_state['network'].nodes[receiving_node_name]['message_history']
    # Not needed in forwarding because receiving node determined 
    # if policy_input['message_to_via_i'] == 'j':
    if in_traffic + policy_input['message_from_i'][1] < in_constraint[0]:
        # print("if route yes")
        if new_storage_j <= constraint_j[0]:
            # value.nodes['j']['current_capacity'] = new_storage_j
            value.nodes[receiving_node_name]['message_history'] = message_list_updater(existing_message_list_j, policy_input['message_from_i'])
            value['i'][receiving_node_name]['traffic'] = prev_state['message_arrival'][1]
            value.nodes[receiving_node_name]['neighbor_estimate']['messages from i'] += 1 #policy_input['new_message_size']

    return (key, value)    


def s_send_i(params, substep, state_history, prev_state, policy_input):
    key = 'network'
    value = prev_state['network']

    # Route Receive from i to j
    # INCOMING Messages Subject to inbound constraint
    in_constraint = prev_state['network'].nodes['j']['inband']
    # CONVERT TO SWEEP OF ALL INCOMING NODES TO J (NEED TO EITHER SWITCH TO MULTI GRAPH)
    # INBOUND EDGES FROM I AND K = inbound bandwidth to j
    in_traffic = inbound_traffic(value.adj['i'], 'j') + inbound_traffic(value.adj['k'], 'j')
    current_store_j = value.nodes['j']['current_capacity']
    new_storage_j = current_store_j + policy_input['message_from_i'][1]
    constraint_j = prev_state['network'].nodes['j']['storage_capacity']
    existing_message_list_j = prev_state['network'].nodes['j']['message_history']
    if policy_input['message_to_via_i'] == 'j':
        if in_traffic + policy_input['message_from_i'][1] < in_constraint[0]:
            # print("if route yes")
            if new_storage_j <= constraint_j[0]:
                # value.nodes['j']['current_capacity'] = new_storage_j
                value.nodes['j']['message_history'] = message_list_updater(existing_message_list_j, policy_input['message_from_i'])
                value['i']["j"]['traffic'] = prev_state['message_arrival'][1]
                value.nodes['j']['neighbor_estimate']['messages from i'] += 1 #policy_input['new_message_size']

    # Route Receive from i to k
    # INCOMING Messages Subject to inbound constraint
    in_constraint = prev_state['network'].nodes['k']['inband']
    # CONVERT TO SWEEP OF ALL INCOMING NODES TO k (NEED TO EITHER SWITCH TO MULTI GRAPH)
    in_traffic = inbound_traffic(value.adj['i'], 'k')
    current_store_k = value.nodes['k']['current_capacity']
    new_storage_k = current_store_k + policy_input['message_from_i'][1]
    constraint_k = prev_state['network'].nodes['k']['storage_capacity']
    existing_message_list_k = prev_state['network'].nodes['k']['message_history']

    if in_traffic + policy_input['message_from_i'][1] < in_constraint[0]:
        # print("if route yes")
        if new_storage_k <= constraint_k[0]:
            # value.nodes['k']['current_capacity'] = new_storage_k
            value.nodes['k']['message_history'] = message_list_updater(existing_message_list_k, policy_input['message_from_i'])
            value['i']["k"]['traffic'] = policy_input['message_from_i'][1]
            value.nodes['k']['neighbor_estimate']['messages from i'] += 1 #policy_input['new_message_size']

    # Route Receive from k to j
    # INCOMING Messages Subject to inbound constraint
    in_constraint = prev_state['network'].nodes['j']['inband']
    # CONVERT TO SWEEP OF ALL INCOMING NODES TO k (NEED TO EITHER SWITCH TO MULTI GRAPH)
    in_traffic = inbound_traffic(value.adj['k'], 'j')
    current_store_j = value.nodes['j']['current_capacity']
    new_storage_j = current_store_k + policy_input['message_from_i'][1]
    constraint_j = prev_state['network'].nodes['j']['storage_capacity']
    existing_message_list_j = prev_state['network'].nodes['j']['message_history']

    if in_traffic + policy_input['message_from_k'][1] < in_constraint[0]:
        # print("if route yes")
        if new_storage_j <= constraint_j[0]:
            # value.nodes['j']['current_capacity'] = new_storage_j
            value.nodes['j']['message_history'] = message_list_updater(existing_message_list_j, policy_input['message_from_k'])
            value['k']["j"]['traffic'] = policy_input['message_from_k'][1]
            value.nodes['j']['neighbor_estimate']['messages from k'] += 1 #policy_input['new_message_size']

    return (key, value)