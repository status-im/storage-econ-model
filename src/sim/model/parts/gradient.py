import networkx as nx
import numpy as np
import pandas as pd
import scipy.stats as stats

from ..sys_params import sys_params
from ..utils import *

## Calculate p_gradient using contract info(escrow and proving time and distance)
def p_gradient(params, substep, state_history, prev_state):
    '''
    Calculate polar coordinates from solved message distance and time.
    Calculate actual z_score and posterior expected z_score.
    Compute tax and subsidy dependent on difference between actual and expected z_score, and amount escrowed for the message.
    Uses solved list of History for escrow and time. Nodes in network for distance.
    '''

    list_length = prev_state['history'].solved
    if len(list_length) > 0:
        time = prev_state['history'].solved[-1].total_time
        time = time * np.random.normal(1,0.2)
        # sending node, receiving node
        # MAKE K to J for distance
        # Keep i to p for TIME
        # TIME
        # Request to Proof
        sending_node = prev_state['history'].solved[-1].sending_node
        sending_id = prev_state['network'].nodes[str(sending_node)]['id']
     
        proving_node = prev_state['history'].solved[-1].proving_node
        proving_id = prev_state['network'].nodes[str(proving_node)]['id']

        # DISTANCE
        # Storing to Receiving Distance
        storing_node = prev_state['history'].solved[-1].storing_node
        storing_id = prev_state['network'].nodes[str(storing_node)]['id']
     
        receiving_node = prev_state['history'].solved[-1].receiving_node
        receiving_id = prev_state['network'].nodes[str(receiving_node)]['id']

        dist = distance_calc(storing_id, receiving_id)

        radii, angles = cart_to_pol(dist,time)

        escrow = prev_state['history'].solved[0].escrow

        # regressor
        angles = angles #* np.random.normal(1,0.2)
        # actual z_score = f(theta) BEFORE added this route to the Regressor Model
        all_zees = prev_state['zees']
        all_angles = prev_state['angles']
        gradient_df = pd.DataFrame(all_angles, columns = ['all_angles'])
        gradient_df['all_zees'] = all_zees
        gradient_df.sort_values(by=['all_angles'], inplace =True)
        actual_zee = np.interp(angles, gradient_df.all_angles, gradient_df.all_zees)

        # expected z_score append solved route, get posterior expected z_score

        angles_appended = np.append(all_angles, angles)

        z_score = stats.zscore(angles_appended)
        # z_score = gradient
        # print(type(angles))
        exp_zee = z_score[-1]

        print('diff', actual_zee - exp_zee)
        # Difference between expected and actual z_score
        diff =  ( actual_zee - exp_zee )
        if diff > 0:
            tax = np.array(params['tax_%'], dtype = float) * diff * np.array(escrow, dtype = float)
        # classifier
        # 2nd order augmented tax for fake add larger tax, still have same subsidy (but fake tax should be more or on the order of subsidy)
        # probability of fake becomes a weight in the 2nd order model
            subsidy = 0
        else:
            subsidy_from_treasury = np.array(params['subsidy_treasury'], dtype = float) * diff * prev_state['treasury']
            subsidy_from_escrow = np.array(params['subsidy_escrow'], dtype = float) * diff * np.array(escrow, dtype = float)
            subsidy = min(subsidy_from_treasury, subsidy_from_escrow)

            tax = 0


    # For keeping dictionary happy
    else:
        radii, angles = None, None
        proving_node = None
        escrow = None
        z_score = 0
        tax = 0
        subsidy = 0

    return {'gradient_update': angles, 'tax': tax, 'subsidy':subsidy, 'proving_node': proving_node, 'escrow': escrow } #, 'commitment': token}

def s_angles(params, substep, state_history, prev_state, policy_input):
    '''
    Collects and stores angles from all solved routes.
    '''
    key = 'angles'
    value = prev_state['angles']
    new_route = policy_input['gradient_update']
    if new_route is not None:
        value = np.append(value, new_route)

    return (key, value)

def s_zees(params, substep, state_history, prev_state, policy_input):
    '''
    Update all z_scroes with solved angle from new message solve
    Append new angle to gradient state (array of angles).
    Re-calculate all z_scores. 
    Stored as state for computation of actual z_score in the next state. 
    '''
    key = 'zees'
    all_angles = prev_state['angles']
    # gradient = np.append(gradient, angles)
    new_route = policy_input['gradient_update']
    # print('new', new)
    if new_route is not None:
        all_angles = np.append(all_angles, new_route)
    value = stats.zscore(all_angles)

    return (key, value)


def s_treasury(params, substep, state_history, prev_state, policy_input):
    '''
    Update treasury account for solved message with tax/subsidy
    Add for tax. Subtract for subsidy from gradient policy.
    '''
    key = 'treasury'
    value = prev_state['treasury']
    
    # Preset in config loop
    # Handling initialization of starting treasury
    # Moved to s_init_treasury
    # if prev_state['timestep'] == 1:
    #     initial_tokens = params['starting_treasury']
    # else:
    #     initial_tokens = 0
    # value += initial_tokens

    delta = policy_input['tax'] - policy_input['subsidy']
    value += delta 

    return (key, value)


def s_reconcile(params, substep, state_history, prev_state, policy_input):
    '''
    Update the escrow amount for each solved message with its computed tax/subsidy from p_gradient.
    '''
    key = 'event'

    list_length = prev_state['history'].solved
    if len(list_length) > 0:
        last_message = prev_state['history'].solved[-1]
        last_message.incentive(tax = policy_input['tax'], subsidy = policy_input['subsidy'])

    value = prev_state['event']

    return (key, value)
    