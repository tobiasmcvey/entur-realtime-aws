#python lambda function to send estimated timetable data to cloudwatch and kinesis
import json
import xmltodict
import logging
import sys
import boto3
import datetime

logger = logging.getLogger(__name__) # for logging and debugging data transformation
client = boto3.client('kinesis')

#set logging level to INFO to avoid debug output
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(log_handler)

# Filter out keys 
# Flatten dict one level to avoid 'Siri' level
def transform_siri_data(event):
    siri_data = xmltodict.parse(event.get('bodyXml'))
    logger.debug("Filter out values starting with '@' from siri data %s", siri_data)
 
    filtered_siri_data = {}
    # the dict is located under Siri key
    if 'Siri' in siri_data:
        # Dict in dict
        siri_sub_dict = siri_data.get('Siri')
        for key in siri_sub_dict.keys():
            if not key.startswith('@'):
                filtered_siri_data[key] = siri_sub_dict.get(key)
            else: 
                logger.debug("Filtering out key from dict: %s", key)
        return filtered_siri_data
    #print(filtered_siri_data)
    # Ignore certain types of siri data if not suitable for indexing
def allow_content(transformed_siri_data):
    #print(transformed_siri_data) # prints an ordered dictionary type
    if 'HeartbeatNotification' in transformed_siri_data:
        return False

    # defaults to True for now
    return True

    # use this to put record to Kinesis stream
def post_to_kinesis(transformed_siri_data):
    client.put_record(
        StreamName='',
        Data=json.dumps(transformed_siri_data),
        PartitionKey=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    )

# lambda function for AWS API Gateway
def lambda_handler(event, context):
    print("Received event. Converting body to dict")
    transformed_siri_data = transform_siri_data(event)
    print(json.dumps(transformed_siri_data)) # this is what we want for kinesis
    if allow_content(transformed_siri_data):
        logger.info("Data is suitable for indexing")
        logger.debug("Converting to json")
        post_to_kinesis(transformed_siri_data)

    # TODO implement
    return {
        'statusCode': '200',
        'body': 'Siri data received'
    }
