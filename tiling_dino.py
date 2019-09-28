#Collaborators: Dillon Liu, Emily Nguyen
import max_flow as mf
import networkx as nx
def tile_image(file_lines):
    G = nx.DiGraph()
    residual = nx.DiGraph()
    black_nodes = []
    white_nodes = []
    for j in range(len(file_lines)):
        for i in range(len(file_lines[0])-1):
            if file_lines[j][i] == '#':
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    black_nodes.append((j,i))
                elif (i % 2 != 0 and j % 2 == 0) or (i % 2 == 0 and j % 2 != 0):
                    white_nodes.append((j,i))
                G.add_node((j,i))
                #residual.add_node((j,i))
                residual.add_node((j,i))
    
    for node in black_nodes:
        neighbors = get_neighbors(node, G)
        for neighbor in neighbors:
            G.add_edge(node, neighbor, capacity=1.0)
            residual.add_edge(node, neighbor, capacity=1.0)
            residual.add_edge(neighbor, node, capacity=0)

    G.add_node("source")
    G.add_node("sink")
    for node in black_nodes:
        G.add_edge("source", node, capacity=1.0)
        residual.add_edge("source", node, capacity=1.0)
        residual.add_edge(node, "source", capacity=0)
    for node in white_nodes:
        G.add_edge(node, "sink", capacity=1.0)
        residual.add_edge(node, "sink", capacity=1.0)
        residual.add_edge("sink", node, capacity=0)
    
    #flow_value, flow_dict = nx.maximum_flow(G, "source", "sink")
    flow_value, flow_dict = mf.max_flow(residual, "source", "sink")
    #print(flow_value)
    #tiles = []
    if flow_value * 2 != G.__len__() - 2: 
        return ["impossible"]
    else: 
        return flow_dict
    '''
        for u in black_nodes:
            for v in white_nodes:
                if G.has_edge(u,v):
                    if flow_dict[u][v] == 1.0:
                        tiles.append(str(v[1]) + ' ' + str(v[0]) + ' ' + str(u[1]) + ' ' + str(u[0])) 
        return tiles '''
        

def get_neighbors(node, graph):
    neighbors = []
    for i in range(-1,2):
        if (i != 0):
            if graph.__contains__((node[0] + i, node[1])):
                neighbors.append((node[0] + i, node[1]))
            if graph.__contains__((node[0], node[1]+i)):
                neighbors.append((node[0], node[1]+i))
    return neighbors