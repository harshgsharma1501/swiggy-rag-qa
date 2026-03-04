import re
from collections import Counter

LOG_FILE = "logs/queries.log"

queries = []
refusals = 0

with open(LOG_FILE, "r") as f:
    for line in f:
        q_match = re.search(r"QUERY: (.*?) \|", line)
        if q_match:
            queries.append(q_match.group(1))

        if "not available" in line.lower():
            refusals += 1

print("\nTotal Queries:", len(queries))
print("Refusals:", refusals)

counter = Counter(queries)

print("\nMost Frequent Queries:")
for q, c in counter.most_common(5):
    print(f"{q} — {c} times")