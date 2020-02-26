from .parts.timestamp import *
from .parts.demand import *
from .parts.store import *
from .parts.network_init import *
from .parts.message import *
from .parts.metrics import *
from .parts.route import *



partial_state_update_block = [
     {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # INIT
        'policies': {
        },
        'variables': {
            # 'network': init_node_i,
            'message_arrival': s_new_message,
 
        }
    },
    # {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # TIME
    #     'policies': {
    #         'time': p_time
    #     },
    #     'variables': {
    #         'timestamp': s_time,
    #     }
    # },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # SEND
        'policies': {
            'i_send_decison': p_send_i,
            'k_send_decision': p_send_kj, 
            'new_arrival': arrival_function,

        },
        'variables': {
            'arrival': arrival_current,
            'network': s_send_i,
        }
    },
        {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # STORE
        'policies': {
            'new_demand': demand_function,


        },
        'variables': {
            'demand': demand_current,
            'network': s_store_network_i,
            'message_list': message_global,
        }
    },
    {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # METRICS
        'policies': {
            # 'test': p_new_message,
        },
        'variables': {
            'gross_storage_demand': m_gross_storage,
            'least_storage_demand': m_least_storage,
           
        }
    },
]