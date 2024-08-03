import boto3
from botocore.exceptions import NoCredentialsError, ClientError

S3_BUCKET_NAME = 'your-new-bucket-name'
S3_REGION = 'your-region'  
S3_ACCESS_KEY = 'your-access-key'
S3_SECRET_KEY = 'your-secret-key'

def upload_to_s3(file_name, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )

    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, S3_BUCKET_NAME, object_name)
        print(f"File {file_name} uploaded to {S3_BUCKET_NAME} as {object_name}.")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except ClientError as e:
        print(f"Failed to upload {file_name}: {e}")
        return False

if __name__ == "__main__":
    file_to_upload = 'local-file.txt'  
    success = upload_to_s3(file_to_upload)
    if success:
        print("Upload succeeded.")
    else:
        print("Upload failed.")
