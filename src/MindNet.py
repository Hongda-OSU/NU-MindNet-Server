import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import matplotlib.patches as mpatches

class MindNet():
    def __init__(self, user_id: int, df: pd.DataFrame, save_file_name: str, directed: bool):
        """
        Args:
            user_id (int): node user id
            df (pandas.dataframe): pandas dataframe for network edgelist
            save_file_name (str): filepath to save network visualization
            directed (boolean): network is directed or not
        """        
        self.user_id = user_id
        self.data_frame = df
        self.directed = directed
        self.graph = self.read_graph_from_edgelist()
        self.save_file_name = save_file_name
        
    def read_graph_from_edgelist(self):
        """
        Returns:
            DiGraph() or Graph(): a nx graph object from edgelist
        """        
        if self.directed:
            graph_type = nx.DiGraph()
        else:
            graph_type = nx.Graph()
            
        return nx.from_pandas_edgelist(self.data_frame, create_using = graph_type)
    
    def visualize(self):
        """
        Visualize network structure
        """        
        plt.clf()
        color_map = ["#FF8C00" if node == self.user_id else "#6B8E23" for node in self.graph]
        nx.draw_networkx(self.graph, node_color = color_map, with_labels=True)
        plt.savefig(self.save_file_name, format = "JPG", dpi = 1000)
        
    def visualize_attr(self, attr_dic: dict):
        """
        Visualize network structure, colored by attr_dic
        """        
        plt.clf()
        num_colors = len(set(attr_dic.values()))
        color_dic = {}
        for val in set(attr_dic.values()):
            if val not in color_dic:
                color_dic[val] = np.random.uniform(0, 1, 3)
        color_map = [color_dic[attr_dic[node]] for node in self.graph]
        nx.draw_networkx(self.graph, node_color = color_map, with_labels=True)
        handle = [mpatches.Patch(color = c, label = attr) for attr, c in color_dic.items()]
        plt.legend(handles = handle)
        plt.savefig(self.save_file_name, format = "JPG", dpi = 1000)
        
    def visualize_degree(self):
        """
        Generate barplot for degree distribution of all nodes
        """        
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
        # plt.savefig("degree.jpg", format = "JPG", dpi = 1000)
        
    def statistics(self, stat_save_path = None):
        """
        Calculates network statistics for gievn graph and saves pandas dataframe to stat_save_path, if given
        Args:
            stat_save_path (str, optional): Save path to store df_stat. Defaults to None.
        """        
        df_stat = pd.DataFrame()
        df_stat["nodes"] = list(self.graph.nodes())
        df_stat["degree"] = [degree for idx, degree in self.graph.degree()]
        df_stat["closeness"] = nx.closeness_centrality(self.graph).values()
        df_stat["eigen_centrality"] = nx.eigenvector_centrality(self.graph).values()
        if self.directed:
            df_stat["reciprocity"] = nx.reciprocity(self.graph, nodes = list(self.graph.nodes())).values()

        print("\n")
        for col_name in df_stat.columns:
            df_stat[f"{col_name}_rank"] = df_stat[f"{col_name}"].rank(ascending=False).astype(int)
            df_stat[f"{col_name}_level"] = df_stat[f"{col_name}_rank"] / len(df_stat) * 3
            df_stat[f"{col_name}_level"] = df_stat[f"{col_name}_level"].apply(np.floor).astype(int)
            
        print(df_stat.head())
    
        self.df_stat = df_stat
        
        if stat_save_path:
            df_stat.to_csv(stat_save_path)
        



