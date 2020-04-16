import numpy as np

def ping_decision(pinging_node, pinged_node):
    ''' 
    Decision by node to ping another node. 
    '''
    # Start Logic to ping
    
    # End logic to ping
    
    decision = pinged_node + '_avail_to_' + pinging_node
    return decision

def ping_calc(old_est,avail):
    ''' 
    Ping is an action to determine if a node is on/offline 
    Updates node's estimate of receiving availability
    '''
    old_est = np.array(old_est) 
    if avail:
        result = old_est + 0.01
        result = min(result,1)
    
    else: 
        result = old_est - 0.01
        result = max(result,0)

    return result

def p_kj_availability(params, substep, state_history, prev_state):
    ''' 
    Random availability of k and j
    Assume high likelihood of online

    Opposite would be highly likelihood of offline
    '''
    k_rand = np.random.rand()
    j_rand = np.random.rand()

    if k_rand < 0.1:
        k_availability = False
    else:
        k_availability = True

    if j_rand < 0.1:
        j_availability = False
    else:
        j_availability = True

    return {'k_availability': k_availability, 'j_availability': j_availability}

def p_ping(params, substep, state_history, prev_state):
    ''' 
    Random choice from i to ping k and/or j
    Assume low likelihood of pinging
    Choice for k to ping j 
    True is a ping, False is no ping
    '''
    k_decision = np.random.rand()
    j_decision = np.random.rand()
    kj_decision = np.random.rand()

    if k_decision < 0.05:
        k_ping = True
    else:
        k_ping = False

    if j_decision < 0.05:
        j_ping = True
    else:
        j_ping = False

    if kj_decision < 0.05:
        kj_ping = True
    else:
        kj_ping = False

    return {'k_ping': k_ping, 'j_ping': j_ping, 'kj_ping': kj_ping}

def s_ping(params, substep, state_history, prev_state, policy_input):
    ''' 
    Update nodes neighbor estimate of neighboring availability based on ping update.
    '''
    key = 'network'
    value = prev_state[key]

    if policy_input['k_ping']:
        # i Ping k
        old_est = value.nodes['i']['neighbor_estimate']['k_avail_to_i']
        # print(old_est)
        avail = policy_input['k_availability']
        new_est = ping_calc(old_est,avail)
        value.nodes['i']['neighbor_estimate']['k_avail_to_i'] = new_est

    if policy_input['j_ping']:
        # i Ping j
        old_est = value.nodes['i']['neighbor_estimate']['j_avail_to_i']
        # print(old_est)
        avail = policy_input['j_availability']
        new_est = ping_calc(old_est,avail)
        value.nodes['i']['neighbor_estimate']['j_avail_to_i'] = new_est

    if policy_input['kj_ping']:
        # k Ping j
        old_est = value.nodes['k']['neighbor_estimate']['j_avail_to_k']
        # print(old_est)
        avail = policy_input['j_availability']
        new_est = ping_calc(old_est,avail)
        value.nodes['k']['neighbor_estimate']['j_avail_to_k'] = new_est

    return (key, value)