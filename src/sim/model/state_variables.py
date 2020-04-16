from datetime import datetime
import networkx as nx
import numpy as np
# from copy import deepcopy
import scipy.stats as stats
from .sys_params import sys_params
from .utils import *
## Message List Initialization ###################################
message_list = [None] *3
message_list = [message_list]*2

## Network Initialization #######################################
ij = nx.DiGraph()
# Empty List for file storage 3 x 2
# [id, size, frequency]
file_list =  [None] *3
# Make send None row for dimensionality
file_list = [file_list] * 2
##### Initial Memory of Stored Files
size = 0
# Message History Initialization 
# # [id, size, freq] 
message_i = message_list.copy()
message_j = message_list.copy()
message_k = message_list.copy()
message_p = message_list.copy()
message_r = message_list.copy()

# Neighbor Estimate for each Node
i_est = {'j_avail_to_i': sys_params['j_avail_to_i'], 'k_avail_to_i': sys_params['k_avail_to_i'], 'p_avail_to_i': sys_params['p_avail_to_i'],'messages from k': 0, 'messages from i': 0}
j_est = {'storage from i': 0, 'storage from k': 0, 'messages from i': 0, 'messages from k': 0}
k_est = {'storage from i': 0,'messages from i': 0,'j_avail_to_k':  sys_params['j_avail_to_k']}
p_est = {'messages from i': 0,'messages from k': 0}
r_est = {'messages from i': 0,'messages from k': 0}


# ADD NODES
ij.add_node('i', neighbor_estimate= i_est, storage_capacity=sys_params['i_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['i_in_bandwidth'],\
     outband=sys_params['i_out_bandwidth'], message_history = message_i, control=[], wallet = sys_params['i_wallet'])
ij.add_node('j', neighbor_estimate= j_est, storage_capacity=sys_params['j_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['j_in_bandwidth'],\
     outband=sys_params['j_out_bandwidth'], message_history = message_j, control=[], wallet = sys_params['j_wallet'])
ij.add_node('k', neighbor_estimate= k_est, storage_capacity=sys_params['k_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['k_in_bandwidth'],\
     outband=sys_params['k_out_bandwidth'], message_history = message_k, control=[], wallet = sys_params['k_wallet'])
ij.add_node('p', neighbor_estimate= p_est, storage_capacity=sys_params['p_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['p_in_bandwidth'],\
     outband=sys_params['p_out_bandwidth'], message_history = message_p, control=[], wallet = sys_params['p_wallet'])
ij.add_node('r', neighbor_estimate= r_est, storage_capacity=sys_params['r_storage'], current_storage = file_list.copy(), current_capacity = size, inband= sys_params['r_in_bandwidth'],\
     outband=sys_params['r_out_bandwidth'], message_history = message_r, control=[], wallet = sys_params['r_wallet'])
# ADD EDGES
ij.add_edge('i',"j")
ij.add_edge('i',"k")
ij.add_edge('i',"p")
ij.add_edge('k',"j")
ij.add_edge('k',"i")
ij.add_edge('k',"p")
ij.add_edge('j',"p")
ij.add_edge('k',"r")
ij.add_edge('r',"j")
ij.add_edge('i',"r")
ij.add_edge('i',"i")

# Add initial history of traffic between nodes
ij['i']["j"]['traffic'] = 0
ij['i']["k"]['traffic'] = 0
ij['k']["j"]['traffic'] = 0
ij['j']["p"]['traffic'] = 0
ij['i']["p"]['traffic'] = 0
ij['k']["r"]['traffic'] = 0
ij['k']["p"]['traffic'] = 0
ij['k']["i"]['traffic'] = 0
ij['r']["j"]['traffic'] = 0
ij['i']["r"]['traffic'] = 0
ij['i']["i"]['traffic'] = 0

# ADD IDS
for node in ij:
    ij.nodes[str(node)]['id']  = np.random.randint(0,16)

# ROUTING TABLE INITIALIZATION
ij.nodes['i']['routing_table'] = []
ij.nodes['j']['routing_table'] = []
ij.nodes['k']['routing_table'] = []
ij.nodes['p']['routing_table'] = []
ij.nodes['r']['routing_table'] = []

ij.nodes['i']['routing_table'] = route_table(ij, 'i')
ij.nodes['j']['routing_table'] = route_table(ij, 'j')
ij.nodes['k']['routing_table'] = route_table(ij, 'k')
ij.nodes['p']['routing_table'] = route_table(ij, 'p')
ij.nodes['r']['routing_table'] = route_table(ij, 'r')

 

## Genesis States #################################################
genesis_states = {
    'timestamp': datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
    'message_array': np.zeros((1, 3), dtype=np.uint),
    'message_list': message_list.copy(),
    'file_list': file_list.copy(),
    'demand': 0,
    'arrival': 0,
    'message_arrival': message_list.copy(),
    'network': ij,
    'gross_storage_demand': 0,
    'least_storage_demand': 0, 
    'PO': 0,
#     'test': 0, # For testing
    'event': Event(),
    'history': History(),
#     'mirror': None, # For testing
    'angles': np.array([0,1,-1], dtype = float),
    'zees': np.array([0,1,-1], dtype = float),
    'treasury': 0,
    'transit' : 0
}
