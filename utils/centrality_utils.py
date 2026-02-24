import networkx as nx
import igraph as ig
import json
import os

def load_network(file_path="../higgs-mention_network.edgelist"):
    network_file = open(file_path)
    network = nx.read_edgelist(network_file, create_using=nx.DiGraph(), data=(('weight', int),))
    return network

def get_in_degree_list(network):
    in_degree_list = list(network.in_degree())
    in_degree_list.sort(key=lambda x: x[1], reverse=True)
    return in_degree_list

def get_out_degree_list(network):
    out_degree_list = list(network.out_degree())
    out_degree_list.sort(key=lambda x: x[1], reverse=True)
    return out_degree_list

def get_betweenness_centrality_list(network):
    network_ig = ig.Graph.from_networkx(network)
    if os.path.exists("betweenness_centrality.json"):
        betweenness_list = json.load(open("betweenness_centrality.json", "r"))
    else:
        betweenness = network_ig.betweenness()
        betweenness_list = list(enumerate(betweenness))
        json.dump(betweenness_list, open("betweenness_centrality.json", "w"))
    betweenness_list.sort(key=lambda x: x[1], reverse=True)
    return betweenness_list

def get_eigenvector_centrality_list(network):
    network_ig = ig.Graph.from_networkx(network)
    if os.path.exists("eigenvector_centrality.json"):
        eigenvector_centrality_list = json.load(open("eigenvector_centrality.json", "r"))
    else:
        eigenvector_centrality = network_ig.eigenvector_centrality()
        eigenvector_centrality_list = list(enumerate(eigenvector_centrality))
        json.dump(eigenvector_centrality_list, open("eigenvector_centrality.json", "w"))
    eigenvector_centrality_list.sort(key=lambda x: x[1], reverse=True)
    return eigenvector_centrality_list
