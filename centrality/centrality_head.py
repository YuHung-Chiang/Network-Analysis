import networkx as nx

def makeDiGraph(node_relations,community):
    G = nx.DiGraph()
    
    for key, values in node_relations.items():
        if key in community["rumours"]: G.add_node(key,at="rumours")
        elif key in community["non_rumours"]:  G.add_node(key,at="non_rumours")
        elif key in community["bridges"]: G.add_node(key,at="bridges")
        elif key in community["uncategorized"]: G.add_node(key,at="uncategorized")
        
        for id in values["rumours"]:
            G.add_node(id,at="rumours")
            G.add_edge(id,key)
        
        for id in values["non_rumours"]:
            G.add_node(id,at="non_rumours")
            G.add_edge(id,key)
        
        for id in values["bridges"]:
            G.add_node(id,at="bridges")
            G.add_edge(id,key)
        
        for id in values["uncategorized"]:
            G.add_node(id,at="uncategorized")
            G.add_edge(id,key)
    
    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)
    return G

'''
Input: Graph
Output: A dictionary organized by communities with in-degree centrality appended to each node
'''
def indegree_centrality(G):
    in_degree = nx.in_degree_centrality(G)
    in_degreeDict = {
        # "rumours" : [x for x,y in G.nodes(data=True) if y['at']=="rumour"]
        # "non_rumours" : [x for x,y in G.nodes(data=True) if y['at']=="non_rumours"],
        # "bridges" : [x for x,y in G.nodes(data=True) if y['at']=="bridges"],
        # "uncategorized" : [x for x,y in G.nodes(data=True) if y['at']=="uncategorized"],
    }
    # in_degreeDict["rumours"] = [x for x,y in G.nodes(data=True) if y['at']=="rumour"]
    # in_degreeDict["non_rumours"] = [x for x,y in G.nodes(data=True) if y['at']=="non_rumours"]
    # in_degreeDict["bridges"] = [x for x,y in G.nodes(data=True) if y['at']=="bridges"]
    # in_degreeDict["uncategorized"] = [x for x,y in G.nodes(data=True) if y['at']=="uncategorized"]
    print([x for x,y in G.nodes(data=True) if y['at']=="rumour"])
    return in_degreeDict