import networkx as nx
import numpy as np
import itertools

# For A/B Test as Parameter Sweep
# from .parts.gradient import p_gradient
# from .parts.gradient_B import p_gradient_ORDER_OPS

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
STARTING_TREASURY_TOKENS = [0] #[0, 1000, 2000]  #[0] #
TAX =  [0.05] #[0.15,0.25,0.35] # [0.05] # [0.15,0.25,0.35]  # [0.05,0.10,0.15] #[0.05,0.10,0.15, 0.20][0.05] #
SUBSIDY_TREASURY =[0.20] # [0.10, 0.20, 0.30] #  #[0.05,0.10,0.15, 0.20]# [0.10] #
SUBSIDY_ESCROW =  [0.20] #[0.10, 0.20, 0.30] #[0.25] #[0.05,0.10,0.15, 0.20]

# ALLOCATION PARAMETERS
ROUTE_ALLOCATION = [0.25, 0.35, 0.45]  # [0.20] #[0.10, .20, .30] # [0.10, .20, .30]
STORE_ALLOCATION = [0.35] # [0.25, 0.35, 0.45] 
# Removed as a parameter because it is dependent
# PROVE_ALLOCATION = list(1 - np.array(ROUTE_ALLOCATION) - np.array(STORE_ALLOCATION))

# Prove Likelihood for Recipient J
PROOF_LIKELIHOOD = [0.95]

# Messaging Storage Cost Parameters
STORAGE_BASE_COST = [0.51]  # $0.0003 / mb  in SNT 
MEESAGE_BASE_COST = [0.034]  #  $0.00002 / mb IN SNT
UTILITY_COST_VOLATILITY = [1]

########### A/B Test Functions ################################################
# Bound Test
# A_B_TESTS = ['bound', 'partition']
# def calc_subsidy(param_test, subsidy_from_treasury, subsidy_from_escrow):
#    if param_test == 'bound':
#       subsidy = min(subsidy_from_treasury, subsidy_from_escrow)
#    if param_test == 'partition':
#       subsidy = subsidy_from_escrow + subsidy_from_treasury
#    return subsidy
# CONTROL = ''

###### order OF operations ####################################
A_B_TESTS = ['Tax_Subsidy_First'] #, 'Fake_Penalty_First']

# Moved to gradient.py
# def p_ORDER_TEST(params, substep, state_history, prev_state):
#    if params['AB_Test'] == 'Tax_Subsidy_First':
#       return p_gradient_ORDER_OPS(params, substep, state_history, prev_state)
#    if params['AB_Test'] == 'Fake_Penalty_First':
#       return p_gradient(params, substep, state_history, prev_state)  
#    raise KeyError('\'{}\' is not a valid function. Check your params'.format(params['AB_Test']))


#### USE ONLY FOR A/B WITH PARAMETER SWEEPS ###########################
# factors = [A_B_TESTS,TAX]
# product = list(itertools.product(*factors))
# A_B_TESTS, TAX = zip(*product)
# A_B_TESTS = list(A_B_TESTS)
# TAX = list(TAX)

factors = [A_B_TESTS,STORE_ALLOCATION, TAX, ROUTE_ALLOCATION]
product = list(itertools.product(*factors))
A_B_TESTS,  STORE_ALLOCATION, TAX, ROUTE_ALLOCATION = zip(*product)
A_B_TESTS = list(A_B_TESTS)
STORE_ALLOCATION = list(STORE_ALLOCATION)
TAX = list(TAX)
ROUTE_ALLOCATION = list(ROUTE_ALLOCATION)
# PROVE_ALLOCATION = list(PROVE_ALLOCATION)
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
   # 'prove_allocation': PROVE_ALLOCATION,
   'starting_treasury': STARTING_TREASURY_TOKENS,
   'j_prove_likelihood': PROOF_LIKELIHOOD,
   'AB_Test' : A_B_TESTS,
   'storage_base_cost' : STORAGE_BASE_COST,
   'message_base_cost' : MEESAGE_BASE_COST,
   'utility_cost_volatility' : UTILITY_COST_VOLATILITY,

}