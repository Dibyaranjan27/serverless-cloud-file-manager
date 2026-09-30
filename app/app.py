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

@app.template_filter('format_size')
def format_size(size_in_bytes):
    try:
        size = float(size_in_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except (ValueError, TypeError):
        return size_in_bytes

@app.template_filter('format_time')
def format_time(timestamp_str):
    try:
        # Example format: 2026-09-29T18:45:14.908332
        # Split at T and remove microseconds
        date_part, time_part = timestamp_str.split('T')
        time_part = time_part.split('.')[0]
        return f"{date_part} {time_part}"
    except Exception:
        return timestamp_str

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
        
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
        
    success_count = 0
    from werkzeug.utils import secure_filename
    for file in files:
        if file.filename:
            try:
                safe_filename = secure_filename(file.filename)
                s3_client.upload_fileobj(file, BUCKET_NAME, safe_filename)
                success_count += 1
            except ClientError as e:
                print(f"S3 Error: {e}")
                flash(f"Failed to upload {safe_filename}: {e}", 'error')
                
    if success_count > 0:
        flash(f"Successfully uploaded {success_count} file(s) to S3!", 'success')
        
    return redirect(url_for('index'))

from flask import send_file
import io

@app.route('/download/<filename>')
def download_file(filename):
    from werkzeug.utils import secure_filename
    safe_filename = secure_filename(filename)
    try:
        file_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=safe_filename)
        return send_file(
            io.BytesIO(file_obj['Body'].read()),
            download_name=safe_filename,
            as_attachment=True
        )
    except ClientError as e:
        print(f"S3 Download Error: {e}")
        flash(f"Failed to download from S3: {e}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

