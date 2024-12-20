import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename

from config import Config

s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config().AWS_SECRET_ACCESS_KEY,
    region_name=Config().S3_REGION_NAME,
)


def upload_file_to_s3(file, bucket_name=Config().S3_BUCKET_NAME):
    """
    Uploads a file to an S3 bucket and returns the file's URL.
    Ensures unique filenames by appending a UUID.
    """
    try:
        # Secure the original filename
        original_filename = secure_filename(file.filename)
        # Generate a unique filename using UUID
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

        # Upload the file to S3
        s3_client.upload_fileobj(
            file,
            bucket_name,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type},  # Remove ACL
        )

        # Return the S3 URL of the uploaded file
        s3_url = f"https://{bucket_name}.s3.{Config().S3_REGION_NAME}.amazonaws.com/{unique_filename}"
        return s3_url
    except NoCredentialsError:
        raise Exception("AWS credentials not available")


def delete_file_from_s3(file_key, bucket_name=Config().S3_BUCKET_NAME):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        raise Exception(f"Failed to delete file: {str(e)}")
