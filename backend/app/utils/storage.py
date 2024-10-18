import os
import logging
import ibm_boto3
from ibm_botocore.client import Config as IBMConfig
from app.config import Config

# IBM COS client setup
cos_client = ibm_boto3.client(
    "s3",
    ibm_api_key_id=Config.IBM_API_KEY_ID,
    ibm_service_instance_id=Config.IBM_SERVICE_INSTANCE_ID,
    config=IBMConfig(signature_version="oauth"),
    endpoint_url=Config.IBM_ENDPOINT_URL
)
bucket_name = Config.COS_BUCKET_NAME

def upload_to_cos(file_name):
    """
    Uploads a file to IBM Cloud Object Storage (COS).

    Args:
        file_name (str): The local file path to upload.

    Returns:
        None
    """
    try:
        cos_client.upload_file(Filename=file_name, Bucket=bucket_name, Key=file_name)
        logging.info(f"File {file_name} uploaded to COS.")
    except Exception as e:
        logging.error(f"Error uploading {file_name} to COS: {str(e)}")