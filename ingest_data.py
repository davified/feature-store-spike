import time
import sagemaker
import pandas as pd
from sagemaker.session import Session
from sagemaker import get_execution_role
from sagemaker.feature_store.feature_group import FeatureGroup

sagemaker_session = sagemaker.Session()
region = sagemaker_session.boto_region_name
s3_bucket_name = sagemaker_session.default_bucket()

example_feature_group_name = 'example-feature-group-17-02-33-48'

example_feature_group = FeatureGroup(
    name=example_feature_group_name, sagemaker_session=sagemaker_session
)

# load data
example_data = pd.read_csv("data/data-small.csv", index_col=0) # data-small: 15MB dataset
# append EventTime
current_time_sec = int(round(time.time()))
example_data["EventTime"] = pd.Series([current_time_sec] * len(example_data), dtype="float64")

example_feature_group.ingest(data_frame=example_data, max_workers=16, wait=True)  # use python <=3.7. otherwise this line will fail: https://github.com/aws/sagemaker-python-sdk/pull/2573
