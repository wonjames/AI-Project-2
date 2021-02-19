import networkx as nx


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def isColorable(G, max_color):
    
    first_node = None
    for i, n in enumerate(G.nodes()):
        if i == 0:
            first_node = n
            break
    # list of dict that holds the color:node values
    colors = []
    for n in G.nodes():
        d = {"colors": [x for x in range(max_color)], "node": n}
        colors.append(d)
    # sets the first node to color 0
    for c in colors:
        if(c["node"] == first_node):
            c["colors"] = 0
    #print(colors)
    node_info = build_dict(colors, key="node")
    #print(node_info)
    graph_list = list(G.neighbors(first_node))
    next_node = getNextNode(G, graph_list, first_node, node_info)
    setNodeColor(next_node, node_info)
    #print("next node: ", next_node)

    graph_list = list(G.neighbors(next_node))
    print(graph_list)
    next_node = getNextNode(G,graph_list, next_node, node_info)
    setNodeColor(next_node, node_info)
    #print("next node: ", next_node)
    
    graph_list = list(G.neighbors(next_node))
    print(graph_list)
    next_node = getNextNode(G,graph_list, next_node, node_info)
    setNodeColor(next_node, node_info)
    #print("next node: ", next_node)
    
    graph_list = list(G.neighbors(next_node))
    print(graph_list)
    next_node = getNextNode(G,graph_list, next_node, node_info)
    setNodeColor(next_node, node_info)
    #print("next node: ", next_node)
    
    print(node_info)
    #next_node = node_info.get(next_node)
    #setNodeColor(next_node)
    #print(next_node)
    #print(node_info)
    # get the neigbors colors it can still be (MRV)
    # choose the one with less choices
    # set it to a color
    # repeat for all neighbors

    #a = [0] * length
    #for i, n in enumerate(graph_list):
    #    l = list(G.neighbors(n))
    #    a[i] = len(l)
    #print(max(a))

def setNodeColor(node, node_info):
    
    node = node_info.get(node)
    
    if type(node['colors']) != int:
        color = node['colors'][0]
        node['colors'] = color
    print("node info: ", node_info)

def getNextNode(G, neighbors, node, node_info):
    # neighbors of A --> B, C
    mrv = 999
    next_node = None
    for n in neighbors:
        n_dict = node_info.get(n)
        n_dict['colors'] = removeColor(node_info.get(node), n_dict)
        if type(n_dict['colors']) == int:
            n_color_length = 999
        else:
            n_color_length = len(n_dict['colors'])
        if mrv > n_color_length:
            mrv = n_color_length
            next_node = n
    return next_node

def removeColor(n, n2):
    print(n['colors'])
    n_color = n['colors']
    n2_color = n2['colors']
    if type(n2_color) == int:
        if n_color == n2_color:
            n2_color.remove(n_color)
    else:
        if n_color in n2_color:
            n2_color.remove(n_color)
    return n2_color 

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge('A', 'B')
    G.add_edge('B', 'D')
    G.add_edge('A', 'C')
    G.add_edge('C', 'D')
    G.add_edge('B', 'E')
    isColorable(G, 3)
    