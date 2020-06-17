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
    ###################### IF FUNDS ARE THERE AND PAID ######################
    for solved_message in list(solved_list):
         

        # get original commited tokens from sender
        commit = solved_message.sender_pledge
        # get tokens from sender wallet (not right becuase ameneded by online learning model)  
        wallet = np.array(value.nodes[solved_message.sending_node]['wallet'], dtype = 'float')
        print(wallet, type(wallet))
        wallet -= commit

        # NOT ENOUGH FUNDS!
        if wallet < 0:
            value.nodes[solved_message.sending_node]['wallet'] = 0
            # NOT PAID LIST , NOT TRUST LIST
            prev_state['history'].add_to_not_paid(solved_message)
            proving_node = solved_message.proving_node
            value.nodes[proving_node]['control'][solved_message.sending_node] = 0
            storing_node = solved_message.storing_node
            value.nodes[storing_node]['control'][solved_message.sending_node] = 0
            route_wallet = np.array(value.nodes['r']['wallet'], dtype = 'float')
            value.nodes['r']['control'][solved_message.sending_node] = 0


        else:
            # Funds are there, PAID
            value.nodes[solved_message.sending_node]['wallet'] = wallet
            # get updated escrow WHICH has already been increased or decreased by gradient
            tokens = solved_message.escrow
            # pay prover
            prove_allocation = (1 -  np.array(params['route_allocation'], dtype = float) - np.array(params['store_allocation'], dtype = float))
            # print('prove allocation', prove_allocation)
            proving_node = solved_message.proving_node
            prove_wallet = np.array(value.nodes[proving_node]['wallet'], dtype = 'float')
            # prove_wallet += tokens * np.array(params['prove_allocation'], dtype = float)
            prove_wallet += tokens * prove_allocation
            value.nodes[proving_node]['wallet'] = prove_wallet
            value.nodes[proving_node]['control'][solved_message.sending_node] = 1

            # pay storer
            storing_node = solved_message.storing_node
            store_wallet = np.array(value.nodes[storing_node]['wallet'], dtype = 'float')
            store_wallet += tokens * np.array(params['store_allocation'], dtype = float)
            value.nodes[storing_node]['wallet'] = store_wallet
            value.nodes[storing_node]['control'][solved_message.sending_node] = 1

            # pay route
            routing_node = solved_message.route_list
            route_wallet = np.array(value.nodes['r']['wallet'], dtype = 'float')
            route_wallet += tokens * np.array(params['route_allocation'], dtype = float)
            value.nodes['r']['wallet'] = route_wallet
            value.nodes['r']['control'][solved_message.sending_node] = 1

            # Move from solved list to paid list in history
            prev_state['history'].add_to_paid(solved_message)

    return (key, value)

def s_treasury_upon_post(params, substep, state_history, prev_state, policy_input):
    '''
    Update treasury account for solved message with tax/subsidy
    Add for tax. Subtract for subsidy from gradient policy.
    Only Paid list, but do not double spend
    '''
    key = 'treasury'
    value = 0 # prev_state['treasury']
    paid_list = prev_state['history'].paid
    for item in paid_list:
        value += item.delta
    # delta = policy_input['tax'] - policy_input['subsidy']
    # value += delta 

    return (key, value)

def s_event_payment(params, substep, state_history, prev_state, policy_input):
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
        prove_allocation = (1 -  np.array(params['route_allocation'], dtype = float) - np.array(params['store_allocation'], dtype = float))
        # print('prove allocation', prove_allocation)
        proving_node = solved_message.proving_node
        prove_wallet = np.array(value.nodes[proving_node]['wallet'], dtype = 'float')
        # prove_wallet += tokens * np.array(params['prove_allocation'], dtype = float)
        prove_wallet += tokens * prove_allocation
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

