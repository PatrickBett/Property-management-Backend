# utils.py

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings

def upload_file_to_s3(file, bucket_name, key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    try:
        # Upload the file
        s3.upload_fileobj(file, bucket_name, key)
        print(f"File uploaded successfully to {bucket_name}/{key}")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
