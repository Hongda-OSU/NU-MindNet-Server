import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import matplotlib.patches as mpatches


def main():
    """
    TODO: 
    1. Read json from frontend
    2. convert Json to pandas dataframes. One for node attributes. Several for questions. 
    3. Create Mindnet Object and specify location to store visualization image files
    4. Visualize images based on node attributes
    5. Calculate network statistics
    6. Store images and statistics files to S3. 
    """
    
    # file_name = "tests/test_data/test_undirected_large.csv"
    # image_name = "test_undirected_large.jpg"
    # df = pd.read_csv(file_name)
    # mn = MindNet(user_id= 1, df = df, save_file_name = image_name, directed = False)
    # mn.visualize_attr(attr_dic = {0: 'male', 1: 'female', 2: 'Walmart Bag', 3: 'male', 4: 'female', 5: 'Walmart Bag', 6: 'male', 7: 'female', 8: 'Walmart Bag', 9: 'male', 10: 'female', 11: 'Walmart Bag', 12: 'male', 13: 'female', 14: 'Walmart Bag', 15: 'male', 16: 'female', 17: 'Walmart Bag', 18: 'male', 19: 'female', 20: 'Walmart Bag', 21: 'male', 22: 'female', 23: 'Walmart Bag', 24: 'male', 25: 'female', 26: 'Walmart Bag', 27: 'male', 28: 'female', 30: 'male', 31: 'female', 32: 'Walmart Bag', 33: 'male', 34: 'female', 35: 'Walmart Bag', 36: 'male', 37: 'female', 39: 'male', 40: 'female', 41: 'Walmart Bag', 42: 'male', 43: 'female', 44: 'Walmart Bag', 45: 'male', 46: 'female', 47: 'Walmart Bag', 48: 'male', 49: 'female'})
    
    
    # Convert json file to pandas dataframes here:

    # Create MindNet objects for each question
    mn1 = MindNet(user_id= 1, df = df1, save_file_name = image_name, directed = False)
    mn2 = MindNet(user_id= 1, df = df2, save_file_name = image_name, directed = False)
    mn3 = MindNet(user_id= 1, df = df3, save_file_name = image_name, directed = False)
    mn4 = MindNet(user_id= 1, df = df4, save_file_name = image_name, directed = False)
    
        


if __name__ == "main":
    main()
