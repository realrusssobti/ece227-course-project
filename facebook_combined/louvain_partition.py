import pandas as pd
import igraph as ig
import networkx as nx

network_path = "facebook_combined.txt"
print("Loading the mention network...")
network_file = open(network_path)
network_nx = nx.read_edgelist(network_file, create_using=nx.Graph(), data=(('weight', int),))
network_ig = ig.Graph.from_networkx(network_nx)
print(f"Loaded mention network with {network_ig.vcount()} nodes and {network_ig.ecount()} edges.")

print("Converting to undirected graph for community detection...")
# Drop edge directions and combine multi-edges
network_undirected = network_ig.as_undirected(mode="collapse")

# ==========================================
# 1. UNBOUNDED APPROACH: LOUVAIN ALGORITHM
# ==========================================
print("Running Unbounded Community Detection (Louvain)...")
# In igraph, Louvain is called 'community_multilevel'
louvain_partition = network_undirected.community_multilevel()
print(f"Louvain naturally found {len(louvain_partition)} communities.")

# Assign the community IDs back to the nodes
network_undirected.vs['Louvain_Community'] = louvain_partition.membership


print("Isolating the Giant Component for bounded detection...")
# Break the graph into its connected pieces
components = network_undirected.connected_components()
# Extract the largest connected piece
giant_component = components.giant()

print(f"The giant component contains {giant_component.vcount()} out of {network_undirected.vcount()} nodes.")

print("Running Bounded Community Detection (Fast-Greedy for 10 communities)...")
dendrogram = giant_component.community_fastgreedy()

# Now we can safely cut it to 10 communities!
TARGET_COMMUNITIES = 10
bounded_partition = dendrogram.as_clustering(n=TARGET_COMMUNITIES)
print(f"Bounded approach successfully forced {len(bounded_partition)} communities inside the giant component.")

# Create a dictionary to map the User IDs to their new bounded community
bounded_membership_map = {
    vertex['_nx_name']: comm_id 
    for vertex, comm_id in zip(giant_component.vs, bounded_partition.membership)
}


# ==========================================
# 3. EXPORT FOR VISUALIZATION
# ==========================================
print("Exporting community data for Gephi...")
nodes_dict = []

for v in network_undirected.vs:
    user_id = v['_nx_name']
    
    # If the user is in the giant component, they get a 0-9 ID. 
    # If they were an isolated island, they get assigned -1
    bounded_id = bounded_membership_map.get(user_id, -1)
    
    nodes_dict.append({
        "Id": user_id, 
        "Louvain_Community": v['Louvain_Community'],
        "Bounded_Community": bounded_id
    })

pd.DataFrame(nodes_dict).to_csv("higgs_communities_nodes.csv", index=False)
print("Saved to higgs_communities_nodes.csv! Ready for Gephi.")
