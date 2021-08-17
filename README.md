# SageMaker Feature Store spike

## Problems with current architecture
- Redundant data download to AWS compute instances
    - training data (23 GB - 7 mins)
    - inference (250 GB - ?? mins)

## Business value
- Read-optimised cache
- Offline store: Save time in data download for each SubModel
    - Save 10s of minutes in end-to-end training
    - Iterate more quickly towards north star of improving AVM accuracy
- Online store: Potential to be used by LAA and reduce complexity around daily data ingestion from BQ to Postgres

## Commands

```sh
# start container
docker run -it -v $(pwd):/app feature-store-spike bash 

# copy and paste credentials in docker container
export AWS_DEFAULT_REGION=ap-southeast-2

# run script
python main.py 


```


## Clean up

- delete
    - [x] username: default-1629162139032
    - [x] execution role: AmazonSageMaker-ExecutionRole-20210817T110374 
