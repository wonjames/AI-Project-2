import networkx as nx


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def isColorable(G, max_color):
    # manually gets the first node
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
    # this builds the a key dictionary
    node_info = build_dict(colors, key="node")
    # gets the neighbors of the node
    graph_list = list(G.neighbors(first_node))
    getNextNode(G, graph_list, first_node, node_info, 0)
    for n in node_info:
        var = node_info.get(n)
        if var['colors'] == []:
            print("Graph is not colorable")
            return
    print("Graph is colorable! Final: ", node_info)

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
    # goes through the neighbors one by one
    for n in neighbors:
        n_dict = node_info.get(n)
        n_dict['colors'] = removeColor(node_info.get(node), n_dict)
        if n_dict['colors'] == []:
            return False
        # if the n_dict['colors'] returns as an int, then there is only one possibility for the color
        # therefore it is already set
        if type(n_dict['colors']) == int:
            n_color_length = 999
        else:
            n_color_length = len(n_dict['colors'])
        # adds the node and mrv to a list of dict to be looped through later
        mrv_dict = {"node": n, "mrv": n_color_length}
        arr.append(mrv_dict)
    # this loops through the array of neighbor nodes 
    # finds the mrv node, pops it from the array when we back track
    # we don't go back to the same node
    for i in range(len(arr)):
        min_mrv = 999
        node = arr[0]
        var = 0
        for iter, x in enumerate(arr):
            mrv = x['mrv']
            if mrv < min_mrv:
                min_mrv = mrv
                node = x
                var = iter
        if min_mrv == 999:
            return True
        if len(arr):
            arr.pop(var)
        # gets the neighbors
        graph_list = list(G.neighbors(node['node']))
        findLCV(node['node'], graph_list, node_info)
        # sets the color for the current node
        #setNodeColor(node['node'], node_info)
        #print("Next Node:", i, node)
        #print('Nodes neighbors: ', graph_list)
        # recursively goes to the next node
        if getNextNode(G,graph_list, node['node'], node_info, v+1) == True:
            return True
    return False

def findLCV(node, neighbors, node_info):
    #print("neighbor: ", neighbors)
    #print("node: ", node)
    #print("node_info: ", node_info)
    
    node = node_info.get(node)
    if not len(node['colors']): 
        print(node) 
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
    #print("LCV array index: ", index)
    setNodeColor(node['node'], node_info, index)

    
# removes the unavailable colors from the neighbors once the node is assigned a color
def removeColor(n, n2):
    n_color = n['colors']
    n2_color = n2['colors']
    # n2_color can either be an array of numbers(colors) or be a single int
    if type(n2_color) == int:
        if n_color == n2_color:
            n2_color.remove(n_color)
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
            print(color)
        if i > 3:
            edge = [int(s) for s in line.split(',')]
            G.add_edge(edge[0], edge[1])
            print(edge)
    isColorable(G, color[0])
    