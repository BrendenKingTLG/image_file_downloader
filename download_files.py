import boto3
from botocore.config import Config
from botocore import UNSIGNED
import os
from datetime import datetime

BUCKET_NAME = 'osm-planet-us-west-2'
PREFIX = 'planet/replication/day/000/004/'
LAST_DOWNLOADED_FILE = 'last_downloaded.txt'
WEEKLY_FILE_COUNT = 7
DOWNLOAD_LOCATION = './'

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def get_last_downloaded_index():
    """
    Retrieve the index of the last downloaded file from the LAST_DOWNLOADED_FILE.

    Returns:
        int: The index of the last downloaded file.

    Raises:
        FileNotFoundError: If the LAST_DOWNLOADED_FILE does not exist.
    """
    try:
        with open(LAST_DOWNLOADED_FILE, 'r') as file:
            index = file.read().strip()
            return int(index)
    except FileNotFoundError:
        raise FileNotFoundError(f'{LAST_DOWNLOADED_FILE} not found')

def update_last_downloaded_index(index):
    """
    Update the index of the last downloaded file in the LAST_DOWNLOADED_FILE.

    Args:
        index (int): The index to write to the file.

    Raises:
        FileNotFoundError: If the LAST_DOWNLOADED_FILE does not exist.
    """
    try:
        with open(LAST_DOWNLOADED_FILE, 'w') as file:
            file.write(str(index))
    except FileNotFoundError:
        raise FileNotFoundError(f'{LAST_DOWNLOADED_FILE} not found')
    
def download_files():
    """
    Download files from the specified S3 bucket starting from the index specified
    in the LAST_DOWNLOADED_FILE. Updates the file index after downloading.

    Downloads up to WEEKLY_FILE_COUNT files and saves them in the DOWNLOAD_LOCATION.
    """
    download_index = get_last_downloaded_index()
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX,
        StartAfter=f'{PREFIX}{str(download_index)}.state.txt',
        MaxKeys=WEEKLY_FILE_COUNT
    )

    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj)
            file_name = obj['Key'].split('/')[-1]
            s3.download_file(BUCKET_NAME, obj['Key'], os.path.join(DOWNLOAD_LOCATION, file_name))

    
if __name__ == '__main__':
    download_files()
import boto3
from botocore.config import Config
from botocore import UNSIGNED
import os
from datetime import datetime

# Constants for bucket configuration and file handling
BUCKET_NAME = 'osm-planet-us-west-2'
PREFIX = 'planet/replication/day/000/004/'
LAST_DOWNLOADED_FILE = 'last_downloaded.txt'
WEEKLY_FILE_COUNT = 7
DOWNLOAD_LOCATION = './'

# Create an S3 client with unsigned requests
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def get_last_downloaded_index():
    """
    Retrieve the index of the last downloaded file from the LAST_DOWNLOADED_FILE.

    Returns:
        int: The index of the last downloaded file.

    Raises:
        FileNotFoundError: If the LAST_DOWNLOADED_FILE does not exist.
    """
    try:
        with open(LAST_DOWNLOADED_FILE, 'r') as file:
            index = file.read().strip()
            return int(index)
    except FileNotFoundError:
        raise FileNotFoundError(f'{LAST_DOWNLOADED_FILE} not found')

def update_last_downloaded_index(index):
    """
    Update the index of the last downloaded file in the LAST_DOWNLOADED_FILE.

    Args:
        index (int): The index to write to the file.

    Raises:
        FileNotFoundError: If the LAST_DOWNLOADED_FILE does not exist.
    """
    try:
        with open(LAST_DOWNLOADED_FILE, 'w') as file:
            file.write(str(index))
    except FileNotFoundError:
        raise FileNotFoundError(f'{LAST_DOWNLOADED_FILE} not found')
    
def download_files():
    """
    Download files from the specified S3 bucket starting from the index specified
    in the LAST_DOWNLOADED_FILE. Updates the file index after downloading.

    Downloads up to WEEKLY_FILE_COUNT files and saves them in the DOWNLOAD_LOCATION.
    
    Returns:
        int: The new index of the last downloaded file.
    """
    download_index = get_last_downloaded_index()
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX,
        StartAfter=f'{PREFIX}{str(download_index)}.state.txt',
        MaxKeys=WEEKLY_FILE_COUNT
    )

    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj)
            file_name = obj['Key'].split('/')[-1]
            s3.download_file(BUCKET_NAME, obj['Key'], os.path.join(DOWNLOAD_LOCATION, file_name))
            
    return download_index + WEEKLY_FILE_COUNT

def main():
    new_index = download_files()
    update_last_downloaded_index(new_index)
    
if __name__ == '__main__':
    main()
