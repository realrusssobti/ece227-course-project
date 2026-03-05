import matplotlib.pyplot as plt
from collections import Counter

# Define the target person
target_person = "sally.beck@enron.com"

# 1. Find all emails sent TO Sally (In-Degree traffic)
# We look at the original 'edges' list from your first code block
emails_to_sally = [sender for sender, receiver in edges if receiver == target_person]

# 2. Count how many times each person emailed her
sender_counts = Counter(emails_to_sally)

# 3. Get the Top 10 people who email Sally the most
top_10_senders = sender_counts.most_common(10)

print(f"--- INCOMING TRAFFIC ANALYSIS FOR {target_person.upper()} ---")
print(f"Total incoming emails in this dataset: {len(emails_to_sally)}")
print(f"Unique people who emailed her (Her exact In-Degree): {len(sender_counts)}\n")

print("Top 10 Senders to Sally:")
for rank, (sender, count) in enumerate(top_10_senders, 1):
    print(f"{rank}. {sender} ({count} emails)")

# 4. Plot the results
senders = [x[0] for x in top_10_senders]
counts = [x[1] for x in top_10_senders]

plt.figure(figsize=(10, 6))
plt.barh(senders[::-1], counts[::-1], color='skyblue') # Reverse to put #1 at the top
plt.xlabel("Number of Emails Sent to Sally")
plt.title(f"Top 10 People Emailing {target_person}")
plt.tight_layout()
plt.savefig("sally_beck_indegree_analysis.png")
plt.show()
