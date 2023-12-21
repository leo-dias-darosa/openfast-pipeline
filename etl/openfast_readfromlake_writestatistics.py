import boto3
import os
import pandas as pd
import io
import s3fs
import pyarrow.parquet as pq

# Bucket name and Database URI
bucket_name = "openfast-data"
database_uri = f"s3://{bucket_name}/processed-data/"

descriptive_statiscs_data = (
    f"{bucket_name}/"
    "processed-data/"
    "openfast_descriptive_statistics/"
)
session = boto3.Session(profile_name="leo-profile")
# Initialize boto and bucket used
s3 = session.resource('s3', region_name='sa-east-1')
bucket = s3.Bucket(bucket_name)

# Read data that already exist in openfast-database bucket
fs = s3fs.S3FileSystem(profile="leo-profile")

existing_df = pq \
    .read_table(descriptive_statiscs_data, filesystem=fs) \
    .to_pandas()

# Columns that do not need to be aggregated and initiate dict
columns_to_drop = ["Wind1VelY", "Wind1VelZ", "RtAeroCp", "RtAeroCt",
                   "RtSkew", "Time", "YawPzn", "timestamp"]

new_data = {"timestamp": [], "turbine": []}

# Iterate over all existing objects
file_number = 1
files_to_process = len(list(bucket.objects.filter(Prefix="data-lake/"))) - len(existing_df)
for obj in bucket.objects.all():
    obj_name = obj.key

    if os.path.dirname(obj_name).startswith("data-lake") and obj_name.endswith(".parquet"):

        print(f"Reading file {obj_name}...")

        name_list = obj_name.split("/")

        # Get turbine name
        turbine = name_list[1]

        # Get timestamp of data
        timestamp, _ = os.path.splitext(name_list[2])

        # Check if the current parquet was already processed
        if (timestamp in existing_df["timestamp"].values and
                turbine in existing_df["turbine"].values):
            print("This file was processed already!")

        else:
            print(f"Starting processing file {file_number} out of approximately {files_to_process} files to process")

            # Create pandas dataframe from this file data
            df = pd \
                .read_parquet(
                    io
                    .BytesIO(
                        obj
                        .get()['Body']
                        .read()
                    )
                )

            # Add timestamp and turbine name
            new_data["timestamp"].append(timestamp)
            new_data["turbine"].append(turbine)

            # Drop columns that shouldn't be aggregated
            df = df.drop(columns=columns_to_drop) \
                .apply(pd.to_numeric, errors='coerce')

            # Initialize dict keys if this is the first file in the processing
            if file_number == 1:
                for column in df.columns:
                    new_data[column + "_avg"] = []
                    new_data[column + "_std"] = []
                    new_data[column + "_min"] = []
                    new_data[column + "_max"] = []

            # Creates avg, max, min, and std deviation for all columns
            for column in df.columns:
                new_data[column + "_avg"].append(df[column].mean())
                new_data[column + "_std"].append(df[column].std())
                new_data[column + "_min"].append(df[column].min())
                new_data[column + "_max"].append(df[column].max())

            file_number = file_number + 1

print("Finish processing...")
# Transform dict data in new pandas dataframe
processed_data = pd.DataFrame().from_dict(new_data)

# Concatenate new processed data to the existing dataframe
output_data = pd.concat([existing_df, processed_data], axis=0)

print(f"Saving to {database_uri}openfast_descriptive_statistics")

output_data.to_parquet(database_uri + "openfast_descriptive_statistics",
                       partition_cols=["turbine"],
                       index=False)
