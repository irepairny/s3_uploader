from flask import Flask, request, jsonify, send_from_directory
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__, static_folder='static')

# Configure your AWS credentials and region
s3_client = boto3.client('s3', region_name='us-east-1')  # change region if needed
BUCKET_NAME = 'your-s3-bucket-name'  # Replace with your bucket name

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generate-presigned-url', methods=['POST'])
def generate_presigned_url():
    data = request.get_json()
    file_name = data.get('file_name')

    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600
        )
        return jsonify({'url': response})
    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not available'}), 500

if __name__ == '__main__':
    app.run(debug=True)
