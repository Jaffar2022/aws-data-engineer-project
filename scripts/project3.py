# Program to upload all local sales data files to S3 and verify the upload

import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# ====== CONFIG ======
# ====== CONFIG ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_FOLDER = os.path.join(BASE_DIR, "..", "data")

BUCKET_NAME = "awsdeprojects"
S3_PREFIX = "raw/sales/"

# ====================

s3 = boto3.client("s3")


def upload_folder_to_s3(local_folder, bucket, s3_prefix):
    uploaded_files = []
    failed_files = []

    print(f"\n📂 Scanning local folder: {local_folder}\n")

    for root, dirs, files in os.walk(local_folder):
        for file in files:
            if file.startswith("."):
                continue  # skip hidden files

            local_path = os.path.join(root, file)

            # Preserve folder structure inside S3
            relative_path = os.path.relpath(local_path, local_folder)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            try:
                print(f"⬆️ Uploading: {local_path}")
                print(f"   → s3://{bucket}/{s3_key}")

                s3.upload_file(local_path, bucket, s3_key)
                uploaded_files.append(s3_key)

            except FileNotFoundError:
                print(f"❌ File not found: {local_path}")
                failed_files.append(local_path)

            except NoCredentialsError:
                print("❌ AWS credentials not configured")
                return

            except ClientError as e:
                print(f"❌ Failed to upload {local_path}")
                print(f"   Error: {e}")
                failed_files.append(local_path)

    return uploaded_files, failed_files


def verify_upload(bucket, prefix):
    print("\n🔍 Verifying uploaded files in S3...\n")

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    if "Contents" in response:
        for obj in response["Contents"]:
            print(f"✅ {obj['Key']}")
    else:
        print("⚠️ No files found in S3 under this prefix")


if __name__ == "__main__":
    uploaded, failed = upload_folder_to_s3(
        LOCAL_FOLDER,
        BUCKET_NAME,
        S3_PREFIX
    )

    print("\n📊 Upload Summary:")
    print(f"✔️ Uploaded: {len(uploaded)} files")
    print(f"❌ Failed: {len(failed)} files")

    verify_upload(BUCKET_NAME, S3_PREFIX)

    print("\n🎉 Done!\n")