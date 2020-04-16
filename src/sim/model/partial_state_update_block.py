from .parts.timestamp import *
from .parts.demand import *
from .parts.store import *
from .parts.network_init import *
from .parts.message import *
from .parts.metrics import *
from .parts.route import *
from .parts.ping import *
from .parts.find import *
from .parts.request import *
from .parts.prove import *
from .parts.preprove import *
from .parts.gradient import *
from .parts.pay import *




partial_state_update_block = [
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PING and UPDATE NODE Estimate AND any initialization functions
        'policies': {
            'availabilty': p_kj_availability,
            'ping_action' : p_ping,
        },
        'variables': {
            'network': init_node_i,
            'network': s_ping,
        }
    },
            {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # REQUEST INITIALIZATION
        'policies': {
            'new_message' : p_new_message,
        },
        'variables': {
            'message_arrival': s_new_message,
            'network': s_network_request,
            'event' : s_event,
        }
    },
        {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Activate Request
        'policies': {
        },
        'variables': {
            'history':  s_history_active,
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # FIND FILE
        'policies': {
            # 'new_demand': demand_function,
            'i_send_decison': p_send_i,

        },
        'variables': {
            'network': s_find_f,
            'history': s_history_located,
            
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # ROUTE 
        'policies': {
            'i_send_decison': p_send_i,
            'k_send_decision': p_send_kj, 
            # 'new_arrival': arrival_function,
        },
        'variables': {
            # 'arrival': arrival_current,
            'network': s_send_k_to_closest,
            # 'test': sent_list,
            'history':  s_history_routed,
        }
    },
        {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Pre-PROVE with J
        'policies': {
            'j_proof': p_prove_j,
        },
        'variables': {
            'history':  s_history_pre_proved,
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PROVE with P
        'policies': {
         
        },
        'variables': {
            'history':  s_history_proved,
         }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # GRADIENT, Update gradient, Update zees, update escrow with tax and subsidy
        'policies': {
          'tax_subsidy':  p_gradient,
        },
        'variables': {
            'angles':  s_angles,
            'event' : s_reconcile,
            'treasury': s_treasury,
            'zees' : s_zees,
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PAY updated escrow amount among contributors 
        'policies': {
         
        },
        'variables': {
            'network': s_network_proof_payment, # + history paid
            # 'history':  s_history_paid,
          }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # STORE 
        'policies': {
            'new_demand': demand_function,
            'new_arrival': arrival_function,

        },
        'variables': {
            'demand': demand_current,
            'arrival': arrival_current,
            'network': s_store_network_i,
            'message_list': message_global,
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # METRIC COMPUTATION
        'policies': {
        },
        'variables': {
            'gross_storage_demand': m_gross_storage,
            'least_storage_demand': m_least_storage,
            'transit': m_transit,
        }
    },
]