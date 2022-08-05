from trace import Trace
import networkx as nx
import matplotlib.pyplot as plt

def makeDiGraph(node_relations,communities):
    G = nx.DiGraph()
    
    for key, values in node_relations.items():
        for id in values["rumours"]: G.add_edge(id,key)
        for id in values["non_rumours"]: G.add_edge(id,key)
        for id in values["bridges"]: G.add_edge(id,key)
        for id in values["uncategorized"]: G.add_edge(id,key)

    # Node attributes
    attributes = {}
    for community, ids in communities.items(): 
        for id in ids: attributes[id] = community

    nx.set_node_attributes(G,attributes,"at")
    
    # Check for error
    for x,y in G.nodes(data=True):
        try: filt = y["at"]
        except: print(x)
    
    return G

'''
Input: Graph
Output: A dictionary organized by communities with in-degree centrality appended to each node
'''
def degree_centrality(G,type):
    if type == "in": in_degree = nx.in_degree_centrality(G)
    if type == "out": in_degree = nx.out_degree_centrality(G)

    degreeDict = {
        "rumours" : {},
        "non_rumours" : {},
        "bridges" : {},
        "uncategorized" : {}
    }
    for x,y in G.nodes(data=True):
        # Only accept nodes with centrality value > 0
        if in_degree[x] <= 0 : continue

        if y["at"] == "rumours": (degreeDict["rumours"])[x] = in_degree[x]
        elif y["at"] == "non_rumours": (degreeDict["non_rumours"])[x] = in_degree[x]
        elif y["at"] == "bridges": (degreeDict["bridges"])[x] = in_degree[x]
        elif y["at"] == "uncategorized": (degreeDict["uncategorized"])[x] = in_degree[x]
    
    # Sort each dict by in_degree centrality
    degreeDict["rumours"]=dict(sorted(degreeDict["rumours"].items(), key=lambda item: item[1],reverse=True))
    degreeDict["non_rumours"]=dict(sorted(degreeDict["non_rumours"].items(), key=lambda item: item[1],reverse=True))
    degreeDict["bridges"]=dict(sorted(degreeDict["bridges"].items(), key=lambda item: item[1],reverse=True))
    degreeDict["uncategorized"]=dict(sorted(degreeDict["uncategorized"].items(), key=lambda item: item[1],reverse=True))

    return degreeDict

def betweeness_centrality(G):
    betweeness = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)

    betweenessDict = {
        "rumours" : {},
        "non_rumours" : {},
        "bridges" : {},
        "uncategorized" : {}
    }
    for x,y in G.nodes(data=True):
        # Only accept nodes with centrality value > 0
        if betweeness[x] <= 0 : continue

        if y["at"] == "rumours": (betweenessDict["rumours"])[x] = betweeness[x]
        elif y["at"] == "non_rumours": (betweenessDict["non_rumours"])[x] = betweeness[x]
        elif y["at"] == "bridges": (betweenessDict["bridges"])[x] = betweeness[x]
        elif y["at"] == "uncategorized": (betweenessDict["uncategorized"])[x] = betweeness[x]
    
    # Sort each dict by in_degree centrality
    betweenessDict["rumours"]=dict(sorted(betweenessDict["rumours"].items(), key=lambda item: item[1],reverse=True))
    betweenessDict["non_rumours"]=dict(sorted(betweenessDict["non_rumours"].items(), key=lambda item: item[1],reverse=True))
    betweenessDict["bridges"]=dict(sorted(betweenessDict["bridges"].items(), key=lambda item: item[1],reverse=True))
    betweenessDict["uncategorized"]=dict(sorted(betweenessDict["uncategorized"].items(), key=lambda item: item[1],reverse=True))

    return betweenessDict

def closeness_centrality(G):
    closeness = nx.closeness_centrality(G)
    closenessDict = {
        "rumours" : {},
        "non_rumours" : {},
        "bridges" : {},
        "uncategorized" : {}
    }

    for x,y in G.nodes(data=True):
        # Only accept nodes with centrality value > 0
        if closeness[x] <= 0 : continue

        if y["at"] == "rumours": (closenessDict["rumours"])[x] = closeness[x]
        elif y["at"] == "non_rumours": (closenessDict["non_rumours"])[x] = closeness[x]
        elif y["at"] == "bridges": (closenessDict["bridges"])[x] = closeness[x]
        elif y["at"] == "uncategorized": (closenessDict["uncategorized"])[x] = closeness[x]
    
    # Sort each dict by in_degree centrality
    closenessDict["rumours"]=dict(sorted(closenessDict["rumours"].items(), key=lambda item: item[1],reverse=True))
    closenessDict["non_rumours"]=dict(sorted(closenessDict["non_rumours"].items(), key=lambda item: item[1],reverse=True))
    closenessDict["bridges"]=dict(sorted(closenessDict["bridges"].items(), key=lambda item: item[1],reverse=True))
    closenessDict["uncategorized"]=dict(sorted(closenessDict["uncategorized"].items(), key=lambda item: item[1],reverse=True))

    return closenessDict

def visualize(G,pos,labels,nodeColor,nodeSize,vertAlign,horAlign):
    if pos == None: pos = nx.spring_layout(G, k=0.8)
    
    nx.draw(G,pos,node_size=nodeSize,node_color=nodeColor,width=1.5)
    nx.draw_networkx_labels(G,pos,labels,font_size=13,font_color="red",verticalalignment=vertAlign,horizontalalignment=horAlign)
    x_values, y_values = zip(*pos.values())
    x_max = max(x_values)
    x_min = min(x_values)
    x_margin = (x_max - x_min) * 0.25
    plt.xlim(x_min - x_margin, x_max + x_margin)
    # plt.show()  