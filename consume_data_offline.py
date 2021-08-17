import sagemaker
import pandas as pd
from sagemaker.feature_store.feature_group import FeatureGroup


sagemaker_session = sagemaker.Session()
region = sagemaker_session.boto_region_name
s3_bucket_name = sagemaker_session.default_bucket()
prefix = "sagemaker-featurestore-introduction"
example_feature_group_name = 'example-feature-group-17-02-33-48'
example_feature_group = FeatureGroup(
    name=example_feature_group_name, sagemaker_session=sagemaker_session
)


example_query = example_feature_group.athena_query()

example_table = example_query.table_name

query_string = (
    'SELECT * FROM "'
    + example_table + '"'
)
print("Running " + query_string)

# run Athena query. The output is loaded to a Pandas dataframe.
example_query.run(
    query_string=query_string,
    output_location="s3://" + s3_bucket_name + "/" + prefix + "/query_results/",
)
example_query.wait()
df = example_query.as_dataframe()

print(df.info())