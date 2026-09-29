import os
from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_local_dev'

# Configure boto3 to use LocalStack
AWS_ENDPOINT = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')
BUCKET_NAME = 'cloud-file-manager-bucket'

s3_client = boto3.client('s3', endpoint_url=AWS_ENDPOINT)
dynamodb = boto3.resource('dynamodb', endpoint_url=AWS_ENDPOINT)

@app.route('/')
def index():
    table = dynamodb.Table('FileMetadata')
    files = []
    try:
        response = table.scan()
        files = response.get('Items', [])
        # Sort by upload time descending
        files.sort(key=lambda x: x.get('upload_timestamp', ''), reverse=True)
    except ClientError as e:
        print(f"DynamoDB Error: {e}")
        flash('Could not connect to database. Ensure LocalStack is running and initialized.', 'error')
    
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
        
    try:
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
        flash(f"File '{file.filename}' successfully uploaded to S3!", 'success')
    except ClientError as e:
        print(f"S3 Error: {e}")
        flash(f"Failed to upload to S3: {e}", 'error')
        
    return redirect(url_for('index'))

from flask import send_file
import io

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        return send_file(
            io.BytesIO(file_obj['Body'].read()),
            download_name=filename,
            as_attachment=True
        )
    except ClientError as e:
        print(f"S3 Download Error: {e}")
        flash(f"Failed to download from S3: {e}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

