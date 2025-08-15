import os
from google.cloud import storage

def upload_to_gcs(bucket_name, source_folder, destination_folder):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for image_name in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, image_name)
        destination_blob_name = f"{destination_folder}/{image_name}"
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        print(f"File {image_name} uploaded to {destination_blob_name}.")

# Replace with your bucket name and folder paths
bucket_name = "captured_images"
source_folder = "captured_images"
destination_folder = "images"  # Folder in the bucket

upload_to_gcs(bucket_name, source_folder, destination_folder)
