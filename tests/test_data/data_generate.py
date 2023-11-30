import pandas as pd
import numpy as np

num_nodes = 25
num_connections = 100
nodes = [i for i in range(num_nodes)]
connections = [(np.random.choice(nodes), np.random.choice(nodes)) for _ in range(num_connections)]

edges = pd.DataFrame(connections, columns=['source', 'target'])

edges.to_csv("tests/test_data/test_undirected_medium.csv", index = False)