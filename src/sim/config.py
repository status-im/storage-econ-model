
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim
# if test notebook is in parent above /src
from .model.state_variables import genesis_states
from .model.partial_state_update_block import partial_state_update_block #, partial_state_update_block_B
from .model.sys_params import sys_params #as sys_params_A
from .model.utils import *

from copy import deepcopy
from cadCAD import configs
import scipy.stats as stats
import networkx as nx
import numpy as np

# if test notebook is in /src
# from model.state_variables import genesis_states
# from model.partial_state_update_block import partial_state_update_block
# from model.sys_params import sys_params as sys_params_A

from .sim_setup import SIMULATION_TIME_STEPS, MONTE_CARLO_RUNS

sim_config = config_sim (
    {
        'N': MONTE_CARLO_RUNS, 
        'T': range(SIMULATION_TIME_STEPS), # number of timesteps
        'M': sys_params,
    }
)
append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=partial_state_update_block
)


# FOR A/B Test
# append_configs(
#     sim_configs=sim_config,
#     initial_state=genesis_states,
#     partial_state_update_blocks=partial_state_update_block_B
# )


def init_network(n, params):
    # message =  [None] *3
    # message= [message]*2
    # # NAMES MUST BE UNIQUE OR NETWORKX WILL OVERWRITE, copy would work too
    # message_i = message
    # message_j = [None] *3
    # message_j = [message_j] *2
    # message_k = [None] *3
    # message_k = [message_k] * 2
    # message_p =[None] *3
    # message_p = [message_p] * 2
    # # NEIGHBOR ESTIMATE DICTIONARY
    # j_est = {'storage from i': 0, 'storage from k': 0, 'messages from i': 0, 'messages from k': 0}
    # k_est = {'storage from i': 0,'messages from i': 0}

    # size = 0
    # ij.add_node('i', neighbor_estimate={}, storage_capacity=sys_params['i_storage'], current_storage=message_i, current_capacity = size, inband= sys_params['i_in_bandwidth'],\
    #     outband=sys_params['i_out_bandwidth'], control=[])
    # ij.add_node('j', neighbor_estimate=j_est, storage_capacity=sys_params['j_storage'], current_storage=message_j, current_capacity = size, inband= sys_params['j_in_bandwidth'],\
    #     outband=sys_params['j_out_bandwidth'], control=[])
    # ij.add_node('k', neighbor_estimate=k_est, storage_capacity=sys_params['k_storage'], current_storage=message_k, current_capacity = size, inband= sys_params['k_in_bandwidth'],\
    #     outband=sys_params['k_out_bandwidth'], control=[])
    # ij.add_node('p', neighbor_estimate=10, storage_capacity=sys_params['p_storage'], current_storage=message_p, current_capacity = size, inband= sys_params['p_in_bandwidth'],\
    #     outband=sys_params['p_out_bandwidth'], control=[])
    # ij.add_edge('i',"j")
    # ij.add_edge('i',"k")
    # ij.add_edge('k',"j")
    # ij.add_edge('j',"p")
    # ij['i']["j"]['traffic'] = 0
    # ij['i']["k"]['traffic'] = 0
    # ij['k']["j"]['traffic'] = 0
    # ij['j']["p"]['traffic'] = 0
    n.nodes['i']['inband'] = params['i_in_bandwidth']

    # for node in n:
    #     n.nodes[str(node)]['id']  = np.random.randint(0,16)

    # n.nodes['j']['inband'] = params['j_in_bandwidth']
    # n.nodes['k']['inband'] = params['k_in_bandwidth']
    # n.nodes['p']['inband'] = params['p_in_bandwidth']

    # n.nodes['j']['param'] = params['node_param_j']
    # n.nodes['k']['param'] = params['node_param_k']
    # n.nodes['p']['param'] = params['node_param_p']
    return n


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # GENESIS SWEEP LOGIC # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

for c in configs: # for each configuration object
    c.initial_state = deepcopy(c.initial_state) # make a deepcopy of the initial state dict (it's shared across configs by default)
    # for k in c.initial_state: # for each state variable
    #     if k in c.sim_config['M']: # if there is a param with the same name in the params dict
    #         c.initial_state[k] = c.sim_config['M'][k] # assign the param value to the initial value of the state variable

    c.initial_state['treasury'] = c.sim_config['M']['starting_treasury'] 
    c.initial_state['network']  = init_network(c.initial_state['network'], c.sim_config['M'])
    # c.initial_state['treasury'] = c.sim_config['M']['AB_Test'] 

    for node in c.initial_state['network']:
        c.initial_state['network'].nodes[str(node)]['id']  = np.random.randint(0,16)
    # ROUTING TABLE INITIALIZATION
    c.initial_state['network'].nodes['i']['routing_table'] = []
    c.initial_state['network'].nodes['j']['routing_table'] = []
    c.initial_state['network'].nodes['k']['routing_table'] = []
    c.initial_state['network'].nodes['p']['routing_table'] = []
    c.initial_state['network'].nodes['r']['routing_table'] = []

    c.initial_state['network'].nodes['i']['routing_table'] = route_table(c.initial_state['network'], 'i')
    c.initial_state['network'].nodes['j']['routing_table'] = route_table(c.initial_state['network'], 'j')
    c.initial_state['network'].nodes['k']['routing_table'] = route_table(c.initial_state['network'], 'k')
    c.initial_state['network'].nodes['p']['routing_table'] = route_table(c.initial_state['network'], 'p')
    c.initial_state['network'].nodes['r']['routing_table'] = route_table(c.initial_state['network'], 'r')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # END GENESIS SWEEP LOGIC # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #