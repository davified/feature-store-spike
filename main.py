import sagemaker
import sys
import boto3
import pandas as pd
import numpy as np
import io
import time
from sagemaker.session import Session
from sagemaker import get_execution_role
from sagemaker.feature_store.feature_group import FeatureGroup
from time import gmtime, strftime, sleep

prefix = "sagemaker-featurestore-introduction"
role = get_execution_role()

sagemaker_session = sagemaker.Session()
region = sagemaker_session.boto_region_name
s3_bucket_name = sagemaker_session.default_bucket()

# create feature group

example_feature_group_name = "example-feature-group-" + strftime("%d-%H-%M-%S", gmtime())
example_feature_group = FeatureGroup(
    name=example_feature_group_name, sagemaker_session=sagemaker_session
)

current_time_sec = int(round(time.time()))
record_identifier_feature_name = ""

# load data
example_data = pd.read_csv("data/example-training-part-1.csv")

# Append EventTime feature to your data frame 
example_data["EventTime"] = pd.Series([current_time_sec] * len(example_data), dtype="float64")

# Preprocess
# convert pandas columns with dtype object to dtype string
# columns_to_convert_to_str = obj_columns + bool_columns
# for col in columns_to_convert_to_str:
#     example_data = example_data.astype({col: pd.StringDtype()})

print(example_data.info())
# Load feature definitions to your feature group.
example_feature_group.load_feature_definitions(data_frame=example_data)

# create feature group
example_feature_group.create(
    s3_uri=f"s3://{s3_bucket_name}/{prefix}",
    record_identifier_name=record_identifier_feature_name,
    event_time_feature_name="EventTime",
    role_arn=role,
    enable_online_store=True,
)

# To confirm that FeatureGroup has been created
print(example_feature_group.describe())

# sagemaker_session.boto_session.client(
#     "sagemaker", region_name=region
# ).list_feature_groups()  # We use the boto client to list FeatureGroups
