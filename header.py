import json
import os
from tabulate import tabulate
from texttable import Texttable
import latextable

from zmq import NULL

# from numpy import source

root = os. getcwd()
thread_en = "threads/en/charliehebdo" 

with open("/Users/yu-hung/Downloads/pheme-rumour-scheme-dataset/Id-conversions/tweet_to_user.json") as file:
    tweet_to_user = json.load(file)

def getPath(): return str("/".join([root,thread_en]))
def getRoot(): return root

def makePath(arr) : return "/".join(arr)

def filtDir(data): 
    listdir = filter(lambda fname: not fname.startswith("."), data)
    return list(listdir)

def getListDir(path):
    sources = os.listdir(path)
    sources = filtDir(sources)
    return sources

def writeToJSON(path,fileName,data):
    with open(makePath([path,fileName+'.json']), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def writeToTxt(path,fileName,data):
    with open(makePath([path,fileName]), 'w') as f:
        f.write(data)

# Get the number of rumour and non-rumour source tweets 
def count():
    path = getPath()
    sources = getListDir(path)

    r=0
    nr=0

    for s in sources:
        with open(makePath([path,s,"annotation.json"])) as f:
            data = json.load(f)
            type = data["is_rumour"]
            
            if(type == "rumour"): r+=1
            if(type == "non-rumour"): nr+=1

# convert and merge all following relations into one JSON file
def followRelate():
    path = getPath()
    src = getListDir(path)

    ids = {}
    for s in src:
        with open(makePath([path,s,"who-follows-whom.dat"]),"r") as f:
            for data in f:
                follower = (data.split())[0]
                followee = (data.split())[1]

                try:
                    ids[follower].append(followee)
                except:
                    ids[follower] = [followee]

    writeToJSON(root,"relateIds",ids)    

def is_follower_react(followingRelate):
    path = getPath()
    src = getListDir(path)

    dic = {}
    for s in src:
        reactPath = makePath([path,s,"reactions"])
        reacts = getListDir(reactPath)

        for r in reacts:
            with open(makePath([reactPath,r])) as f:
                data = json.load(f)
                # the person who reacted
                followerId = (data["user"])["id_str"] 
                # the person being responded
                followeeId = data['in_reply_to_user_id_str']

            try: 
                followees = followingRelate[followerId]
                # if not(followeeId in followees):
                try:
                    dic[s].append(data["id_str"])
                except:
                    dic[s] = [data["id_str"]]
            except:
                continue

    writeToJSON(root,"org_reactions",dic)

''' Extracting annotations that belong to Charlie Hebdo event
param:
    event: name of the event
    path: path of the annotation file

returns: a json file will be created and saved in the root directory
'''
def extract_annotations(event, path):
    dic = {}
    filt_annot = []
    with open(path) as annots:
        annots = annots.readlines()
        for a in annots:
            if a[0] != "#": 
                annotations = json.loads(a)
                if annotations["event"] == event: filt_annot.append(annotations)
            else: 
                dic[a[2:-1]] = []
                filt_annot = dic[a[2:-1]]

    writeToJSON(root,"filtered_annotations",dic)

''' Organize the annotations based on conversation. Annotations for the same conversation will share the same source tweet id
param:
    annots : a dictionary containing all annotations from an event.

returns: a dictionary will be saved in the root directory
'''
def org_annotations(annots):
    sources = annots["Source Tweets"]
    direct_rep = annots["Direct Replies"]
    deep_rep = annots["Deep Replies"]
    dic = {}

    for s in sources:
        srcId = s["threadid"]
        dic[srcId] = {
            "Source Tweets": s,
            "Direct Replies":[],
            "Deep Replies":[]
        }

        direct_repList = []
        for d in direct_rep:
            if d["threadid"] == srcId:
                (dic[srcId])["Direct Replies"].append(d)
                direct_repList.append(d["tweetid"])
        
        for d in deep_rep:
            if d["threadid"] == srcId:
                (dic[srcId])["Deep Replies"].append(d)
    
    writeToJSON(root,"organized_annotations",dic)

def gen_idConversion():
    tweet_to_user = {}
    user_to_tweet = {}

    path = getPath()
    dir = getListDir(path)

    for d in dir:
        # source tweet
        sourcePath = makePath([path,d,"source-tweets"])
        source = getListDir(sourcePath)
        for s in source:
            with open(makePath([sourcePath,s])) as f:
                data = json.load(f)
                user = data["user"]
                tweetId = data["id_str"]
                userId = user["id_str"]

                try: user_to_tweet[userId].append(tweetId)
                except : user_to_tweet[userId] = [tweetId]

        # reactions
        reactionsPath = makePath([path,d,"reactions"])
        reactions = getListDir(reactionsPath)
        for r in reactions:
            with open(makePath([reactionsPath,r])) as f:
                data = json.load(f)
                user = data["user"]
                tweetId = data["id_str"]
                userId = user["id_str"]

                try: user_to_tweet[userId].append(tweetId)
                except : user_to_tweet[userId] = [tweetId]
    
    for user in user_to_tweet:
        tweets = user_to_tweet[user]
        for t in tweets:
            tweet_to_user[t] = user
    
    writeToJSON(root,"user_to_tweet",user_to_tweet)
    writeToJSON(root,"tweet_to_user",tweet_to_user)

def iter_structure(dic,structure,react_to,reacter):
    # empty dict
    if not(structure): return dic
    
    if react_to == NULL: 
        react_to = list(structure.keys())[0]
        return iter_structure(dic,structure[react_to],react_to,reacter)
        
    
    for r in structure.keys():
        # removes self-loops
        if tweet_to_user[react_to] == tweet_to_user[r]: continue
        
        try:
            dic[tweet_to_user[react_to]].append(tweet_to_user[r])

        except:
            dic[tweet_to_user[react_to]] = []
            dic[tweet_to_user[react_to]].append(tweet_to_user[r])
        
        dic = iter_structure(dic,structure[r],r,reacter)
    
    return dic
        
# Retreat who reacted by whom relations
def who_reacted_by_whom():
    thread_path = getPath()
    threads = getListDir(thread_path)
    
    who_reacted_by_whom = {}
    
    for thread in threads:
        with open(makePath([thread_path,thread,"structure.json"])) as f:
            data = json.load(f)
            who_reacted_by_whom = iter_structure(who_reacted_by_whom,data,NULL,NULL)
    
    return who_reacted_by_whom

# Return number of rumour and non-rumour followers count per bridge
def get_follower_counts(data,dataType):
    table = Texttable()
    table.set_cols_align(["c", "c", "c"])
    table.set_cols_valign(["t", "t", "t"])
    table.set_cols_dtype(dataType)

    headers = [["id","\#rumour followers","\#non-rumour followers"]]
    entries = []
    
    for id, values in data.items():
        entries.append([id,values["rum_count"],values["nonrum_count"]])
    
    headers.extend(entries)
    table.add_rows(headers)
    return latextable.draw_latex(table, caption="An example table.", label="table:example_table") 

# Return all bridges with non-zero betweenness centrality
def get_bridge_betweeness(data,dataType):
    table = Texttable()
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["t", "t"])
    table.set_cols_dtype(dataType)

    headers = [["id","betweeness"]]
    entries = []
    
    for id, values in data.items():
        if values["betweeness"] > 0: entries.append([id,values["betweeness"]])
    
    entries = sorted(entries, key=lambda x:x[1],reverse=True)
    headers.extend(entries)
    table.add_rows(headers)
    return latextable.draw_latex(table, caption="An example table.", label="table:example_table") 

def get_followers_centralities(data,dataType):
    table = Texttable()
    table.set_cols_align(["c", "c", "c"])
    table.set_cols_valign(["t", "t", "t"])
    table.set_cols_dtype(dataType)

    entries = []

    for id, values in data.items():
        if not(values["rumours"] or values["non_rumours"] or values["uncategorized"]): continue
        entries.append([id,"betweenness","centrality"])        

        if values["rumours"]: 
            entries.append(["rumours","",""])
            for follower, centralities in values["rumours"].items():
                entries.append([follower,centralities["betweeness"],centralities["closeness"]])

        if values["non_rumours"]: 
            entries.append(["non-rumours","",""])
            for follower, centralities in values["non_rumours"].items():
                entries.append([follower,centralities["betweeness"],centralities["closeness"]])
    
        if values["uncategorized"]: 
            entries.append(["uncategorized","",""])
            for follower, centralities in values["uncategorized"].items(): 
                entries.append([follower,centralities["betweeness"],""])
                entries.append(["","rumour","non-rumour"])
                entries.append(["",centralities["rum_closeness"],centralities["nonrum_closeness"]])

    table.add_rows(entries)
    return latextable.draw_latex(table, caption="", label="table:") 

def makeTable(cols_align,cols_valign,cols_dtype,data):
    table = Texttable()
    table.set_cols_align(cols_align)
    table.set_cols_valign(cols_valign)
    table.set_cols_dtype(cols_dtype)
    
    table.add_rows(data)
    return latextable.draw_latex(table, caption="", label="") 


