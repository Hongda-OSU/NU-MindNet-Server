import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from src.MindNet import MindNet
import pytest

def test_directed_small():
    file_name = "tests/test_data/test_directed_small.csv"
    image_name = "test_directed_small.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = True)
    mn.visualize()
    
def test_undirected_small():
    file_name = "tests/test_data/test_undirected_small.csv"
    image_name = "test_undirected_small.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = False)
    mn.visualize()
    
def test_directed_medium():
    file_name = "tests/test_data/test_directed_medium.csv"
    image_name = "test_directed_medium.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = True)
    mn.visualize()
    
def test_undirected_medium():
    file_name = "tests/test_data/test_undirected_medium.csv"
    image_name = "test_undirected_medium.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = False)
    mn.visualize()
    
def test_directed_large():
    file_name = "tests/test_data/test_directed_large.csv"
    image_name = "test_directed_large.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = True)
    mn.visualize()
    
def test_undirected_large():
    file_name = "tests/test_data/test_undirected_large.csv"
    image_name = "test_undirected_large.jpg"
    df = pd.read_csv(file_name)
    mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = False)
    mn.visualize()