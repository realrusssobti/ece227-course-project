import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from google.colab import files
import math

print("--- ANALYZING TOP 10 SENDERS FOR ENRON EXECUTIVES ---")

# 1. Map all raw email aliases to their exact human and role
# This combines duplicate inboxes so the data is 100% accurate!
exec_mapping = {
    'a..martin@enron.com': 'Thomas Martin (VP)',
    'd..martin@enron.com': 'Thomas Martin (VP)',
    'thomas.martin@enron.com': 'Thomas Martin (VP)',
    'andy.zipper@enron.com': 'Andy Zipper (VP)',
    'barry.tycholiz@enron.com': 'Barry Tycholiz (VP)',
    'b..sanders@enron.com': 'Richard Sanders (VP)',
    'richard.sanders@enron.com': 'Richard Sanders (VP)',
    'dana.davis@enron.com': 'Dana Davis (VP)',
    'danny.mccarty@enron.com': 'Danny McCarty (VP)',
    'drew.fossum@enron.com': 'Drew Fossum (VP)',
    'd..steffes@enron.com': 'James Steffes (VP)',
    'james.steffes@enron.com': 'James Steffes (VP)',
    'fletcher.sturm@enron.com': 'Fletcher Sturm (VP)',
    'j..sturm@enron.com': 'Fletcher Sturm (VP)',
    'harry.arora@enron.com': 'Harpreet Arora (VP)',
    'hunter.shively@enron.com': 'Hunter Shively (VP)',
    's..shively@enron.com': 'Hunter Shively (VP)',
    'jane.tholt@enron.com': 'Jane Tholt (VP)',
    'm..tholt@enron.com': 'Jane Tholt (VP)',
    'j..kean@enron.com': 'Steven Kean (VP)',
    'steven.kean@enron.com': 'Steven Kean (VP)',
    'joe.stepenovitch@enron.com': 'Joe Stepenovitch (VP)',
    'john.arnold@enron.com': 'John Arnold (VP)',
    'john.zufferli@enron.com': 'John Zufferli (VP)',
    'kevin.presto@enron.com': 'Kevin Presto (VP)',
    'm..presto@enron.com': 'Kevin Presto (VP)',
    'richard.shapiro@enron.com': 'Richard Shapiro (VP)',
    'rod.hayslett@enron.com': 'Rod Hayslett (VP)',
    'scott.neal@enron.com': 'Scott Neal (VP)',
    'shelley.corman@enron.com': 'Shelley Corman (VP)',
    'sally.beck@enron.com': 'Sally Beck (COO)',
    'david.delainey@enron.com': 'David Delainey (CEO)',
    'w..delainey@enron.com': 'David Delainey (CEO)',
    'jeff.skilling@enron.com': 'Jeffery Skilling (CEO)',
    'john.lavorato@enron.com': 'John Lavorato (CEO)',
    'kenneth.lay@enron.com': 'Kenneth Lay (CEO)'
}

# 2. Count the emails per REAL PERSON (Grouping aliases together)
# We assume 'edges' still exists in memory from your very first block!
incoming_counts = defaultdict(Counter)

for sender, receiver in edges:
    if receiver in exec_mapping:
        real_name = exec_mapping[receiver]
        # Skip emails where they email themselves
        if sender not in exec_mapping or exec_mapping.get(sender) != real_name:
            incoming_counts[real_name][sender] += 1

# 3. Build the NetworkX Graph
top10_graph = nx.DiGraph()
executive_top10_data = {} # Save for bar charts

for exec_name, sender_counts in incoming_counts.items():
    # Get Top 10 senders for this specific executive
    top_10 = sender_counts.most_common(10)
    executive_top10_data[exec_name] = top_10
    
    top10_graph.add_node(exec_name, Role="Executive")
    for sender, count in top_10:
        top10_graph.add_node(sender, Role="Sender")
        top10_graph.add_edge(sender, exec_name, weight=count)

print(f"Graph built with {top10_graph.number_of_nodes()} highly connected people.")

# ==========================================
# PLOT 1: THE NETWORKX GALAXY GRAPH
# ==========================================
print("\nRendering Network Graph (This takes a few seconds)...")
plt.figure(figsize=(22, 18))
pos = nx.spring_layout(top10_graph, k=0.6, iterations=60)

executives = [n for n, d in top10_graph.nodes(data=True) if d.get('Role') == 'Executive']
senders = [n for n, d in top10_graph.nodes(data=True) if d.get('Role') == 'Sender']

# Scale node sizes based on degree
exec_sizes = [top10_graph.degree(n) * 300 for n in executives]
sender_sizes = [top10_graph.degree(n) * 50 for n in senders]

# Edge thickness based on number of emails (scaled down to look clean)
max_weight = max([d['weight'] for u, v, d in top10_graph.edges(data=True)]) if top10_graph.edges() else 1
edge_widths = [(d['weight'] / max_weight) * 5 + 0.5 for u, v, d in top10_graph.edges(data=True)]

# Draw the graph elements

nx.draw_networkx_nodes(top10_graph, pos, nodelist=executives, node_color='crimson', node_size=exec_sizes, edgecolors='black')
nx.draw_networkx_nodes(top10_graph, pos, nodelist=senders, node_color='lightblue', node_size=sender_sizes, edgecolors='gray')
nx.draw_networkx_edges(top10_graph, pos, width=edge_widths, edge_color='gray', alpha=0.5, arrows=True)

# Add Labels for Executives ONLY
labels = {node: node for node in executives}
nx.draw_networkx_labels(top10_graph, pos, labels=labels, font_size=10, font_weight='bold', font_color='black')

plt.title("Top 10 Sender Networks: CEOs, COO, and VPs", fontsize=24)
plt.axis('off')
plt.tight_layout()
plt.savefig("Executive_Network_Map.png", dpi=300, bbox_inches='tight')
plt.show()

# ==========================================
# PLOT 2: THE BAR CHART GRID (In-Degree Distribution)
# ==========================================
print("\nRendering Bar Chart Grid...")
num_execs = len(executive_top10_data)
cols = 4
rows = math.ceil(num_execs / cols)

# Create a massive grid to hold all the bar charts
fig, axes = plt.subplots(rows, cols, figsize=(20, 5 * rows))
axes = axes.flatten()

# Plot each executive's data in their own square
for idx, (exec_name, top_10) in enumerate(executive_top10_data.items()):
    ax = axes[idx]
    
    if not top_10:
        ax.set_title(f"{exec_name}\n(No incoming data)", fontsize=10)
        ax.axis('off')
        continue
        
    senders = [x[0].split('@')[0] for x in top_10] # Clean up emails for the axis
    counts = [x[1] for x in top_10]
    
    ax.barh(senders[::-1], counts[::-1], color='teal')
    ax.set_title(exec_name, fontsize=12, fontweight='bold')
    ax.tick_params(axis='y', labelsize=8)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

# Hide any empty squares at the end of the grid
for i in range(num_execs, len(axes)):
    axes[i].axis('off')

plt.suptitle("Top 10 Senders per Executive (Incoming Emails)", fontsize=24, y=1.02)
plt.tight_layout()
plt.savefig("Executive_Bar_Charts.png", dpi=300, bbox_inches='tight')
plt.show()

# Trigger downloads
print("\nTriggering file downloads...")
files.download("Executive_Network_Map.png")
files.download("Executive_Bar_Charts.png")
