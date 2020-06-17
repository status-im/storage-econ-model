import networkx as nx
import numpy as np
import pandas as pd
import scipy.stats as stats

from ..sys_params import sys_params
from ..utils import *

# from ..sys_params import calc_subsidy

def p_ORDER_TEST(params, substep, state_history, prev_state):
   if params['AB_Test'] == 'Tax_Subsidy_First':
      return p_gradient_ORDER_OPS(params, substep, state_history, prev_state)
   if params['AB_Test'] == 'Fake_Penalty_First':
      return p_gradient(params, substep, state_history, prev_state)  
   raise KeyError('\'{}\' is not a valid function. Check your params'.format(params['AB_Test']))

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
        ############################################
        ## FOR TESTING #############################
        time = time * np.random.normal(1,0.2)
        #############################################
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

        # classifier
        # Probability Fake
        fake_zees = prev_state['f_hat']
        fake_angles = prev_state['f_hat_angles']
        fake_pdf = stats.norm(fake_zees.mean(), fake_zees.std())
        fake_df = pd.DataFrame(fake_angles, columns = ['fake_angles'])
        fake_df['fake_zees'] = fake_zees
        fake_df.sort_values(by=['fake_angles'], inplace =True)
        fake_zee = np.interp(angles, fake_df.fake_angles, fake_df.fake_zees)
        fake_star = fake_pdf.pdf(fake_zee)
        print('fake star', fake_star)

        # Probability Real
        # actual z_score = f(theta) BEFORE added this route to the Regressor Model
        all_zees = prev_state['zees']
        all_angles = prev_state['angles']
        real_df = pd.DataFrame(all_angles, columns = ['all_angles'])
        real_df['all_zees'] = all_zees
        real_df.sort_values(by=['all_angles'], inplace =True)
        real_zee = np.interp(angles, real_df.all_angles, real_df.all_zees)
        real_pdf = stats.norm(all_zees.mean(), all_zees.std())
        real_star = real_pdf.pdf(real_zee)

        # Redo with law of cosines
        # vector u
        u = np.array([fake_star, fake_zee])
        u_squared = (np.matrix.transpose(u)@u)
        u_norm = np.linalg.norm(u)

        # vector v
        v = np.array([ real_star, real_zee ])
        v_squared = (np.matrix.transpose(v)@v)
        v_norm = np.linalg.norm(v)

        # dot_prod = np.dot(u,v)
        dot_prod = np.dot(v,u)

        # angle
        # theta = np.arccos(dot_prod / (u_norm * v_norm))
        theta = np.arccos(dot_prod / (v_norm * u_norm))

        p_hat_star = theta * 2 / np.pi


        # Cumulative probability of fake
        denom = len(fake_df) + len(real_df)

        # change update to law of cosines
        # p_hat_star = fake_star * len(fake_df) / denom + real_star * len(real_df) / denom  

        # Coefficent for fake penalty
        fake_penalty_coef = p_hat_star**9 # WORKED ! Param sweep this

        fake_penalty = escrow * fake_penalty_coef
        # print('fake penalty', fake_penalty)

#################  A /B TEST NUMBER 2 TEST TEST ORDER OF OPERATIONS FOR ESCROW FAKE FIRST ##############################################
        # remaining escrow
        escrow = escrow - fake_penalty
        # expected z_score append solved route, get posterior expected z_score
        # regressor
        angles_appended = np.append(all_angles, angles)

        z_score = stats.zscore(angles_appended)
        # z_score = gradient
        # print(type(angles))
        exp_zee = z_score[-1]

        print('diff', real_zee - exp_zee)
        # Difference between expected and actual z_score
        diff =  ( real_zee - exp_zee )
        if diff > 0:
            tax = np.array(params['tax_%'], dtype = float) * diff * np.array(escrow, dtype = float)
        # classifier
        # 2nd order augmented tax for fake add larger tax, still have same subsidy (but fake tax should be more or on the order of subsidy)
        # probability of fake becomes a weight in the 2nd order model
            subsidy = 0
        else:
            diff = np.abs(diff)
            subsidy_from_treasury = np.array(params['subsidy_treasury'], dtype = float) * diff * prev_state['treasury']
            subsidy_from_escrow = np.array(params['subsidy_escrow'], dtype = float) * diff * np.array(escrow, dtype = float)
#################  A /B TEST NUMBER 1 TEST BOUNDS OF SUBSIDY ##############################################
            # subsidy = min(subsidy_from_treasury, subsidy_from_escrow)
            subsidy = subsidy_from_escrow + subsidy_from_treasury
            # subsidy = calc_subsidy(params['AB_Test'], subsidy_from_treasury, subsidy_from_escrow)
#################  A /B TEST NUMBER 1 TEST BOUNDS OF SUBSIDY ##############################################

            tax = 0

        # tax  = regressor tax for slow routing + penalty for being fake
        tax = tax + fake_penalty
        p_hat =  p_hat_star + 0.5 * np.random.rand()
        print('p hat = ', p_hat)

    # For keeping dictionary happy
    else:
        radii, angles = None, None
        proving_node = None
        escrow = None
        z_score = 0
        tax = 0
        subsidy = 0
        p_hat = None

    return {'gradient_update': angles, 'tax': tax, 'subsidy':subsidy, 'proving_node': proving_node, 'escrow': escrow , 'p_hat': p_hat} #, 'commitment': token}

def p_gradient_ORDER_OPS(params, substep, state_history, prev_state):
    '''
    TEST WITH ORDER: PENALIZING FAKE ROUTE BEFORE TAKING % TAX OR REWARDING % SUBSIDY
    Calculate polar coordinates from solved message distance and time.
    Calculate actual z_score and posterior expected z_score.
    Compute tax and subsidy dependent on difference between actual and expected z_score, and amount escrowed for the message.
    Uses solved list of History for escrow and time. Nodes in network for distance.
    '''

    list_length = prev_state['history'].solved
    if len(list_length) > 0:
        time = prev_state['history'].solved[-1].total_time
        ############################################
        ## FOR TESTING #############################
        time = time * np.random.normal(1,0.2)
        #############################################
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

        # classifier
        # Probability Fake
        fake_zees = prev_state['f_hat']
        fake_angles = prev_state['f_hat_angles']
        fake_pdf = stats.norm(fake_zees.mean(), fake_zees.std())
        fake_df = pd.DataFrame(fake_angles, columns = ['fake_angles'])
        fake_df['fake_zees'] = fake_zees
        fake_df.sort_values(by=['fake_angles'], inplace =True)
        fake_zee = np.interp(angles, fake_df.fake_angles, fake_df.fake_zees)
        fake_star = fake_pdf.pdf(fake_zee)
        print('fake star', fake_star)

        # Probability Real
        # actual z_score = f(theta) BEFORE added this route to the Regressor Model
        all_zees = prev_state['zees']
        all_angles = prev_state['angles']
        real_df = pd.DataFrame(all_angles, columns = ['all_angles'])
        real_df['all_zees'] = all_zees
        real_df.sort_values(by=['all_angles'], inplace =True)
        real_zee = np.interp(angles, real_df.all_angles, real_df.all_zees)
        real_pdf = stats.norm(all_zees.mean(), all_zees.std())
        real_star = real_pdf.pdf(real_zee)

        # Redo with law of cosines
        # vector u
        u = np.array([fake_star, fake_zee])
        u_squared = (np.matrix.transpose(u)@u)
        u_norm = np.linalg.norm(u)

        # vector v
        v = np.array([ real_star, real_zee ])
        v_squared = (np.matrix.transpose(v)@v)
        v_norm = np.linalg.norm(v)

        # dot_prod = np.dot(u,v)
        dot_prod = np.dot(v,u)

        # angle
        # theta = np.arccos(dot_prod / (u_norm * v_norm))
        theta = np.arccos(dot_prod / (v_norm * u_norm))

        p_hat_star = theta * 2 / np.pi


        # Cumulative probability of fake
        denom = len(fake_df) + len(real_df)

        # change update to law of cosines
        # p_hat_star = fake_star * len(fake_df) / denom + real_star * len(real_df) / denom  

        # Coefficent for fake penalty
        fake_penalty_coef = p_hat_star**9 # WORKED ! Param sweep this

        # fake_penalty = escrow * fake_penalty_coef
        # print('fake penalty', fake_penalty)

#################  A /B TEST NUMBER 2 TEST TEST ORDER OF OPERATIONS FOR ESCROW FAKE FIRST ##############################################
        # remaining escrow
        # escrow = escrow - fake_penalty
        # expected z_score append solved route, get posterior expected z_score
        # regressor
        angles_appended = np.append(all_angles, angles)

        z_score = stats.zscore(angles_appended)
        # z_score = gradient
        # print(type(angles))
        exp_zee = z_score[-1]

        print('diff', real_zee - exp_zee)
        # Difference between expected and actual z_score
        diff =  ( real_zee - exp_zee )
        if diff > 0:
            tax = np.array(params['tax_%'], dtype = float) * diff * np.array(escrow, dtype = float)
            fake_penalty = (escrow - tax ) * fake_penalty_coef
        # classifier
        # 2nd order augmented tax for fake add larger tax, still have same subsidy (but fake tax should be more or on the order of subsidy)
        # probability of fake becomes a weight in the 2nd order model
            subsidy = 0
        else:
            diff = np.abs(diff)
            subsidy_from_treasury = np.array(params['subsidy_treasury'], dtype = float) * diff * prev_state['treasury']
            subsidy_from_escrow = np.array(params['subsidy_escrow'], dtype = float) * diff * np.array(escrow, dtype = float)
#################  A /B TEST NUMBER 1 TEST BOUNDS OF SUBSIDY ##############################################
            subsidy = min(subsidy_from_treasury, subsidy_from_escrow)
            tax = 0
            fake_penalty = (escrow - tax ) * fake_penalty_coef
            # subsidy = subsidy_from_escrow + subsidy_from_treasury
           

        # tax  = regressor tax for slow routing + penalty for being fake
        tax = tax + fake_penalty
        p_hat =  p_hat_star + 0.5 * np.random.rand()
        print('p hat = ', p_hat)

    # For keeping dictionary happy
    else:
        radii, angles = None, None
        proving_node = None
        escrow = None
        z_score = 0
        tax = 0
        subsidy = 0
        p_hat = None

    return {'gradient_update': angles, 'tax': tax, 'subsidy':subsidy, 'proving_node': proving_node, 'escrow': escrow , 'p_hat': p_hat} #, 'commitment': token}

def s_angles(params, substep, state_history, prev_state, policy_input):
    '''
    Collects and stores angles from not f hat solved routes.
    '''
    key = 'angles'
    value = prev_state['angles']
    new_route = policy_input['gradient_update']

    condition = policy_input['p_hat']
    condition = 1 if condition is None else condition
# FOR TESTING CONDITIONAL VALUE
    if condition < 0.80:
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
    value = prev_state['zees']
    all_angles = prev_state['angles']
    # gradient = np.append(gradient, angles)
    new_route = policy_input['gradient_update']
    # print('new', new)
    # if new_route is not None:

    condition = policy_input['p_hat']
    condition = 1 if condition is None else condition
#  > 0.75 and 
    if condition < 0.80:    
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
    

def s_f_hat_angles(params, substep, state_history, prev_state, policy_input):
    '''
    Update the angles of routes in the f_hat distribution. Routes that are classified as fake.
    '''
    key = 'f_hat_angles'
    value = prev_state['f_hat_angles']

    condition = policy_input['p_hat']

    
    condition = 0 if condition is None else condition
    print('fhat condition = ', condition)
    
#  > 0.75 and 
    if condition > 0.80:
        
        print('f hat conditional triggered')
        all_angles = prev_state['f_hat_angles']
        # gradient = np.append(gradient, angles)
        new_route = policy_input['gradient_update']

        value = np.append(all_angles, new_route)

    return (key, value)

def s_f_hat(params, substep, state_history, prev_state, policy_input):
    '''
    Update the z_scores of the routes in the f_hat distribution. Routes that are classified as fake.
    '''
    key = 'f_hat'
    value = prev_state['f_hat']

    condition = policy_input['p_hat']

    
    condition = 0 if condition is None else condition
    print('fhat condition = ', condition)
    
#  > 0.75 and 
    if condition > 0.80:
        
        print('f hat conditional triggered')
        all_angles = prev_state['f_hat_angles']
        # gradient = np.append(gradient, angles)
        new_route = policy_input['gradient_update']

        all_angles = np.append(all_angles, new_route)
        value = stats.zscore(all_angles)

    return (key, value)

# def s_not_f_hat_angles(params, substep, state_history, prev_state, policy_input):
#     '''
#     Update the f_hat.
#     '''
#     key = 'not_f_hat_angles'
#     value = prev_state['not_f_hat_angles']

#     condition = policy_input['p_hat']
#     condition = 1 if condition is None else condition
# #  > 0.75 and 
#     if condition < 0.75:
#         print('not f hat angles conditional triggered')
#         new_route = policy_input['gradient_update']

#         value = np.append(value, new_route)
      
#     return (key, value)

# def s_not_f_hat(params, substep, state_history, prev_state, policy_input):
#     '''
#     Update the f_hat.
#     '''
#     key = 'not_f_hat'
#     value = prev_state['not_f_hat']

#     condition = policy_input['p_hat']
#     condition = 1 if condition is None else condition
# #  > 0.75 and 
#     if condition < 0.75:
#         all_angles = prev_state['not_f_hat_angles']
#         # gradient = np.append(gradient, angles)
#         new_route = policy_input['gradient_update']

#         all_angles = np.append(all_angles, new_route)
#         value = stats.zscore(all_angles)

#     return (key, value)