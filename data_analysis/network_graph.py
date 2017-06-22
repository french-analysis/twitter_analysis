from collections import Counter
from pymongo import MongoClient
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

def connect_Mongo():
    print("Connecting to Mongo database")
    client = MongoClient()
    return client.twitter

def graph_add_tweet(DiGraph, tweet, nodes, followers):
    edge_start = int(tweet["user"])
    edge_ends = [int(id) for id in tweet["mentions_user"] if id in followers]
    nodes.append(edge_start)
    nodes += edge_ends 
    for edge_end in edge_ends:
        DiGraph.add_edge(edge_start, edge_end)
    if tweet["retweeted_user"] != "":
        nodes.append(int(tweet["retweeted_user"]))
        DiGraph.add_edge(edge_start, int(tweet["retweeted_user"]))
    return DiGraph, nodes

def get_interactions(main_id, followers):
    DG=nx.DiGraph()
    nodes = [main_id]
    for tweet in db.tweets.find():
        if tweet["user"] in followers:
            DG, nodes = graph_add_tweet(DG, tweet, nodes, followers)
    return DG, nodes

def get_followers_id(id):
    followers = []
    for link in db.followers.find({"followee" : id}):
        followers.append(link["follower"])
    return followers

if  __name__ == "__main__":

    db = connect_Mongo()
    main_id = "864042284505063424"

    followers = get_followers_id(main_id)
    DG, nodes = get_interactions(int(main_id), followers)
    
    nx.draw(DG,pos=nx.spring_layout(DG))
    print(nx.info(DG))
    plt.show()
