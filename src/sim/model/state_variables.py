from datetime import datetime
import networkx as nx
import numpy as np
# from copy import deepcopy
import scipy.stats as stats
from .sys_params import sys_params
from .utils import *
from .parts.network_init import *

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

## Fake Route Initialization #######################################
f_hat = np.linspace(-3,3,num =3, dtype = float)
f_hat_angles = np.linspace(-1,1,num =3, dtype = float)
not_f_hat_angles = np.linspace(-1,1,num =3, dtype = float)
not_f_hat = np.linspace(-3,3,num =30, dtype = float)
 

## Genesis States #################################################
genesis_states = {
    'timestamp': datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
    'message_array': np.zeros((1, 3), dtype=np.uint),
    'message_list': message_list.copy(),
    'file_list': file_list.copy(),
    'demand': 0,
    'arrival': 0,
    'message_arrival': message_list.copy(),
    'network': init_network(),
    'gross_storage_demand': 0,
    'least_storage_demand': 0, 
#     'PO': 0,  #  FOr testing
#     'test': 0, # For testing
    'event': Event(),
    'history': History(),
#     'mirror': None, # For testing
    'angles': np.array([0,1,-1], dtype = float),
    'zees': np.array([0,1,-1], dtype = float),
    'treasury': 0,
    'transit' : 0,
    'f_hat_angles': f_hat_angles,
    'f_hat': f_hat,
#     'not_f_hat_angles': not_f_hat_angles, 
#     'not_f_hat': not_f_hat,
}
