import sagemaker
import pandas as pd


sagemaker_session = sagemaker.Session()
region = sagemaker_session.boto_region_name
example_feature_group_name = 'example-feature-group-17-02-33-48'

# Helper to parse the feature value from the record.
def response_to_dataframe(response):
    record = response['Record']
    row = {feature['FeatureName']: feature['ValueAsString'] for feature in record}
    df = pd.DataFrame(row, index=[0])
    print(df)
    return df

record_identifier_feature_name = "column_1"
record_identifier = 3212
record_response = sagemaker_session.boto_session.client(
    "sagemaker-featurestore-runtime", region_name=region
).get_record(
    FeatureGroupName=example_feature_group_name, RecordIdentifierValueAsString=str(record_identifier)
)

response_to_dataframe(record_response)