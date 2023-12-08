import json
import boto3
import os
import uuid
import base64
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from configparser import ConfigParser
from MindNet import MindNet


def lambda_handler(event, context):
    """
    TODO: 
    1. Read json from frontend
    2. convert Json to pandas dataframes. One for node attributes. Several for questions. 
    3. Create Mindnet Object and specify location to store visualization image files
    4. Visualize images based on node attributes
    5. Calculate network statistics
    6. Store images and statistics files to S3. 
    """
    try:
        print("**STARTING**")
        print("**lambda: visualization**")
        
        #
        # setup AWS based on config file:
        #
        print("**Read Config**")
        config_file = 'config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        #
        # configure for S3 access:
        #
        print("**Connect to S3**")
        s3_profile = 's3readwrite'
        boto3.setup_default_session(profile_name=s3_profile)
        
        bucketname = configur.get('s3', 'bucket_name')
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucketname)
       
        # body is json data
        print("**Read Json Data**")
        
        body = event["body"]
        # print(body)
        print(type(body))
        body = json.loads(body)
        print(type(body))
        node_attr = body["Node_attr"]
        connections = body["connections"]
        image_urls = {}
        
        # initialize image_urls
        for i in range(1, 6):
            image_urls[f'Q{i}'] = []
        
        # Convert json file to pandas dataframes here:
        print("**Convert Json data to pandas dataframes**")
        df1 = pd.DataFrame(connections['Q0'])
        df2 = pd.DataFrame(connections['Q1'])
        df3 = pd.DataFrame(connections['Q2'])
        df4 = pd.DataFrame(connections['Q3'])
        df5 = pd.DataFrame(connections['Q4'])

        # Node attributes dictionary to store attributes for each node ID
        node_attributes_gender = {}
        node_attributes_age = {}
        
        # Iterate through each user in Node_attr and update DataFrames and node attributes
        for node in node_attr:
            user_id = node['userId']
            
            # Update node_attributes dictionary with user_id as key and attributes as value list
            node_attributes_gender[user_id] = node['gender']
            num = int(node['age']) // 10
            node_attributes_age[user_id] = f"{num * 10}~{num * 10 + 9}"

        # Create MindNet objects for each question
        mn1 = MindNet(user_id= 0, df = df1, directed = False)
        mn2 = MindNet(user_id= 0, df = df2, directed = False)
        mn3 = MindNet(user_id= 0, df = df3, directed = False)
        mn4 = MindNet(user_id= 0, df = df4, directed = False)
        mn5 = MindNet(user_id= 0, df = df5, directed = True)
        
        save_file_name1 = f"/tmp/Q1-{uuid.uuid4()}.jpg"
        save_file_name2 = f"/tmp/Q2-{uuid.uuid4()}.jpg"
        save_file_name3 = f"/tmp/Q3-{uuid.uuid4()}.jpg"
        save_file_name4 = f"/tmp/Q4-{uuid.uuid4()}.jpg"
        save_file_name5 = f"/tmp/Q5-{uuid.uuid4()}.jpg"
        
        image_urls['Q1'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name1)}")
        image_urls['Q2'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name2)}")
        image_urls['Q3'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name3)}")
        image_urls['Q4'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name4)}")
        image_urls['Q5'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name5)}")
        
        # Visualize basic layout without attributes
        mn1.visualize(save_file_name = save_file_name1, s3_bucket = bucketname)
        mn2.visualize(save_file_name = save_file_name2, s3_bucket = bucketname)
        mn3.visualize(save_file_name = save_file_name3, s3_bucket = bucketname)
        mn4.visualize(save_file_name = save_file_name4, s3_bucket = bucketname)
        mn5.visualize(save_file_name = save_file_name5, s3_bucket = bucketname)
        
        save_file_name1 = f"/tmp/Q1-Gender-{uuid.uuid4()}.jpg"
        save_file_name2 = f"/tmp/Q2-Gender-{uuid.uuid4()}.jpg"
        save_file_name3 = f"/tmp/Q3-Gender-{uuid.uuid4()}.jpg"
        save_file_name4 = f"/tmp/Q4-Gender-{uuid.uuid4()}.jpg"
        save_file_name5 = f"/tmp/Q5-Gender-{uuid.uuid4()}.jpg"
        
        image_urls['Q1'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name1)}")
        image_urls['Q2'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name2)}")
        image_urls['Q3'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name3)}")
        image_urls['Q4'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name4)}")
        image_urls['Q5'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name5)}")
        
        # Visualize basic layout based on gender
        mn1.visualize_attr(save_file_name = save_file_name1, attr_dic = node_attributes_gender, s3_bucket = bucketname)
        mn2.visualize_attr(save_file_name = save_file_name2, attr_dic = node_attributes_gender, s3_bucket = bucketname)
        mn3.visualize_attr(save_file_name = save_file_name3, attr_dic = node_attributes_gender, s3_bucket = bucketname)
        mn4.visualize_attr(save_file_name = save_file_name4, attr_dic = node_attributes_gender, s3_bucket = bucketname)
        mn5.visualize_attr(save_file_name = save_file_name5, attr_dic = node_attributes_gender, s3_bucket = bucketname)
        
        save_file_name1 = f"/tmp/Q1-Age-{uuid.uuid4()}.jpg"
        save_file_name2 = f"/tmp/Q2-Age-{uuid.uuid4()}.jpg"
        save_file_name3 = f"/tmp/Q3-Age-{uuid.uuid4()}.jpg"
        save_file_name4 = f"/tmp/Q4-Age-{uuid.uuid4()}.jpg"
        save_file_name5 = f"/tmp/Q5-Age-{uuid.uuid4()}.jpg"
        
        image_urls['Q1'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name1)}")
        image_urls['Q2'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name2)}")
        image_urls['Q3'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name3)}")
        image_urls['Q4'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name4)}")
        image_urls['Q5'].append(f"https://{bucketname}.s3.amazonaws.com/{os.path.basename(save_file_name5)}")
        
        print(image_urls)
    
        
        # Visualize basic layout based on age
        mn1.visualize_attr(save_file_name = save_file_name1, attr_dic = node_attributes_age, s3_bucket = bucketname)
        mn2.visualize_attr(save_file_name = save_file_name2, attr_dic = node_attributes_age, s3_bucket = bucketname)
        mn3.visualize_attr(save_file_name = save_file_name3, attr_dic = node_attributes_age, s3_bucket = bucketname)
        mn4.visualize_attr(save_file_name = save_file_name4, attr_dic = node_attributes_age, s3_bucket = bucketname)
        mn5.visualize_attr(save_file_name = save_file_name5, attr_dic = node_attributes_age, s3_bucket = bucketname)
        
        # calculate network statistics
        mn1.statistics()
        mn2.statistics()
        mn3.statistics()
        mn4.statistics()
        mn5.statistics()
        
        # extract statistics ranks from statistics. Need to return these values to frontend as json
        dic1 = mn1.extract_level_from_statistics()
        dic2 = mn2.extract_level_from_statistics()
        dic3 = mn3.extract_level_from_statistics()
        dic4 = mn4.extract_level_from_statistics()
        dic5 = mn5.extract_level_from_statistics()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Success',
                'image_urls': image_urls,
                "statistics": {
                    'Q1': dic1,
                    'Q2': dic2,
                    'Q3': dic3,
                    'Q4': dic4,
                    'Q5': dic5
                }
            })
        }
                        
        
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
        'statusCode': 400,
        'body': json.dumps(str(err))
        }
    
        