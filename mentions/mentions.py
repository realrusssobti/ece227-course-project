import os
import networkx as nx
import igraph as ig
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

mention_file = open(os.path.join(DATA_DIR, "higgs-mention_network.edgelist"))
mentions = nx.read_edgelist(mention_file, create_using=nx.DiGraph(), data=(('weight', int),))

nodes = mentions.nodes
print("Number of nodes in the mention network:")
print(mentions.order())
keys = nodes.keys()

print("\n")

# In degree and out degree
print("In Degree Statistics")
in_degree_list = list(mentions.in_degree())
in_degree_list.sort(key=lambda x: x[1], reverse=True)
print("Top 10 nodes with highest in degree:")
print(in_degree_list[0:10])
in_degree_avg = sum(map(lambda x: x[1], in_degree_list)) / len(in_degree_list)
print("Average in degree:")
print(in_degree_avg)

print("\n")

print("Out Degree Statistics")
out_degree_list = list(mentions.out_degree())
out_degree_list.sort(key=lambda x: x[1], reverse=True)
print("Top 10 nodes with highest out degree:")
print(out_degree_list[0:10])
out_degree_avg = sum(map(lambda x: x[1], out_degree_list)) / len(out_degree_list)
print("Average out degree:")
print(out_degree_avg)

mentions_ig = ig.Graph.from_networkx(mentions)

print("\n")
# Betweenness Centrality
betweenness_json_file = os.path.join(os.path.dirname(__file__), "mention_betweenness_centrality.json")
if os.path.exists(betweenness_json_file):
    print("Loading Betweenness Centrality from JSON...")
    betweenness_list = json.load(open(betweenness_json_file, "r"))
else:
    print("Computing Betweenness Centrality (this may take a while)...")
    betweenness = mentions_ig.betweenness()
    betweenness_list = list(zip(mentions_ig.vs['_nx_name'], betweenness))
    json.dump(betweenness_list, open(betweenness_json_file, "w"))

betweenness_list.sort(key=lambda x: x[1], reverse=True)
print("Betweenness Centrality Statistics")
print("Top 10 nodes with highest betweenness centrality:")
print(betweenness_list[0:10])

print("\n")
# Eigenvector Centrality
eigenvector_json_file = os.path.join(os.path.dirname(__file__), "mention_eigenvector_centrality.json")
if os.path.exists(eigenvector_json_file):
    print("Loading Eigenvector Centrality from JSON...")
    eigenvector_centrality_list = json.load(open(eigenvector_json_file, "r"))
else:
    print("Computing Eigenvector Centrality...")
    eigenvector_centrality = mentions_ig.eigenvector_centrality(directed=True)
    eigenvector_centrality_list = list(zip(mentions_ig.vs['_nx_name'], eigenvector_centrality))
    json.dump(eigenvector_centrality_list, open(eigenvector_json_file, "w"))

eigenvector_centrality_list.sort(key=lambda x: x[1], reverse=True)
print("Eigenvector Centrality Statistics")
print("Top 10 nodes with highest eigenvector centrality:")
print(eigenvector_centrality_list[0:10])

top_10_percent_in_degree = in_degree_list[0:int(0.1 * len(in_degree_list))]
top_10_percent_out_degree = out_degree_list[0:int(0.1 * len(out_degree_list))]
top_10_percent_betweenness = betweenness_list[0:int(0.1 * len(betweenness_list))]
top_10_percent_eigenvector_centrality = eigenvector_centrality_list[0:int(0.1 * len(eigenvector_centrality_list))]
print(f"Nodes that are in top 10% of in and out degree:")
print(len(set(map(lambda x: x[0], top_10_percent_in_degree)).intersection(set(map(lambda x: x[0], top_10_percent_out_degree)))))
print("\n")
print(f"Nodes that are in top 10% of in degree and betweenness centrality:")
print(len(set(map(lambda x: x[0], top_10_percent_in_degree)).intersection(set(map(lambda x: x[0], top_10_percent_betweenness)))))
print("\n")
print(f"Nodes that are in top 10% of in degree and eigenvector centrality:")
print(len(set(map(lambda x: x[0], top_10_percent_in_degree)).intersection(set(map(lambda x: x[0], top_10_percent_eigenvector_centrality)))))
print("\n")
print(f"Nodes that are in top 10% of out degree and betweenness centrality:")
print(len(set(map(lambda x: x[0], top_10_percent_out_degree)).intersection(set(map(lambda x: x[0], top_10_percent_betweenness)))))
print("\n")
print(f"Nodes that are in top 10% of out degree and eigenvector centrality:")
print(len(set(map(lambda x: x[0], top_10_percent_out_degree)).intersection(set(map(lambda x: x[0], top_10_percent_eigenvector_centrality)))))
print("\n")
print(f"Nodes that are in top 10% of betweenness centrality and eigenvector centrality:")
print(len(set(map(lambda x: x[0], top_10_percent_betweenness)).intersection(set(map(lambda x: x[0], top_10_percent_eigenvector_centrality)))))