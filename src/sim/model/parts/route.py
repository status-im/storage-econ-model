import networkx as nx
import numpy as np
from .message import message_list_updater
from ..utils import *

def p_send_kj(params, substep, state_history, prev_state):
    """
    Constraint check for ability to route stored message from k to j
    """
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

# used for testing
def sent_list(params, substep, state_history, prev_state, policy_input):
    """
    Testing of sent message
    """
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
    Using PO in routing table, select closest node (excluding self) in routing table
    """
    PO_list = [row[4] for row in network.nodes[sending_node]['routing_table']]
    # need to select closest node that has second max to disregard self
    third = PO_list[2]
    first_max = max(PO_list[0],PO_list[1])
    print('first max', first_max)
    second_max=min(PO_list[0],PO_list[1]) 
    print('second max', second_max)
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
    print('receiving node from func', receiving_node)
    if receiving_node[0][0] == sending_node:
        print('triggered')
        closest_node = PO_list.index(third)
        receiving_node = network.nodes[sending_node]['routing_table'][closest_node]
        print('receiving node from func', receiving_node)
    # receiving node name [0]
    return receiving_node[0]

def s_send_k_to_closest(params, substep, state_history, prev_state, policy_input):
    """
    Route stored message from k to j via nodes in routing table
    """
    key = 'network'
    value = prev_state['network']

    # Route Receive from k to closest
    receiving_node_name = send_closest(value, 'k')

    # INCOMING Messages Subject to inbound constraint
    in_constraint = np.array(prev_state['network'].nodes[receiving_node_name]['inband'])

    # CONVERT TO SWEEP OF ALL INCOMING NODES TO J (NEED TO EITHER SWITCH TO MULTI GRAPH)
    # INBOUND EDGES FROM I AND K = inbound bandwidth to j
    in_traffic = inbound_traffic(value.adj['k'], receiving_node_name) #+ inbound_traffic(value.adj['k'], receiving_node_name)
    current_store_j = value.nodes[receiving_node_name]['current_capacity']
    new_storage_j = current_store_j + policy_input['message_from_k'][1]
    constraint_j = prev_state['network'].nodes[receiving_node_name]['storage_capacity']
    existing_message_list_j = prev_state['network'].nodes[receiving_node_name]['message_history']
    # Not needed in forwarding because receiving node determined 
    # if policy_input['message_to_via_i'] == 'j':
    # message_traffic = policy_input['message_from_i'][1]
    
    if in_traffic + policy_input['message_from_k'][1] < in_constraint:
        # print("if route yes")
        if new_storage_j <= constraint_j[0]:
            # value.nodes['j']['current_capacity'] = new_storage_j
            # print('receive from k', receiving_node_name)
            receiving_node_name = 'j'
            value.nodes[receiving_node_name]['message_history'] = message_list_updater(existing_message_list_j, policy_input['message_from_k'])
            value['k'][receiving_node_name]['traffic'] = prev_state['message_arrival'][1]
            value.nodes[receiving_node_name]['neighbor_estimate']['messages from k'] += 1 #policy_input['new_message_size']

    return (key, value)    

def s_history_routed(params, substep, state_history, prev_state, policy_input):
    """
    Located files that have completed routing are updated with block of completion. In the history, messages are added to routed list and removed from the active list.
    """
    key = 'history'
 
    if len(prev_state['history'].located) > 5:
        temp = prev_state['history'].located[-3]
        temp.complete(block_route=prev_state['timestep'])
        prev_state['history'].add_to_routed(temp)


    value = prev_state['history']
    return (key, value)