import operator
import numpy as np

# CLASSICAL
def distance_calc(own_id, neighbor_id):
    """
    Get the distance between own node and its neighbors.
    Using XOR Logic
    """
    return own_id ^ neighbor_id

# RECURSIVE
# Proximity Order for Forwarding Kademlia
def shared_prefix(args):
    """
    Find the shared prefix between the binary strings of node ids.
    Enter list of ids
    Returns bin of shared prefix
    """
    i = 0
    while i < min(map(len, args)):
        if len(set(map(operator.itemgetter(i), args))) != 1:
            break
        i += 1
    return args[0][:i]

def route_table_peer(network, own_node):
    """
    Collect XOR distance for each into a routing table
    [name,  id, bin(id), XOR distance from node, Proximity Order from node (shared prefix), Trust]
    """
    own_id =  network.nodes[str(own_node)]['id']
    own_bin = format(own_id, '#06b')
    for node in network:
        node_id =  network.nodes[str(node)]['id']
        dist = distance_calc(own_id, node_id)
        # force leading zeros to nibble length, for proper determination of shared prefix
        node_bin = format(node_id, '#06b')
        prefix = shared_prefix([own_bin,node_bin])
        print(own_node,node)
        if own_node == 'p':
            trust = 1        
        elif own_node != node:
            trust = network[own_node][node]['trust'] 
        else:
            trust = 1

        network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix, trust]) 
    print('init routing table', own_node, network.nodes[own_node]['routing_table'])
    return  network.nodes[own_node]['routing_table']

def route_table(network, own_node, peer):
    """
    Collect XOR distance for each into a routing table
    [name,  id, bin(id), XOR distance from node, Proximity Order from node (shared prefix), Trust]
    """
    # own_id =  network.nodes[str(own_node)]['id']
    # own_bin = format(own_id, '#06b')
    # for node in network:
    #     node_id =  network.nodes[str(node)]['id']
    #     dist = distance_calc(own_id, node_id)
    #     # force leading zeros to nibble length, for proper determination of shared prefix
    #     node_bin = format(node_id, '#06b')
    #     prefix = shared_prefix([own_bin,node_bin])
    #     print(own_node,node)
    #     if own_node == 'p':
    #         trust = 1        
    #     elif own_node != node:
    #         trust = network[own_node][node]['trust'] 
    #     else:
    #         trust = 1

    #     network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix, trust]) 
    #     # print(node,dist)

    own_id =  network.nodes[str(own_node)]['id']
    own_bin = format(own_id, '#06b')
    for node in network:
        print(node)
        if own_node == 'i' and network.nodes[node]['role'] == peer:
            node_id =  network.nodes[str(node)]['id']
            dist = distance_calc(own_id, node_id)
            # force leading zeros to nibble length, for proper determination of shared prefix
            node_bin = format(node_id, '#06b')
            prefix = shared_prefix([own_bin,node_bin])
            print(own_node,node)
            if own_node == 'p':
                trust = 1        
            elif own_node != node:
                trust = network[own_node][node]['trust'] 
            else:
                trust = 1

            network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix, trust]) 
        # print(node,dist)
    return network.nodes[own_node]['routing_table']

def remove_from_route_table(network, own_node): #, target_node):
    """
    Collect XOR distance for each into a routing table
    [name,  id, bin(id), XOR distance from node, Proximity Order from node (shared prefix), Trust]
    """
    own_id =  network.nodes[str(own_node)]['id']
    own_bin = format(own_id, '#06b')
    for node in network:
        print(node)
        # if own_id == 'i' and 
        node_id =  network.nodes[str(node)]['id']
        dist = distance_calc(own_id, node_id)
        # force leading zeros to nibble length, for proper determination of shared prefix
        node_bin = format(node_id, '#06b')
        prefix = shared_prefix([own_bin,node_bin])
        print(own_node,node)
        if own_node == 'p':
            trust = 1        
        elif own_node != node:
            trust = network[own_node][node]['trust'] 
        else:
            trust = 1

        network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix, trust]) 
        # print(node,dist)
    return network.nodes[own_node]['routing_table']

def add_to_route_table(network, own_node, target_node):
    """
    Collect XOR distance for each into a routing table
    [name,  id, bin(id), XOR distance from node, Proximity Order from node (shared prefix), Trust]
    """
    own_id =  network.nodes[str(own_node)]['id']
    own_bin = format(own_id, '#06b')
    for node in network:
        node_id =  network.nodes[str(node)]['id']
        dist = distance_calc(own_id, node_id)
        # force leading zeros to nibble length, for proper determination of shared prefix
        node_bin = format(node_id, '#06b')
        prefix = shared_prefix([own_bin,node_bin])
        print(own_node,node)
        if own_node == 'p':
            trust = 1        
        elif own_node != node:
            trust = network[own_node][node]['trust'] 
        else:
            trust = 1

        network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix, trust]) 
        # print(node,dist)
    return network.nodes[own_node]['routing_table']



def outbound_traffic(node_name):
    '''
    Sweep of adjacent nodes from given node_name, sum of outbound traffic.
    Must have OUTBOUND edges defined with 'traffic' attribute from given node
    '''
    total_traffic = 0
    for nbr, eattr in node_name.items():
        # [1] just for size
        total_traffic += eattr['traffic']

    return total_traffic

def inbound_traffic(out_node_name, in_node_name):
    '''
    Sweep of adjacent nodes from one given node_name, sum of inbound traffic.
    Must have OUTBOUND edges defined with 'traffic' attribute from given node
    Convert to a sweep of all nodes, with identified inbound node.
    '''
    total_traffic = 0
    for nbr, eattr in out_node_name.items():
        # [1] just for size
        if nbr == in_node_name:
            total_traffic += eattr['traffic']

    return total_traffic

def cart_to_pol(x, y):
    """
    Convert from cartesian to polar coordinates
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def pol_to_cart(r, theta):
    """
    Convert from polar to cartesian coordinates
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

def calc_z_scores(array):
    zees = np.zeros_like(array, dtype = float)

    for count,item in enumerate(array):
        z_index = count + 1
        z_score = stats.zscore(array[0:z_index])

        if count != 0: 
            zees[count] = z_score.item(count) 
    return zees

def calc_incentive(x_dist, y_dist):

    incentive = np.zeros(len(x_dist))
    for n in range(len(x_dist)):
        if x_dist[n] < 0:
            # reward = + incentive
            incentive[n] = np.abs(x_dist[n]) + np.abs(y_dist[n])
        else:
            # tax = -incentive 
            incentive[n] = - (np.abs(x_dist[n]) + np.abs(y_dist[n]))
    return incentive

# def bucket(node_table, min_range, max_range, k_size):

class History(): #args Event
    """
    History class for states of message requests (Parent to Event)
    """          
    def __init__ (self): #, sending_node='i'):#, receiving_node='j', hash_file=2, size=3, block_init=4, reward=5):
        """
        Initiate event instance
        """        
        self.active = []
        self.located = []
        self.routed = []
        self.solved = []
        self.paid = []
        self.not_paid = []
    
    def add_to_active(self, Event):#sending_node='i', receiving_node='j', hash_file=2, size=3, reward=5, block_init=4):
        """
        Initiate a new event message request with:
        sending_node='i'
        receiving_node='j'
        hash of file, 
        size of file(# of chunks
        offered token reward
        time of request (block_init)
        """
        self.active.append(Event)

    def add_to_located(self, Event):#sending_node='i', receiving_node='j', hash_file=2, size=3, reward=5, block_init=4):
        """
        Initiate a new event message request with:
        sending_node='i'
        receiving_node='j'
        hash of file, 
        size of file(# of chunks
        offered token reward
        time of request (block_init)
        """
        self.active.remove(Event) 
        self.located.append(Event)
    
    def add_to_routed(self,Event): #storing_node = 'k',  route_list = [], block_end = 9):
        """
        Complete a message routing event with:
        identity of storing node k
        proving node p
        list of nodes in route
        block at completion
        """
        # Pop from active as completed
        
        
        self.located.remove(Event) 
        self.routed.append(Event)
#         del self.active(Event)
        
    def add_to_solved(self,Event): #storing_node = 'k', proving_node = 'p', route_list = [], block_end = 9):
        """
        Complete a message solving event with:
        identity of proving node p
        list of nodes in route
        block at completion
        """
        self.routed.remove(Event) 
        self.solved.append(Event)
        
    def add_to_paid(self,Event): #storing_node = 'k', proving_node = 'p', route_list = [], block_end = 9):
        """
        Complete a message paid event with:
        Paying escrow  + subsidy - tax to allocated nodes
        """
        self.solved.remove(Event) 
        self.paid.append(Event)

    def add_to_not_paid(self,Event): #storing_node = 'k', proving_node = 'p', route_list = [], block_end = 9):
        """
        Complete a message not_paid event due to failure, ex. funds not being there, time-out of route not being posted for proof?:
        Use to update trust score of bad nodes
        """
        self.solved.remove(Event) 
        self.not_paid.append(Event)
                
    def __str__(self):
        """
        Print all attributes of an event
        """
        return str(self.__class__) + ": " + str(self.__dict__)

class Event(History): #args
    """
    Event class for message requests (Child class to History parent Class)
    """  
    def __init__(self, sending_node='i', receiving_node='j', hash_file=2, size=3, block_init=4, escrow=5):
        """
        Initiate event instance a new event message request with:
        sending_node='i'
        receiving_node='j'
        hash of file, 
        size of file(# of chunks         
        offered token reward
        time of request (block_init)
        """        
        self.sending_node =  sending_node
        self.receiving_node = receiving_node
        self.hash_file = hash_file
        self.size = size
        self.block_init = block_init
        self.escrow = escrow
        self.sender_pledge = escrow

#     def initiate(self, sending_node='i', receiving_node='j', hash_file=2, size=3, reward=5, block_init=4):
#         """
#         Initiate a new event message request with:
#         sending_node='i'
#         receiving_node='j'
#         hash of file, 
#         size of file(# of chunks
#         offered token reward
#         time of request (block_init)
#         """
#         self.sending_node =  sending_node
#         self.receiving_node = receiving_node
#         self.hash_file = hash_file
#         self.size = size
#         self.reward = reward
#         self.block_init = block_init    
#         return self

    def locate(self, storing_node = 'k', block_locate=4):
        """
        Initiate a new event message request with:
        sending_node='i'
        receiving_node='j'
        hash of file, 
        size of file(# of chunks
        offered token reward
        time of request (block_init)
        """
        self.storing_node = storing_node
        self.block_locate = block_locate
        time = block_locate - self.block_init
        self.time_to_find = time 
    
    def complete(self,storing_node = 'k', route_list = [], block_route = 9):
        """
        Complete a message routing event with:
        identity of stroing node k
        proving node p
        list of nodes in route
        block at completion
        """
        self.storing_node = storing_node
        self.route_list = route_list
        self.block_route = block_route
        time = self.block_route - self.block_locate
        self.time_to_route = time
        
    def prove(self, proving_node = 'p', block_prove = 9):
        self.proving_node = proving_node
        self.block_prove = block_prove
        time = self.block_prove - self.block_route
        self.time_to_prove = time
        self.total_time = self.time_to_find + self.time_to_route + self.time_to_prove

    def incentive(self, tax = 0, subsidy = 0):
        """
        Update escrow for message with tax and subsidy.
        Tax is negative
        Subsidy is positive
        """
#         self.tax_sub = tax_sub
        self.delta = tax - subsidy
        self.escrow += subsidy - tax  
                
                
    def __str__(self):
        """
        Print all attributes of an event
        """
        return str(self.__class__) + ": " + str(self.__dict__)