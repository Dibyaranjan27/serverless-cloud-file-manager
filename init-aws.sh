#!/bin/bash

echo "Initializing LocalStack AWS resources..."

# Create S3 Bucket
awslocal s3 mb s3://cloud-file-manager-bucket

# Create DynamoDB Table
awslocal dynamodb create-table \
    --table-name FileMetadata \
    --attribute-definitions AttributeName=file_id,AttributeType=S \
    --key-schema AttributeName=file_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Package Lambda function
cd /lambda
zip process_file.zip process_file.py

# Create Lambda Function
awslocal lambda create-function \
    --function-name ProcessFileLambda \
    --runtime python3.9 \
    --handler process_file.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --zip-file fileb://process_file.zip \
    --timeout 30

# Configure S3 to trigger Lambda
awslocal s3api put-bucket-notification-configuration \
    --bucket cloud-file-manager-bucket \
    --notification-configuration '{"LambdaFunctionConfigurations": [{"LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:ProcessFileLambda", "Events": ["s3:ObjectCreated:*"]}]}'

echo "Initialization complete!"

