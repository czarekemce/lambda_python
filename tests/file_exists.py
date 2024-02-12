import boto3
import os

first_bucket = os.environ.get('FIRST_BUCKET')
client = boto3.client('s3')

objects = client.list_objects_v2(Bucket=first_bucket)
contents = objects['Contents']
for key in contents:
    files_in_bucket = key['Key']
    if 'test.txt' in files_in_bucket:
        print('File in bucket: Success')
    else:
        print('There is no file test.txt')

