import numpy as np

def s_network_proof_payment(params, substep, state_history, prev_state, policy_input):
    '''
    Update wallets for payment from solving / proving / routing and taxed and subsidized payment. 
    Payments are allocated across participants via allocation parameters.
    Escrow amount from message has already been adjusted with s_reconcile in previous partial state update.
    Solved messages are removed from solved list and added to paid list.
    '''
    key = 'network'
    value = prev_state['network']
    solved_list = prev_state['history'].solved
    # get solved message
    # iterate over copy of list because list elements are removed in loop
    for solved_message in list(solved_list):
         
        # get updated escrow
        tokens = solved_message.escrow
             
        # pay prover
        proving_node = solved_message.proving_node
        prove_wallet = np.array(value.nodes[proving_node]['wallet'], dtype = 'float')
        prove_wallet += tokens * np.array(params['prove_allocation'], dtype = float)
        value.nodes[proving_node]['wallet'] = prove_wallet

        # pay storer
        storing_node = solved_message.storing_node
        store_wallet = np.array(value.nodes[storing_node]['wallet'], dtype = 'float')
        store_wallet += tokens * np.array(params['store_allocation'], dtype = float)
        value.nodes[storing_node]['wallet'] = store_wallet

        # pay route
        routing_node = solved_message.route_list
        route_wallet = np.array(value.nodes['r']['wallet'], dtype = 'float')
        route_wallet += tokens * np.array(params['route_allocation'], dtype = float)
        value.nodes['r']['wallet'] = route_wallet

        # Move from solved list to paid list in history
        prev_state['history'].add_to_paid(solved_message)

    return (key, value)

