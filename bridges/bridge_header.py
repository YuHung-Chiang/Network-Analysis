def getType1 (data):
    for d in list(data):
        if len((data[d])["rumours"])>0 and len((data[d])["non_rumours"])>0:
            continue
        else:
            data.pop(d)

    return data

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
                nonrumour[id] = {} 
                (nonrumour[id])["betweeness"] = b
                (nonrumour[id])["rum_closeness"] = rum_c
                (nonrumour[id])["nonrum_closeness"] = nonrum_c
        
    return centralities