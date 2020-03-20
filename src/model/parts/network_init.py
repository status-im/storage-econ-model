import networkx as nx

def init_node_i(params, substep, state_history, prev_state, policy_input):
    key = 'network'
    value = prev_state['network']

    if prev_state['timestep'] == 0:

        value.nodes['i']['inband'] = params['i_in_bandwidth']
    else: 
        value = prev_state['network']

    return (key, value)
