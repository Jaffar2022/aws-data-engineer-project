# This script downloads all Parquet files from the specified S3 bucket and prefix to a local directory.

import boto3
import os

s3 = boto3.client("s3")

BUCKET = "awsdeprojects"
PREFIX = "processed/sales/"

# 👉 Save outside scripts folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_BASE = os.path.join(BASE_DIR, "..", "parquet_downloads")

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

                print(f"⬇️ Downloading {key}")
                s3.download_file(BUCKET, key, local_path)

    print("✅ Download completed")

download_files()