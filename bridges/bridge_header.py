def getType1 (data):
    for d in list(data):
        if len((data[d])["rumours"])>0 and len((data[d])["non_rumours"])>0:
            continue
        else:
            data.pop(d)

    return data

def getFollows(data,follows,communities):
    follows = {}
    for id in list(data):
        follows[id] = {
            "rumours":[],
            "non_rumours":[],
            "bridges":[],
            "uncategorized":[]
        }
        try: followsList = follows[id]
        except: continue

        for f in followsList:
            if f in communities["rumours"]: (follows[id])["rumours"].append(f)
            elif f in communities["non_rumours"]: (follows[id])["non_rumours"].append(f)
            elif f in communities["bridges"]: (follows[id])["bridges"].append(f)
            elif f in communities["uncategorized"]: (follows[id])["uncategorized"].append(f)
    
    return follows

def originateFrom(data,communities):
    origin = {
            "rumours":[],
            "non_rumours":[],
            "uncategorized":[]
        }

    for id in list(data):
        if id in communities["rumours"]: origin["rumours"].append(id)
        elif id in communities["non_rumours"]: origin["non_rumours"].append(id)
        elif id in communities["uncategorized"]: origin["uncategorized"].append(id)
    
    return origin

def tweets_type(data,tweets_types):
    types = {}
    for id in list(data):
        types[id] = {}
        if id in (tweets_types["Source_Tweets"].keys()): 
            (types[id])["Source_Tweets"] = (tweets_types["Source_Tweets"])[id]
        else: (types[id])["Source_Tweets"] = 0

        if id in (tweets_types["Reply_Tweets"].keys()): 
            (types[id])["Reply_Tweets"] = (tweets_types["Reply_Tweets"])[id]
        else: (types[id])["Reply_Tweets"] = 0
    
    return types

def getType2 (data,follow_relation,communities):
    for id in list(data):
        values = data[id]
        # XOR operation
        if (len(values["rumours"]) > 0) ^ (len(values["non_rumours"]) > 0):
            try: follows = follow_relation[id]
            except: 
                data.pop(id)
                continue
            
            if len(values["rumours"]) > 0:
                if not len(set(follows).intersection(set(communities["non_rumours"]))): data.pop(id)
            
            else: 
                if not len(set(follows).intersection(set(communities["rumours"]))): data.pop(id)
        
        else: data.pop(id)


    return data

def getType3(data, communities):
    type3 = {}
    for id, values in data.items():
        if id in communities["uncategorized"]:
            type3[id] = values
    
    return type3

def get_centralities(bridges,betweeness,nonrum_closeness,rum_closeness,uncat_nonrum_closeness,uncat_rum_closeness):
    centralities = {}

    for bridge, values in bridges.items():
        centralities[bridge] = {
            "rum_count": len(values["rumours"]),
            "nonrum_count": len(values["non_rumours"]),
            "rumours": {},
            "non_rumours": {},
            "uncategorized": {}
        }
        try: (centralities[bridge])["betweeness"] = (betweeness["bridges"])[bridge]
        except: (centralities[bridge])["betweeness"] = 0.0

        rumour = (centralities[bridge])["rumours"]
        for id in values["rumours"]:
            try: b = (betweeness["rumours"])[id]
            except: b = 0.0

            try: c = (rum_closeness["rumours"])[id]
            except: c = 0.0

            if (b > 0) or (c > 0):
                rumour[id] = {} 
                (rumour[id])["betweeness"] = b
                (rumour[id])["closeness"] = c
        
        nonrumour = (centralities[bridge])["non_rumours"]
        for id in values["non_rumours"]:
            try: b = (betweeness["non_rumours"])[id]
            except: b= 0.0

            try: c = (nonrum_closeness["non_rumours"])[id]
            except: c = 0.0
            
            if (b > 0) or (c > 0):
                nonrumour[id] = {} 
                (nonrumour[id])["betweeness"] = b
                (nonrumour[id])["closeness"] = c

        uncat = (centralities[bridge])["uncategorized"]
        for id in values["uncategorized"]:
            try: b = (betweeness["uncategorized"])[id]
            except: b = 0.0

            try: rum_c = (uncat_rum_closeness["uncategorized"])[id]
            except: rum_c = 0.0

            try: nonrum_c = (uncat_nonrum_closeness["uncategorized"])[id]
            except: nonrum_c = 0.0

            if (b > 0) or (rum_c > 0)  or (nonrum_c > 0):
                uncat[id] = {} 
                (uncat[id])["betweeness"] = b
                (uncat[id])["rum_closeness"] = rum_c
                (uncat[id])["nonrum_closeness"] = nonrum_c
        
    return centralities