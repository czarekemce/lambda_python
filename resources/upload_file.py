import boto3
import os

first_bucket = os.environ.get('FIRST_BUCKET')

def create_file():
    with open('test.txt', 'w') as file:
        file.write('Some text')

client = boto3.client('s3')

def upload_file(file_name, bucket, object_name):
    try:
        client.upload_file(file_name, bucket, object_name)
        print("Upload file: Success")
    except Exception as e:
        print(e)

def test():
    list_bucket = client.list_buckets()
    response = list_bucket['Buckets']
    for name in response:
        bucket_name = name['Name']
        if first_bucket in bucket_name:
            try:
                upload_file(file_name='test.txt', bucket=first_bucket, object_name='test.txt')
            except Exception as e:
                print(e)

create_file()
test()

