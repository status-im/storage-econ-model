import networkx as nx
import numpy as np
from .message import message_list_updater

from ..utils import *

# SEND from i
def p_send_i(params, substep, state_history, prev_state):
    """
    Find message storage location of requested message from i via nodes in routing table
    """
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

def find_closest(network, sending_node):
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
    storing_node = network.nodes[sending_node]['routing_table'][closest_node]

    if storing_node[0][0] == sending_node:
        closest_node = PO_list.index(third)
        storing_node = network.nodes[sending_node]['routing_table'][closest_node]
    return storing_node[0]

def s_find_f(params, substep, state_history, prev_state, policy_input):
    """
    Message request finding location of file, though routing table of i
    """
    key = 'network'
    value = prev_state['network']

    # Route Receive from i to closest
    receiving_node_name = find_closest(value, 'i')

    # INCOMING Messages Subject to inbound constraint
    in_constraint = np.array(prev_state['network'].nodes[receiving_node_name]['inband'])

    # CONVERT TO SWEEP OF ALL INCOMING NODES TO k (NEED TO EITHER SWITCH TO MULTI GRAPH)
    # INBOUND EDGES FROM I AND K = inbound bandwidth to k
    in_traffic = inbound_traffic(value.adj['i'], receiving_node_name) #+ inbound_traffic(value.adj['k'], receiving_node_name)
    current_store_k = value.nodes[receiving_node_name]['current_capacity']
    new_storage_k = current_store_k + policy_input['message_from_i'][1]
    constraint_k = prev_state['network'].nodes[receiving_node_name]['storage_capacity']
    existing_message_list_k = prev_state['network'].nodes[receiving_node_name]['message_history']
    # Not needed in forwarding because receiving node determined 
    
    if in_traffic + policy_input['message_from_i'][1] < in_constraint:
        # print("if route yes")
        if new_storage_k <= constraint_k[0]:
            # value.nodes['j']['current_capacity'] = new_storage_j
            value.nodes[receiving_node_name]['message_history'] = message_list_updater(existing_message_list_k, policy_input['message_from_i'])
            value['i'][receiving_node_name]['traffic'] = prev_state['message_arrival'][1]
            value.nodes[receiving_node_name]['neighbor_estimate']['messages from i'] += 1 #policy_input['new_message_size']

    return (key, value) 

def s_history_located(params, substep, state_history, prev_state, policy_input):
    """
    Located files move message request from active to located states.
    """
    key = 'history'
    
    if len(prev_state['history'].active) > 5:
        temp = prev_state['history'].active[-3]
        temp.locate(block_locate=prev_state['timestep'])
        prev_state['history'].add_to_located(temp)


    value = prev_state['history']
    return (key, value)



