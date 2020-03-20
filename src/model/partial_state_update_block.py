from .parts.timestamp import *
from .parts.demand import *
from .parts.store import *
from .parts.network_init import *
from .parts.message import *
from .parts.metrics import *
from .parts.route import *
from .parts.ping import *


partial_state_update_block = [
     {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PING and INIT
        'policies': {
            'availibilty': p_kj_availability,
            'ping_action' : p_ping,
        },
        'variables': {
            # 'network': init_node_i,
            'message_arrival': s_new_message,
            'network': s_ping,
 
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
            # 'network': s_send_i,
            'network': s_send_i_to_closest,
            'test': sent_list,

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
            'PO': m_po
           
        }
    },
]