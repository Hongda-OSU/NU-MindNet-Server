import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from src.MindNet import MindNet
import pytest

def test_directed_small():
    file_name = "tests/test_data/test_directed_small.csv"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, directed = True)
    mn.visualize()
    
def test_undirected_small():
    file_name = "tests/test_data/test_undirected_small.csv"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, directed = False)
    mn.visualize()
    
# def test_undirected_medium():
#     file_name = "tests/test_data/test_undirected_medium.csv"
#     df = pd.read_csv(file_name)
#     mn = MindNet(user_id= 1, df = df, directed = False)
#     mn.visualize()