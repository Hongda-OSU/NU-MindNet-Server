import pandas as pd
import numpy as np

num_nodes = 50
num_connections = 50
nodes = [i for i in range(num_nodes)]

connections = []
while len(connections) < num_connections:
    a = np.random.choice(nodes)
    b = np.random.choice(nodes)
    if a != b:
        connections.append((a, b))

edges = pd.DataFrame(connections, columns=['source', 'target'])

edges.to_csv("tests/test_data/test_directed_large.csv", index = False)