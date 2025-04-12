from google.cloud import storage

from config import logger, STORAGE_MAX_USAGE_GB


def check_storage_usage():
    client = storage.Client()
    total_size_gb = sum(
        blob.size for bucket in client.list_buckets()
        for blob in client.list_blobs(bucket)
    ) / (1024 ** 3)

    if total_size_gb > STORAGE_MAX_USAGE_GB:
        raise Exception(f"Cloud Storage limit exceeded: {total_size_gb:.2f}GB used.")


def upload_to_gcs(local_path, bucket_name, blob_name):
    check_storage_usage()
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    logger.INFO(f"✅ Uploaded {local_path} to GCS bucket '{bucket_name}' as '{blob_name}'")
