import boto3
import os

s3 = boto3.client("s3")

BUCKET = "awsdeprojects"
PREFIX = "processed/sales/"
LOCAL_BASE = "./parquet_downloads"

def download_files():
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        if "Contents" not in page:
            continue

        for obj in page["Contents"]:
            key = obj["Key"]

            if key.endswith(".parquet"):
                local_path = os.path.join(LOCAL_BASE, key)

                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                print(f"Downloading {key}")
                s3.download_file(BUCKET, key, local_path)

download_files()