import json
import os

# from numpy import source

root = os. getcwd()
thread_en = "threads/en/charliehebdo" 

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

def extract_annotations(event,path):
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

