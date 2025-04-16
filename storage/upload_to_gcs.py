from google.cloud import storage

from config import logger, STORAGE_MAX_USAGE_GB


def check_storage_usage():
    client = storage.Client()

    total_size_bytes = 0

    for bucket in client.list_buckets():
        for blob in client.list_blobs(bucket):
            try:
                size = int(blob.size)  # force to int in case it's string or None
                total_size_bytes += size
            except (TypeError, ValueError):
                continue  # skip blobs with no/invalid size

    total_size_gb = total_size_bytes / (1024 ** 3)
    logger.info(
        f"Total size: {total_size_gb} (type: {type(total_size_gb)}), "
        f"Limit: {STORAGE_MAX_USAGE_GB} (type: {type(STORAGE_MAX_USAGE_GB)})"
    )

    if total_size_gb > STORAGE_MAX_USAGE_GB:
        raise Exception(f"Cloud Storage limit exceeded: {total_size_gb:.2f}GB used.")


def upload_to_gcs(local_path, bucket_name, blob_name):
    try:
        check_storage_usage()
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_path)
        logger.info(f"Uploaded {local_path} to GCS bucket '{bucket_name}' as '{blob_name}'")
    except Exception as e:
        logger.error(f"Failed to upload {local_path} to GCS: {e}")

