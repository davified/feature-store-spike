# SageMaker Feature Store spike

## Problems with current architecture
- Redundant data download to AWS compute instances
    - training data (23 GB - 7 mins)
    - inference (250 GB - ?? mins)

## Business value
- Read-optimised cache
- Offline store: Save time in data download for each SubModel
    - Save 10s of minutes in end-to-end training
    - Iterate more quickly towards north star of improving model accuracy
- Online store: Remove complexity/re-work around making data available at low-latency for real-time API requests

## Commands

```sh
# build image
docker build . -t feature-store-spike

# start container
docker run -it -v $(pwd):/app feature-store-spike bash 

# copy and paste credentials in docker container
export AWS_DEFAULT_REGION=ap-southeast-2

# on AWS, update my role > trust relationship > to include: #

{
    "Effect": "Allow",
    "Principal": {
        "Service": "sagemaker.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
}
# https://stackoverflow.com/questions/56240769/sagemaker-clienterror-an-error-occurred-validationexception-when-calling-the

# optional: create data
python create_dataset.py

# create feature group
python create_feature_group.py

# ingest data from local filesystem into Feature Store
python ingest_data.py

# consume data from Feature Store (online)
python consume_data_online.py

# consume data from Feature Store (offline)
python consume_data_offline.py
```

## Learnings:
- Have to first cast dataframe to include only types accepted by Feature Store: https://sagemaker-examples.readthedocs.io/en/latest/ml-lifecycle/feature_store/FS_demo.html?highlight=integral#Prepare-data-For-Feature-Store
- Have to use Python <= 3.7 due to bug: https://github.com/aws/sagemaker-python-sdk/pull/2573
- Consuming feature
    - Online store
        - Some minimal work is needed to convert a Record to a Pandas DataFrame
    - Offline
        - Batch download of all data
            - better to use Athena query than `batch_get_record()` (the latter requires that you provide a list of record identifiers)
                - see example: https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-featurestore/sagemaker_featurestore_fraud_detection_python_sdk.html#Ingest-Data-into-FeatureStore

- Questions:
    - how to handle schema changes?
    - how to update/overwrite records? is it append-only?

## Useful resources:
- Overview: https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html
- Code sample: https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-featurestore/feature_store_introduction.html
- Data ingestion options: https://sagemaker-examples.readthedocs.io/en/latest/ingest_data/index.html

