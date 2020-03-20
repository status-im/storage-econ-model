import networkx as nx
### NETWORK INITIALIZATION ###############################
# ij = nx.DiGraph()

### NODE INITITALIZATION #################################
# i node Initial Values and Constraints #
i_storage = [500]
i_in_bandwidth = [500, 1234]
i_out_bandwidth = [140]

# j node Initial Values and Constraints #
j_storage = [500]
j_in_bandwidth = [400]
j_out_bandwidth = [100]

# p node Initial Values and Constraints #
p_storage = [4000]
p_in_bandwidth = [400]
p_out_bandwidth = [600]

# k node Initial Values and Constraints #
k_storage = [8000]
k_in_bandwidth = [400]
k_out_bandwidth = [80]

# Node Availability Estimate Initial Values
j_avail_to_i = [0.90]
k_avail_to_i = [0.80]
j_avail_to_k = [0.70]
p_avail_to_i = [0.60]

# Time
BLOCK_TIME = [30]

# depth
depth = [15]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
sys_params = {
   'block_time': BLOCK_TIME,
   'i_storage': i_storage,
   'i_in_bandwidth': i_in_bandwidth, 
   'i_out_bandwidth': i_out_bandwidth,
   'j_storage': j_storage,
   'j_in_bandwidth': j_in_bandwidth,
   'j_out_bandwidth': j_out_bandwidth,
   'p_storage': p_storage,
   'p_in_bandwidth': p_in_bandwidth,
   'p_out_bandwidth': p_out_bandwidth,
   'k_storage': k_storage,
   'k_in_bandwidth': k_in_bandwidth,
   'k_out_bandwidth': k_out_bandwidth,
   'j_avail_to_i': j_avail_to_i,
   'k_avail_to_i': k_avail_to_i,
   'j_avail_to_k': j_avail_to_k,
   'p_avail_to_i': p_avail_to_i,
   'depth':depth



   # 'network': ij
   # parameter networkx object just the initiallization 

}