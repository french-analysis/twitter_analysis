from collections import Counter
from pymongo import MongoClient
from pprint import pprint
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
import random
import scipy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def connect_Mongo_twitter():
    print("Connecting to Mongo twitter database")
    client = MongoClient()
    return client.twitter

def connect_Mongo_prod():
    print("Connecting to Mongo prod database")
    client = MongoClient()
    return client.prod

def formatting(graph, main_id, followers):
    pr = nx.pagerank(graph, alpha = 0.85)
    graph_json = json_graph.node_link_data(graph)
    graph_prod = dict()
    graph_prod['nodes'] = []
    graph_prod['nodes'].append({
                'id' : str(main_id),
                'group' : 1,
                'rank' : 1
            })
    graph_prod['links'] = []
    for node in graph_json['nodes']:
        if node['id'] != main_id:
            if node['id'] in followers:
                graph_prod['nodes'].append({
                        'id' : str(node['id']),
                        'rank' : stats.percentileofscore(list(pr.values()), pr[node['id']]),
                        'group' : 2
                    })
            else:
                graph_prod['nodes'].append({
                        'id' : str(node['id']),
                        'rank' : stats.percentileofscore(list(pr.values()), pr[node['id']]),
                        'group' : 3
                    })
    for edge in graph_json['links']:
        graph_prod['links'].append({
                'source' : str(graph_prod['nodes'][edge['source']]['id']),
                'target' : str(graph_prod['nodes'][edge['target']]['id']),
                'value' : 1
            })
    return json.dumps(graph_prod)

def graph_add_tweet(DiGraph, tweet, nodes, followers):
    edge_start = int(tweet["user"])
    edge_ends = [int(id) for id in tweet["mentions_user"] if int(id) in followers]
    for edge_end in edge_ends:
        DiGraph.add_edge(edge_start, edge_end)
    if tweet["retweeted_user"] in followers:
        DiGraph.add_edge(edge_start, int(tweet["retweeted_user"]))
    return DiGraph

def get_followers_id(id, db):
    followers = []
    for link in db.followers.find({"followee" : id}):
        followers.append(int(link["follower"]))
    return followers

def build_graph(main_id, db):
    followers = get_followers_id(main_id, db)
    DG=nx.DiGraph()
    nodes = [int(main_id)]
    i = 0
    for tweet in db.tweets.find():
        if int(tweet["user"]) in followers:
            DG = graph_add_tweet(DG, tweet, nodes, followers)
            i += 1
    print(nx.info(DG))
    return formatting(DG, main_id, followers)

def export_graph_prod(id, graph, db):
    db.graphs.update(
        { 'id' : str(id) },
        {
            '$set' : { 'graph' : graph }
        },
        upsert = True)
    return

if  __name__ == "__main__":

    tweets = connect_Mongo_twitter()
    main_id = "864042284505063424"

    DG_str = build_graph(main_id, tweets)

    prod = connect_Mongo_prod()
    export_graph_prod(main_id, DG_str, prod)
