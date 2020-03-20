import operator

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



def route_table(network, own_node):
    """
    Collect XOR distance for each into a routing table
    [name,  id, bin(id), XOR distance from node, Proximity Order from node (shared prefix)]
    """
    own_id =  network.nodes[str(own_node)]['id']
    own_bin = format(own_id, '#06b')
    for node in network:
        node_id =  network.nodes[str(node)]['id']
        dist = distance_calc(own_id, node_id)
        # force leading zeros to nibble length, for proper determination of shared prefix
        node_bin = format(node_id, '#06b')
        prefix = shared_prefix([own_bin,node_bin])
        network.nodes[own_node]['routing_table'].append([node,node_id, node_bin, dist, prefix]) 
        # print(node,dist)
    return network.nodes[own_node]['routing_table']





# def bucket(node_table, min_range, max_range, k_size):


