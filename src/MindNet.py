import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

class MindNet():
    def __init__(self, user_id, df, save_file_name, directed):
        self.user_id = user_id
        self.data_frame = df
        self.directed = directed
        self.graph = self.read_graph_from_edgelist()
        self.save_file_name = save_file_name
        
    def read_graph_from_edgelist(self):
        if self.directed:
            graph_type = nx.DiGraph()
        else:
            graph_type = nx.Graph()
            
        return nx.from_pandas_edgelist(self.data_frame, create_using = graph_type)
    
    def visualize(self):
        plt.clf()
        color_map = ["#FF8C00" if node == self.user_id else "#6B8E23" for node in self.graph]
        nx.draw(self.graph, node_color = color_map, with_labels=True)
        plt.savefig(self.save_file_name, format = "JPG", dpi = 1000)
        
    def visualize_degree(self):
        deg_seq = [degree for idx, degree in self.graph.degree()]
        deg_seq.sort(reverse = True)
        deg_set = set(deg_seq)
        counts = [deg_seq.count(d) for d in deg_set]
        user_deg = self.graph.degree(self.user_id)
        plt.clf()
        plt.bar(list(deg_set), counts)
        plt.xlabel("Degree")
        plt.ylabel("Freq")
        plt.axvline(x=user_deg, c = "red")
        plt.savefig("degree.jpg", format = "JPG", dpi = 1000)
        
    


