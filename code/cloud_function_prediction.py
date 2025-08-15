import os
import base64
import logging
from google.cloud import aiplatform
from google.cloud import storage

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hello_gcs(event, context):
    """Triggered by GCS upload. Sends image to Vertex AI and logs prediction."""
    bucket_name = event['bucket']
    file_name = event['name']
    logger.info(f"Processing file: {file_name} from bucket: {bucket_name}")

    try:
        # Download image from GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        image_bytes = blob.download_as_bytes()
        logger.info(f"Downloaded image {file_name} successfully.")

        # Encode image in base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        instance = {"content": encoded_image}

        # Get env vars from Cloud Function config
        project_id = os.environ.get("PROJECT_ID")
        region = os.environ.get("REGION")
        endpoint_id = os.environ.get("ENDPOINT_ID")

        # Init Vertex AI
        aiplatform.init(project=project_id, location=region)
        endpoint = aiplatform.Endpoint(endpoint_id)

        # Predict
        response = endpoint.predict(instances=[instance])
        logger.info(f"Prediction results for {file_name}: {response.predictions}")

    except Exception as e:
        logger.error(f"Error processing file {file_name}: {str(e)}")
        raise e
