import os
from datetime import datetime

import boto3
from botocore.config import Config
from botocore import UNSIGNED

BUCKET_NAME = 'osm-planet-us-west-2'
PREFIX = 'planet/replication/day/000/004/'
LAST_DOWNLOADED_FILE = 'last_downloaded.txt'
DAILY_FILE_COUNT = 1 * 2 # one state and one change file per day
DOWNLOAD_LOCATION = './'

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
def download_files():
    """
    Download files from the specified S3 bucket starting from the index specified
    in the LAST_DOWNLOADED_FILE. Updates the file index after downloading.

    Downloads up to DAILY_FILE_COUNT files and saves them in the DOWNLOAD_LOCATION.
    """
    download_index = get_last_downloaded_index()
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX,
        StartAfter=f'{PREFIX}{str(download_index)}.state.txt',
        MaxKeys=DAILY_FILE_COUNT
    )

    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj)
            file_name = obj['Key'].split('/')[-1]
            s3.download_file(BUCKET_NAME, obj['Key'], os.path.join(DOWNLOAD_LOCATION, file_name))

    return download_index + DAILY_FILE_COUNT/2

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

def update_index_file(index):
    """
    Update the index of the last downloaded file in the LAST_DOWNLOADED_FILE.

    Args:
        index (int): The index to write to the file.

    Raises:
        FileNotFoundError: If the LAST_DOWNLOADED_FILE does not exist.
    """
    try:
        with open(LAST_DOWNLOADED_FILE, 'w') as file:
            file.write(str(int(index)))
    except FileNotFoundError:
        raise FileNotFoundError(f'{LAST_DOWNLOADED_FILE} not found')

def main():
    new_index = download_files()
    update_index_file(new_index)
    
if __name__ == '__main__':
    main()
