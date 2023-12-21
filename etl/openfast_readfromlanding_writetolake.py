import boto3
import pandas as pd
import os

# Initialize s3
s3 = boto3.resource('s3', region_name='sa-east-1')

# Define buckets names
bucket_name = "openfast-data"
lake_bucket = f"s3://${bucket_name}/data-lake/"

# Create landing bucket (openfast-data/landing-data) object
bucket = s3.Bucket(bucket_name)

# Iterate over all landing bucket objects
for obj in bucket.objects.all():
    obj_name = obj.key
    if os.path.dirname(obj_name).startswith("landing-data") and obj_name.endswith(".out"):
        openfast_data = []
        
        # Get file name
        file_name = os.path.basename(obj_name)
        name_list = file_name.split("-")
        # Get turbine name
        turbine_name = name_list[0]

        # Get timestamp of data
        timestamp = name_list[1][:-4]
    
        # Transform obj data to python list
        file_data = obj.get()['Body'].readlines()
        
        # Get openfast line respective to the columns
        openfast_columns = file_data[6].decode("utf8").split()
        
        for line, data in enumerate(file_data):
            # Remove not used lines from file
            # Transform bytes lines to list of strings.
            if line > 7:
                openfast_data.append(data.decode("utf8").split())
    
        # Create pandas dataframe from list
        df = pd.DataFrame(columns=openfast_columns, data=openfast_data, index=None)
    
        # Create timestamp column
        df["timestamp"] = timestamp
    
        # Save data to openfast-data/data-lake bucket
        df.to_parquet(lake_bucket+turbine_name+"/"+timestamp+".parquet", index=False)
    
        # Delete file from landing bucket
        s3.Object(bucket_name, obj_name).delete()
