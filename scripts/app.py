import boto3
from botocore.exceptions import NoCredentialsError

# Initialize S3 client
s3 = boto3.client('s3')

# ---------- UPLOAD FUNCTION ----------
def upload_file(file_name, bucket, object_name=None):
    try:
        if object_name is None:
            object_name = file_name

        s3.upload_file(file_name, bucket, object_name)
        print(f"✅ File '{file_name}' uploaded to '{bucket}/{object_name}'")

    except FileNotFoundError:
        print("❌ File not found")
    except NoCredentialsError:
        print("❌ AWS credentials not configured")


# ---------- DOWNLOAD FUNCTION ----------
def download_file(bucket, object_name, file_name):
    try:
        s3.download_file(bucket, object_name, file_name)
        print(f"✅ File '{object_name}' downloaded from '{bucket}'")

    except Exception as e:
        print(f"❌ Error: {e}")


# ---------- MAIN ----------
if __name__ == "__main__":
    bucket_name = "awsdeprojects"

    # Upload example
    upload_file("../data/sample.csv", bucket_name, "raw/sample.csv")

    # Download example
    download_file(bucket_name, "raw/sample.csv", "downloaded_sample.csv")