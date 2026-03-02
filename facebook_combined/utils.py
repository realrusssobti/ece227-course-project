import networkx as nx
import igraph as ig
import json
import os

def load_network(file_path="../higgs-mention_network.edgelist"):
    network_file = open(file_path)
    network = nx.read_edgelist(network_file, create_using=nx.Graph())
    return network

def get_degree_list(network):
    degree_list = list(network.degree())
    degree_list.sort(key=lambda x: x[1], reverse=True)
    return degree_list

def get_betweenness_centrality_list(network):
    network_ig = ig.Graph.from_networkx(network)
    #if os.path.exists("betweenness_centrality.json"):
    #    betweenness_list = json.load(open("betweenness_centrality.json", "r"))
    #else:
    #    betweenness = network_ig.betweenness()
    #    betweenness_list = list(enumerate(betweenness))
    #    json.dump(betweenness_list, open("betweenness_centrality.json", "w"))
    betweenness = network_ig.betweenness()
    betweenness_list = list(enumerate(betweenness))
    betweenness_list.sort(key=lambda x: x[1], reverse=True)
    return betweenness_list

def get_eigenvector_centrality_list(network):
    network_ig = ig.Graph.from_networkx(network)
    #if os.path.exists("eigenvector_centrality.json"):
    #    eigenvector_centrality_list = json.load(open("eigenvector_centrality.json", "r"))
    #else:
    #    eigenvector_centrality = network_ig.eigenvector_centrality()
    #    eigenvector_centrality_list = list(enumerate(eigenvector_centrality))
    #    json.dump(eigenvector_centrality_list, open("eigenvector_centrality.json", "w"))
    eigenvector_centrality = network_ig.eigenvector_centrality()
    eigenvector_centrality_list = list(enumerate(eigenvector_centrality))
    eigenvector_centrality_list.sort(key=lambda x: x[1], reverse=True)
    return eigenvector_centrality_list

def estimate_betweenness_centrality_list(network, k=1000):
    network_ig = ig.Graph.from_networkx(network)
    #if os.path.exists("estimated_betweenness_centrality.json"):
    #    estimated_betweenness_centrality_list = json.load(open("estimated_betweenness_centrality.json", "r"))
    #else:
    #    estimated_betweenness_centrality = network_ig.betweenness(vertices=network_ig.vs, directed=True, cutoff=None, weights=None, nobigint=True, k=k)
    #    estimated_betweenness_centrality_list = list(enumerate(estimated_betweenness_centrality))
    #    json.dump(estimated_betweenness_centrality_list, open("estimated_betweenness_centrality.json", "w"))
    estimated_betweenness_centrality = network_ig.estimate_betweenness(vertices=network_ig.vs, cutoff=None, weights=None, nobigint=True, k=k)
    estimated_betweenness_centrality_list = list(enumerate(estimated_betweenness_centrality))
    estimated_betweenness_centrality_list.sort(key=lambda x: x[1], reverse=True)
    return estimated_betweenness_centrality_list

def estimate_eigenvector_centrality_list(network, max_iter=1000, tol=1e-06):
    network_ig = ig.Graph.from_networkx(network)
    #if os.path.exists("estimated_eigenvector_centrality.json"):
    #    estimated_eigenvector_centrality_list = json.load(open("estimated_eigenvector_centrality.json", "r"))
    #else:
    #    estimated_eigenvector_centrality = network_ig.eigenvector_centrality(max_iter=max_iter, tol=tol)
    #    estimated_eigenvector_centrality_list = list(enumerate(estimated_eigenvector_centrality))
    #    json.dump(estimated_eigenvector_centrality_list, open("estimated_eigenvector_centrality.json", "w"))
    estimated_eigenvector_centrality = network_ig.eigenvector_centrality(max_iter=max_iter, tol=tol)
    estimated_eigenvector_centrality_list = list(enumerate(estimated_eigenvector_centrality))
    estimated_eigenvector_centrality_list.sort(key=lambda x: x[1], reverse=True)
    return estimated_eigenvector_centrality_list