import networkx as nx

# method that creates a key for the dictionary to index by
# from: https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def isColorable(G, max_color):
    # manually gets the first node
    first_node = None
    max_neighbor = 0
    for i, n in enumerate(G.nodes()):
        length = len(list(G.neighbors(n)))
        if max_neighbor <= length:
            max_neighbor = length
            first_node = n

    # list of dict that holds the color:node values
    colors = []
    for n in G.nodes():
        d = {"colors": [x for x in range(max_color)], "node": n}
        colors.append(d)

    # sets the first node to color 0
    for c in colors:
        if(c["node"] == first_node):
            c["colors"] = 0
    # this builds the a key dictionary
    node_info = build_dict(colors, key="node")
    # gets the neighbors of the node
    graph_list = list(G.neighbors(first_node))
    # calls the recursive function that assigns the colors to the nodes
    getNextNode(G, graph_list, first_node, node_info, 0)
    # if any of the nodes has an empty color array, then the graph is not colorable
    print("Final Graph: ", node_info)
    for n in node_info:
        node = node_info.get(n)
        if node['colors'] == []:
            return False
    return True

# sets the node color to the first available color
def setNodeColor(node, node_info, index):
    node = node_info.get(node)
    if type(node['colors']) != int and len(node['colors']):
        color = node['colors'][index]
        node['colors'] = color

# recursive function that finds the next node
def getNextNode(G, neighbors, node, node_info, v):
    # base case: we have gone through the entire graph
    if v == len(G.nodes):
        return True
    # min remaining value: based on number of colors the neighbors can be
    # set as 999 initially
    mrv = 999
    arr = []
    # goes through the neighbors one by one removes the current nodes color from the neighbors color array 
    for n in neighbors:
        n_dict = node_info.get(n)
        n_dict['colors'] = removeColor(node_info.get(node), n_dict)
        # we have removed the last remaining color in array, thus the graph cannot be colored
        if n_dict['colors'] == []:
            return False
        # if the n_dict['colors'] returns as an int, then there is only one possibility for the color
        # therefore it is already set
        if type(n_dict['colors']) == int:
            n_color_length = 999
        else:
            n_color_length = len(n_dict['colors'])
        # adds the node and mrv to a list of dict to be looped through later
        mrv_dict = {"node": n, "mrv": n_color_length, "colors":n_dict['colors']}
        arr.append(mrv_dict)

    # this loops through the array of neighbor nodes 
    # finds the mrv node, pops it from the array when we back track
    # we don't go back to the same node
    for i in range(len(arr)):
        min_mrv = 999
        neighbor_length = -1
        index = 0
        for iter, x in enumerate(arr):
            mrv = x['mrv']
            n_len = len(list(G.neighbors(x['node'])))
            # if there is a tie we choose the one with more connections
            if mrv == min_mrv:
                if neighbor_length < n_len:
                    node = x
                    index = iter
            if mrv < min_mrv:
                min_mrv = mrv
                node = x
                index = iter
                neighbor_length = n_len
        if min_mrv == 999:
            continue
        if len(arr):
            arr.pop(index)
        # gets the neighbors of the new node
        graph_list = list(G.neighbors(node['node']))
        # sets the color based off of LCV
        findLCV(node['node'], graph_list, node_info)
        # recursively goes to the next node
        if getNextNode(G,graph_list, node['node'], node_info, v+1) == True:
            return True
    return False

# finds the least constraint value and sets the node color to that value
def findLCV(node, neighbors, node_info):
    node = node_info.get(node)
    if type(node['colors']) == int:
        setNodeColor(node['node'], node_info, 0)
        return
    if not len(node['colors']): 
        return
    lcv_array = [0]*len(node['colors'])
    for n in neighbors:
        n = node_info.get(n)
        for i,color in enumerate(node['colors']):
            if type(n['colors']) == int:
                if color == n['colors']:
                    lcv_array[i] += 1
            else:
                if color in n['colors']:
                    lcv_array[i] += 1
    index = lcv_array.index(min(lcv_array))
    setNodeColor(node['node'], node_info, index)

    
# removes the unavailable colors from the neighbors once the node is assigned a color
def removeColor(n, n2):
    n_color = n['colors']
    n2_color = n2['colors']
    # if the type is int and we are removing it, then the array is empty and the graph is not colorable
    if type(n2_color) == int:
        if n_color == n2_color:
            return []
    else:
        if n_color in n2_color:
            n2_color.remove(n_color)
        
    return n2_color 

if __name__ == '__main__':
    G = nx.Graph()
    file = open("graph4.txt", "r")
    color = 0
    for i,line in enumerate(file):
        if "colors =" in line:
            color = [int(s) for s in line.split() if s.isdigit()]
            
        if i > 3:
            edge = [int(s) for s in line.split(',')]
            G.add_edge(edge[0], edge[1])
           
    coloring = isColorable(G, color[0])
    if coloring:
        print('Graph is colorable')
    else:
        print('Graph is not colorable')