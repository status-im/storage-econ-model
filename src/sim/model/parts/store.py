import networkx as nx
from .message import message_list_updater

def file_checker(new_file, existing_list):
    '''
    Checks to see if new_file is already stored by node in existing_list by id (0 element in the list).
    Expected new storage is either 0 if file exists or the new file size.
    '''
    i = 0
    while i < len(existing_list):
        if new_file[0] == existing_list[i][0]:
            added_storage = 0
            break
        i += 1
    else: 
        added_storage = new_file[1]
    return added_storage

def s_store_network_i(params, substep, state_history, prev_state, policy_input):
    '''
    Update to storage of files for each node, using demand and arrival policy updates to inform the decision. 
    '''
    key = 'network'
    value = prev_state['network']
    # NODE I 
    current_store_i = value.nodes['i']['current_capacity']
    existing_message_list_i = value.nodes['i']['current_storage']
    added_storage_i = file_checker(policy_input['new_message'],existing_message_list_i)
    new_storage_i = current_store_i + added_storage_i
    constraint_i = value.nodes['i']['storage_capacity']
   
    # NODE j
    current_store_j = value.nodes['j']['current_capacity']
    existing_message_list_j = value.nodes['j']['current_storage']
    added_storage_j = file_checker(policy_input['new_message'],existing_message_list_j)
    # print(added_storage_j)
    new_storage_j = current_store_j + added_storage_j
    # print('current_store_j', current_store_j, 'new_storage_j', new_storage_j, 'added_storage_j', added_storage_j)
    constraint_j = value.nodes['j']['storage_capacity']

    # NODE K
    current_store_k = value.nodes['k']['current_capacity']
    existing_message_list_k = value.nodes['k']['current_storage']
    added_storage_k = file_checker(policy_input['new_message'],existing_message_list_k)
    new_storage_k = current_store_k + added_storage_k
    constraint_k = value.nodes['k']['storage_capacity']
    # print('constraint_k', constraint_k,'new_storage_k',new_storage_k )

    if new_storage_i <= constraint_i[0]:
        # storage is allowed
        value.nodes['i']['current_capacity'] = new_storage_i
        value.nodes['i']['current_storage'] = message_list_updater(existing_message_list_i, policy_input['new_message'])

    elif new_storage_j <= constraint_j[0]:
        # print('i to j')
        # storage at i cannot happen
        # storage at j
        value.nodes['j']['current_capacity'] = new_storage_j
        value.nodes['j']['current_storage'] = message_list_updater(existing_message_list_j, policy_input['new_message'])
        # Route to j from i 
        # # add to traffic from ROUTING # # # # NEED cONstraint
        # print('ij pre ', value['i']["j"]['traffic'])
        value['i']["j"]['traffic'] = value['i']["j"]['traffic'] + policy_input['new_message_size']
        value.nodes['j']['neighbor_estimate']['storage from i'] += 1 #policy_input['new_message_size']
        # print('ij post ', value['i']["j"]['traffic'])
    elif new_storage_k <= constraint_k[0]:
        # storage at j cannot happen
        # storage at k
        value.nodes['k']['current_capacity'] = new_storage_k
        value.nodes['k']['current_storage'] = message_list_updater(existing_message_list_k, policy_input['new_message'])
        # Route to J from k
            # # add to traffic from ROUTING # # # NEED cONstraint
        # print('ik pre ', value['i']["k"]['traffic'])
        value['i']["k"]['traffic'] = value['i']["k"]['traffic'] + policy_input['new_message_size']
        value.nodes['k']['neighbor_estimate']['storage from i'] += 1 #policy_input['new_message_size']

        # print('ik post ', value['i']["k"]['traffic'])
    else:

        value =  prev_state['network']

    return (key, value)
