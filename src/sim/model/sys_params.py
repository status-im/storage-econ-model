import networkx as nx
import numpy as np
### NETWORK INITIALIZATION ###############################
# ij = nx.DiGraph()

### NODE INITITALIZATION #################################
# i node Initial Values and Constraints #
i_storage = [500]
i_in_bandwidth = [1234]
i_out_bandwidth = [140]
i_wallet = [10000]

# j node Initial Values and Constraints #
j_storage = [500]
j_in_bandwidth = [400]
j_out_bandwidth = [100]
j_wallet = [0]

# p node Initial Values and Constraints #
p_storage = [4000]
p_in_bandwidth = [400]
p_out_bandwidth = [600]
p_wallet = [0]

# k node Initial Values and Constraints #
k_storage = [8000]
k_in_bandwidth = [400]
k_out_bandwidth = [80]
k_wallet = [0]

# r node Initial Values and Constraints #
r_storage = [8000]
r_in_bandwidth = [400]
r_out_bandwidth = [80]
r_wallet = [0]

# Node Availability Estimate Initial Values
j_avail_to_i = [0.90]
k_avail_to_i = [0.80]
j_avail_to_k = [0.70]
p_avail_to_i = [0.60]

# Time
BLOCK_TIME = [30]

# depth
depth = [15]

# TREASURY ACCOUNTING PARAMETERS
STARTING_TREASURY_TOKENS = [0, 1000, 2000]
TAX = [0.10]
SUBSIDY_TREASURY = [0.10]
SUBSIDY_ESCROW = [0.10]

# ALLOCATION PARAMETERS
ROUTE_ALLOCATION = [0.10]
STORE_ALLOCATION = [0.45]
PROVE_ALLOCATION = list(1 - np.array(ROUTE_ALLOCATION) - np.array(STORE_ALLOCATION))

# Prove Likelihood for Recipient J
PROOF_LIKELIHOOD = [0.95]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
sys_params = {
   'block_time': BLOCK_TIME,
   'i_storage': i_storage,
   'i_in_bandwidth': i_in_bandwidth, 
   'i_out_bandwidth': i_out_bandwidth,
   'j_storage': j_storage,
   'i_wallet': i_wallet, 
   'j_in_bandwidth': j_in_bandwidth,
   'j_out_bandwidth': j_out_bandwidth,
   'j_wallet': j_wallet, 
   'p_storage': p_storage,
   'p_in_bandwidth': p_in_bandwidth,
   'p_out_bandwidth': p_out_bandwidth,
   'p_wallet': p_wallet, 
   'k_storage': k_storage,
   'k_in_bandwidth': k_in_bandwidth,
   'k_out_bandwidth': k_out_bandwidth,
   'k_wallet': k_wallet,
   'r_storage': r_storage,
   'r_in_bandwidth': r_in_bandwidth,
   'r_out_bandwidth': r_out_bandwidth,
   'r_wallet': r_wallet, 
   'j_avail_to_i': j_avail_to_i,
   'k_avail_to_i': k_avail_to_i,
   'j_avail_to_k': j_avail_to_k,
   'p_avail_to_i': p_avail_to_i,
   'depth':depth,
   'tax_%': TAX,
   'subsidy_escrow': SUBSIDY_ESCROW,
   'subsidy_treasury': SUBSIDY_TREASURY,
   'route_allocation': ROUTE_ALLOCATION,
   'store_allocation': STORE_ALLOCATION,
   'prove_allocation': PROVE_ALLOCATION,
   'starting_treasury': STARTING_TREASURY_TOKENS,
   'j_prove_likelihood': PROOF_LIKELIHOOD,

}