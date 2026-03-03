!pip install igraph python-louvain

import pandas as pd
import email
import networkx as nx
import igraph as ig
import json
import os
import zipfile
import matplotlib.pyplot as plt
import community.community_louvain as community_louvain # Louvain algorithm
from google.colab import files
from collections import defaultdict

# ==========================================
# 1. DATA PARSING & NETWORK CONSTRUCTION
# ==========================================
print("1. Reading emails.csv and parsing network...")
# LIMITING to 50,000 rows to prevent Colab from crashing.
# Remove `nrows=50000` ONLY if you have sufficient RAM.
df = pd.read_csv('emails.csv', usecols=['message'], nrows=50000)

edges = []

for msg_text in df['message']:
    msg = email.message_from_string(msg_text)
    sender = msg['From']
    receiver = msg['To']

    if sender and receiver:
        receivers = str(receiver).replace('\n', '').replace('\t', '').split(',')
        for rec in receivers:
            # We strip extra spaces from the ends of the strings
            edges.append((sender.strip(), rec.strip()))

# Load directly into NetworkX from the Python list
enron_graph = nx.DiGraph()
enron_graph.add_edges_from(edges)

# Save safely to a file for your final zip download using a TAB delimiter
enron_file_path = "enron_network.edgelist"
nx.write_edgelist(enron_graph, enron_file_path, delimiter='\t', data=False)

print(f"Network built! Nodes: {enron_graph.order()}, Edges: {enron_graph.size()}\n")


# ==========================================
# 2. CENTRALITY METRICS & JSON EXPORT
# ==========================================
print("2. Calculating Centrality Metrics...")

# Degree Centrality
in_degree_list = list(enron_graph.in_degree())
out_degree_list = list(enron_graph.out_degree())

in_degree_list.sort(key=lambda x: x[1], reverse=True)
out_degree_list.sort(key=lambda x: x[1], reverse=True)

print(f"Top 10 by In-Degree:\n{in_degree_list[:10]}\n")
print(f"Top 10 by Out-Degree:\n{out_degree_list[:10]}\n")

# Convert to igraph for faster complex computations
enron_ig = ig.Graph.from_networkx(enron_graph)

# Betweenness Centrality
betweenness_json_file = "enron_betweenness_centrality.json"
if os.path.exists(betweenness_json_file):
    print("Loading Betweenness Centrality from JSON...")
    with open(betweenness_json_file, "r") as f:
        betweenness_list = json.load(f)
else:
    print("Computing Betweenness Centrality (this takes a moment)...")
    betweenness = enron_ig.betweenness(directed=True)
    betweenness_list = list(zip(enron_ig.vs['_nx_name'], betweenness))
    with open(betweenness_json_file, "w") as f:
        json.dump(betweenness_list, f)

betweenness_list.sort(key=lambda x: x[1], reverse=True)
print(f"Top 10 by Betweenness Centrality:\n{betweenness_list[:10]}\n")

# Eigenvector Centrality
eigenvector_json_file = "enron_eigenvector_centrality.json"
if os.path.exists(eigenvector_json_file):
    print("Loading Eigenvector Centrality from JSON...")
    with open(eigenvector_json_file, "r") as f:
        eigenvector_list = json.load(f)
else:
    print("Computing Eigenvector Centrality...")
    eigenvector = enron_ig.eigenvector_centrality(directed=True)
    eigenvector_list = list(zip(enron_ig.vs['_nx_name'], eigenvector))
    with open(eigenvector_json_file, "w") as f:
        json.dump(eigenvector_list, f)

eigenvector_list.sort(key=lambda x: x[1], reverse=True)
print(f"Top 10 by Eigenvector Centrality:\n{eigenvector_list[:10]}\n")


# ==========================================
# 3. TOP 10% INTERSECTIONS
# ==========================================
print("3. Calculating Top 10% Overlaps...")
top_10_percent = int(0.1 * len(in_degree_list))

in_set = set(map(lambda x: x[0], in_degree_list[:top_10_percent]))
out_set = set(map(lambda x: x[0], out_degree_list[:top_10_percent]))
bw_set = set(map(lambda x: x[0], betweenness_list[:top_10_percent]))
ev_set = set(map(lambda x: x[0], eigenvector_list[:top_10_percent]))

print(f"Nodes in top 10% of In-Degree AND Betweenness: {len(in_set.intersection(bw_set))}")
print(f"Nodes in top 10% of In-Degree AND Eigenvector: {len(in_set.intersection(ev_set))}")


# ==========================================
# 4. COMMUNITY DETECTION (LOUVAIN)
# ==========================================
print("\n4. Performing Community Detection...")
# Louvain requires an undirected graph
undirected_graph = enron_graph.to_undirected()
partition = community_louvain.best_partition(undirected_graph)

# Count communities
num_communities = len(set(partition.values()))
print(f"Louvain algorithm found {num_communities} distinct communities.")
community_sizes = [num_communities for community in partition]
print(f"Community sizes: {community_sizes}")

# Save communities for Gephi visualization later
nx.set_node_attributes(enron_graph, partition, 'community_id')
nx.write_gexf(enron_graph, "enron_communities.gexf")
print("Saved network with communities to 'enron_communities.gexf' for Gephi.")
print("\n--- Top 5 Central Nodes per Community (by In-Degree) ---")
print("    (Ordered by Community Size: Largest to Smallest)")

# 1. Get in-degrees for all nodes for fast lookup
in_degree_dict = dict(enron_graph.in_degree())

# 2. Group nodes by their community ID
community_groups = defaultdict(list)
for node, comm_id in partition.items():
    community_groups[comm_id].append((node, in_degree_dict.get(node, 0)))

# 3. Sort the nodes *within* each community by in-degree (descending)
for comm_id in community_groups:
    community_groups[comm_id].sort(key=lambda x: x[1], reverse=True)

# 4. Sort the communities themselves by size (DESCENDING order)
# Adding reverse=True puts the largest communities at the top
sorted_communities = sorted(community_groups.items(), key=lambda item: len(item[1]), reverse=True)

# 5. Extract top 5, print them, and prepare data for JSON
community_export_data = []

for comm_id, members in sorted_communities:
    top_5 = members[:5]

    # Format the top 5 list into dictionaries for a clean JSON structure
    top_5_formatted = [{"node": node, "in_degree": degree} for node, degree in top_5]

    # Build the dictionary for this specific community
    community_data = {
        "community_id": comm_id,
        "size": len(members),
        "top_5_nodes": top_5_formatted
    }
    community_export_data.append(community_data)

    # Print the results to the console so you can see them immediately
    print(f"\nCommunity {comm_id} (Size: {len(members)} nodes):")
    for rank, (node, degree) in enumerate(top_5, 1):
        print(f"  {rank}. {node} (In-Degree: {degree})")

# 6. Export to JSON and download
json_filename = "top_nodes_per_community.json"

with open(json_filename, "w") as f:
    # indent=4 makes the JSON file nicely formatted and easy for humans to read
    json.dump(community_export_data, f, indent=4)

print(f"\nSaved community rankings to '{json_filename}'. Triggering download...")
files.download(json_filename)

# ==========================================
# 5. DEGREE DISTRIBUTION (POWER LAW)
# ==========================================
print("\n5. Plotting Degree Distribution...")
degrees = [deg for node, deg in undirected_graph.degree()]

plt.figure(figsize=(8, 5))
# A log-log plot is best for visualizing a power law distribution
plt.hist(degrees, bins=50, log=True)
plt.title("Degree Distribution of Enron Network (Log Scale)")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.savefig("degree_distribution.png")
plt.show()
print("Saved degree distribution plot as 'degree_distribution.png'.")


# ==========================================
# 6. DIAMETER & AVERAGE SHORTEST PATH
# ==========================================
print("\n6. Calculating Global Metrics (on Largest Connected Component)...")
# Must extract the Largest Weakly Connected Component first,
# otherwise disconnected nodes return an infinite path length.
components = nx.weakly_connected_components(enron_graph)
lcc_nodes = max(components, key=len)
lcc_graph = enron_graph.subgraph(lcc_nodes)

# Using igraph again because NetworkX shortest paths would take hours
lcc_ig = ig.Graph.from_networkx(lcc_graph)

diameter = lcc_ig.diameter()
avg_path = lcc_ig.average_path_length()

print(f"Diameter of LCC: {diameter}")
print(f"Average Shortest Path of LCC: {avg_path:.2f}")


# ==========================================
# 7. ZIP AND DOWNLOAD RESULTS
# ==========================================
print("\n7. Zipping files for download...")
zip_filename = "enron_full_analysis.zip"

# Added the JSON files to the zip export list
files_to_zip = [
    "enron_network.edgelist",
    "enron_communities.gexf",
    "degree_distribution.png",
    "enron_betweenness_centrality.json",
    "enron_eigenvector_centrality.json"
]

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)

print("Triggering download...")
files.download(zip_filename)