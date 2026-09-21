import json
import urllib.parse
import boto3
import uuid
from datetime import datetime
import os

print('Loading function')

s3 = boto3.client('s3', endpoint_url=f"http://{os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')}:4566")
dynamodb = boto3.resource('dynamodb', endpoint_url=f"http://{os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')}:4566")

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the object from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        size = event['Records'][0]['s3']['object']['size']
        
        print(f"Processing file: {key} from bucket {bucket} with size {size}")
        
        table = dynamodb.Table('FileMetadata')
        
        file_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Insert record into DynamoDB
        response = table.put_item(
            Item={
                'file_id': file_id,
                'filename': key,
                'bucket': bucket,
                'size_bytes': size,
                'upload_timestamp': timestamp
            }
        )
        
        print(f"Successfully inserted metadata for {key} into DynamoDB")
        return {
            'statusCode': 200,
            'body': json.dumps('File processed successfully!')
        }
    except Exception as e:
        print(e)
        print("Error processing object. Make sure it exists and your bucket is in the same region as this function.")
        raise e

