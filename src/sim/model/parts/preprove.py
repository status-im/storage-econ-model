import networkx as nx
import numpy as np

from ..utils import *

def p_prove_j(params, substep, state_history, prev_state):
    """
    Policy for likelihood for j to prove message receipt. Opens ability for another node to post proof.
    Uses parameter of 'j_prove_likelihood'.
    """
    
    prove_likelihood = np.array(params['j_prove_likelihood'])

    proof = True if np.random.rand() < prove_likelihood else False
 
    return {'proof_from_j': proof}

## Pre-Prove Chance for j to post proof
def s_history_pre_proved(params, substep, state_history, prev_state, policy_input):
    """
    Routed files are proved with j as prover (if j post proof according to policy p_prove_j). 
    History are added to solved list, which removes it from the routed list.
    """
    key = 'history'

    #j not prove# #########################################
    # no_proof = True if np.random.rand() < 0.95 else False

    proof =  policy_input['proof_from_j']
    if len(prev_state['history'].routed) > 3 and proof:
        temp = prev_state['history'].routed[-2]
        temp.prove(proving_node = 'j', block_prove=prev_state['timestep'])
        prev_state['history'].add_to_solved(temp)

    value = prev_state['history']
    return (key, value)

