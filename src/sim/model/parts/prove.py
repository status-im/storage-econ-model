import networkx as nx
import numpy as np

from ..utils import *


## Prove Chance for p to post proof if j doesn't
def s_history_proved(params, substep, state_history, prev_state, policy_input):
    """
    Routed files are proved with p as prover (if j does not post proof according to policy p_prove_j). 
    History are added to solved list, which removes it from the routed list.
    """

    key = 'history'
 
    if len(prev_state['history'].routed) > 3:
        temp = prev_state['history'].routed[-2]
        temp.prove(proving_node = 'p', block_prove=prev_state['timestep'])
        prev_state['history'].add_to_solved(temp)

        # Move out
        # Reward for proof
        # proving_node = temp.proving_node
        # tokens = temp.escrow
        # wallet = np.array(prev_state['network'].nodes[proving_node]['wallet'])
        # wallet += tokens
        # prev_state['network'].nodes[proving_node]['wallet'] = wallet

    value = prev_state['history']
    return (key, value)