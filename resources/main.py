import boto3
import time
import os

role_arn = os.environ.get('ROLE_ARN')
first_bucket = os.environ.get('FIRST_BUCKET')
second_bucket = os.environ.get('SECOND_BUCKET')

lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')


def create_lambda_function():
    try:
        create_response = lambda_client.create_function(
            FunctionName='CopyToBucket',
            Runtime='python3.12',
            Role=role_arn,
            Code={
                'S3Bucket': first_bucket,
                'S3Key': 'lambda_fun.zip'
            },
            Handler='lambda_function.handler_function'
        )
        lambda_function_full_arn = create_response['FunctionArn']
        print('Create function: Success')

    except Exception as e:
        print(f"Create function: {e}")

    try:
        permission_response = lambda_client.add_permission(
            FunctionName='CopyToBucket',
            StatementId='AllowToBeInvoked',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f"arn:aws:s3:::{first_bucket}"
        )
        time.sleep(5)
        print('Add permission: Success')
    except Exception as e:
        print(f"Add permission: {e}")

    try:
        lambda_client.get_policy(FunctionName='CopyToBucket')
        print('Get policy: Success')
    except Exception as e:
        print(f"Get policy: {e}")

    try:
        s3_client.put_bucket_notification_configuration(
            Bucket=first_bucket,
            NotificationConfiguration= {'LambdaFunctionConfigurations':[{'LambdaFunctionArn': lambda_function_full_arn, 'Events': ['s3:ObjectCreated:*']}]})
        print('Put bucket notification configuration: Success')
    except Exception as e:
        print(f"Put bucket notification configuration: {e}")


create_lambda_function()
