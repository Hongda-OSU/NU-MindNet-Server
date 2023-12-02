import pandas as pd
import numpy as np

num_nodes = 50
num_connections = 60
nodes = [i for i in range(num_nodes)]

connections = []
while len(connections) < num_connections:
    a = np.random.choice(nodes)
    b = np.random.choice(nodes)
    if a != b:
        connections.append((a, b))

edges = pd.DataFrame(connections, columns=['source', 'target'])

edges.to_csv("tests/test_data/test_undirected_large.csv", index = False)

arr = set(edges["source"].tolist() + edges["target"].tolist())
print(arr)
values = ["male", "female", "Walmart Bag"]
dic = {}
for idx in arr:
    dic[idx] = values[idx % 3]
print(dic)