from collections import Counter
from pymongo import MongoClient
from pprint import pprint
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

def connect_Mongo_twitter():
    print("Connecting to Mongo twitter database")
    client = MongoClient()
    return client.twitter

def connect_Mongo_prod():
    print("Connecting to Mongo prod database")
    client = MongoClient()
    return client.prod

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

def get_interactions(main_id, followers, db):
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

def export_graph_prod(id, graph, db):
    db.graphs.update(
        { 'id' : str(id) },
        {
            '$set' : { 'graph' : graph }
        },
        upsert = True)
    return

def to_json(graph):
    return json.dumps(json_graph.node_link_data(graph))
     

if  __name__ == "__main__":

    db = connect_Mongo_twitter()
    main_id = "864042284505063424"

    followers = get_followers_id(main_id)
    DG, nodes = get_interactions(int(main_id), followers, db)

    DG_json = to_json(DG)

    prod = connect_Mongo_prod()
    export_graph_prod(main_id, DG_json, prod)

    print(nx.info(DG))
    plt.show()
