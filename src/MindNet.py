import os
import boto3
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class MindNet():
    def __init__(self, user_id: int, df: pd.DataFrame, directed: bool):
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
        self.hex_colors = ["#ADD8E6", "#FF7F50", "#40E0D0", "#DAA520", "#DA70D6",
                           "#FF6347", "#000080", "#008080", "#808000", "#800000",
                           "#00FF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#808080",
                           "#800080", "#008000", "#0000FF", "#FF0000", "#FFFF00"]
                           
                           
    def upload_to_s3(self, local_file_path, s3_bucket, s3_key):
        """
        Uploads a file to S3
        """
        s3_client = boto3.client('s3')
        s3_client.upload_file(
            Filename=local_file_path, 
            Bucket=s3_bucket, 
            Key=s3_key,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpg'} 
        )

        
    def read_graph_from_edgelist(self):
        """
        Returns:
            DiGraph() or Graph(): a nx graph object from edgelist
        """        
        if self.directed:
            graph_type = nx.DiGraph()
        else:
            graph_type = nx.Graph()
            
        return nx.from_pandas_edgelist(self.data_frame, source = "Source", target = "Target", create_using = graph_type)
    
    def visualize(self, save_file_name, s3_bucket):
        """
        Visualize network structure
        """        
        plt.clf()
        color_map = ["#ADD8E6" if node == self.user_id else "#FF7F50" for node in self.graph]
        nx.draw_networkx(self.graph, node_color = color_map, with_labels=True)
        plt.savefig(save_file_name, format = "JPG", dpi = 1000)
        
        s3_key = os.path.basename(save_file_name)
        self.upload_to_s3(save_file_name, s3_bucket, s3_key)
        
    def visualize_attr(self, save_file_name: str, attr_dic: dict, s3_bucket):
        """
        Visualize network structure, colored by attr_dic
        """        
        plt.clf()
        num_colors = len(set(attr_dic.values()))
        color_dic = {}
        idx = 0
        for val in set(attr_dic.values()):
            if val not in color_dic:
                color_dic[val] = self.hex_colors[idx]
                idx += 1
        color_map = [color_dic[attr_dic[node]] for node in self.graph]
        nx.draw_networkx(self.graph, node_color = color_map, with_labels=True)
        handle = [mpatches.Patch(color = c, label = attr) for attr, c in color_dic.items()]
        plt.legend(handles = handle)
        plt.savefig(save_file_name, format = "JPG", dpi = 1000)
        
        s3_key = os.path.basename(save_file_name)
        self.upload_to_s3(save_file_name, s3_bucket, s3_key)
        
        
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

        # print("\n")
        for col_name in df_stat.columns:
            df_stat[f"{col_name}_rank"] = df_stat[f"{col_name}"].rank(ascending=False).astype(int)
            df_stat[f"{col_name}_level"] = df_stat[f"{col_name}_rank"] / len(df_stat) * 3
            df_stat[f"{col_name}_level"] = df_stat[f"{col_name}_level"].apply(np.floor).astype(int)
            
        # print(df_stat.head())
    
        self.df_stat = df_stat
        
        if stat_save_path:
            df_stat.to_csv(stat_save_path)
            
    def extract_level_from_statistics(self):
        col_names = ["degree_level", "closeness_level", "eigen_centrality_level"]
        if self.directed:
            col_names.append("reciprocity_level")
        user_row = self.df_stat[self.df_stat['nodes'] == self.user_id]
        user_data = {col: user_row.iloc[0][col] for col in col_names}
        user_data['user_id'] = self.user_id
        return user_data
        
        



