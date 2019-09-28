#Resources: https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
import networkx as nx

def max_flow(residual, s, t):
    max_flow = 0
    parent = {}
    for node in residual:
        parent[node] = "none"
        
    while augmenting_path(residual, s, t, parent) == True:
        v = t
        max_flow += 1
        while v != s:
            u = parent[v]
            residual[u].get(v)['capacity'] -= 1
            residual[v].get(u)['capacity'] += 1
            v = parent[v]
    
    flow_dict = []
    #print(residual.adj)
    for v, vals in residual[s].items():
        if vals['capacity'] == 0:
            for u, vals2 in residual[v].items():
                if vals2['capacity'] == 0:
                    flow_dict.append(str(u[1]) + ' ' + str(u[0]) + ' ' + str(v[1]) + ' ' + str(v[0]))

    #done = []
    #for u in residual:
    #    for v, vals in residual[u].items():
    #        if vals['capacity'] == 1:
    #            done.append((u,v))
    #            if (v,u) not in done:
    #                flow_dict.append(str(v[1]) + ' ' + str(v[0]) + ' ' + str(u[1]) + ' ' + str(u[0]))
    return max_flow, flow_dict

def augmenting_path(residual, s, t, parent):
    Q = []
    Q.append(s)
    visited = []
    visited.append(s)
    
    while Q:
        u = Q.pop(0)
        for v, vals in residual[u].items():
            if v not in visited and vals['capacity'] > 0: 
                Q.append(v) 
                visited.append(v)
                parent[v] = u
    
    if t in visited:
        return True
    return False