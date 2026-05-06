# -*- coding: utf-8 -*-
import logging
import uuid
from datetime import datetime

_logger = logging.getLogger(__name__)

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    _logger.warning("boto3 library not installed. S3 storage will not be available.")


class S3Service:
    """Service class for AWS S3 operations"""

    def __init__(self, access_key, secret_key, bucket, region, endpoint=None, use_ssl=True):
        """
        Initialize S3 service

        Args:
            access_key (str): AWS Access Key ID
            secret_key (str): AWS Secret Access Key
            bucket (str): S3 bucket name
            region (str): AWS region
            endpoint (str, optional): Custom endpoint URL for S3-compatible services
            use_ssl (bool): Use HTTPS
        """
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 library is required for S3 storage. Install it with: pip install boto3")

        self.bucket = bucket
        self.region = region
        self.use_ssl = use_ssl

        # Configure S3 client
        config_params = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'region_name': region,
        }

        if endpoint:
            config_params['endpoint_url'] = endpoint

        self.s3_client = boto3.client('s3', **config_params)
        self.s3_resource = boto3.resource('s3', **config_params)

    @classmethod
    def from_config(cls, env):
        """
        Create S3Service from Odoo configuration

        Args:
            env: Odoo environment

        Returns:
            S3Service: Configured S3 service instance
        """
        config = env['ir.config_parameter'].sudo()

        access_key = config.get_param('isd_marketing_template.media_s3_access_key')
        secret_key = config.get_param('isd_marketing_template.media_s3_secret_key')
        bucket = config.get_param('isd_marketing_template.media_s3_bucket')
        region = config.get_param('isd_marketing_template.media_s3_region', 'us-east-1')
        endpoint = config.get_param('isd_marketing_template.media_s3_endpoint')
        use_ssl = config.get_param('isd_marketing_template.media_s3_use_ssl', 'True') == 'True'

        if not all([access_key, secret_key, bucket]):
            raise ValueError("S3 configuration is incomplete. Please configure S3 settings.")

        return cls(access_key, secret_key, bucket, region, endpoint, use_ssl)

    def upload_file(self, file_content, filename, content_type='application/octet-stream'):
        """
        Upload file to S3

        Args:
            file_content (bytes): File content
            filename (str): Original filename
            content_type (str): MIME type

        Returns:
            tuple: (s3_key, public_url)
        """
        try:
            # Generate unique S3 key with timestamp and UUID to avoid conflicts
            timestamp = datetime.now().strftime('%Y/%m/%d')
            unique_id = uuid.uuid4().hex[:8]
            s3_key = f"media/{timestamp}/{unique_id}_{filename}"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                ACL='public-read'  # Make file publicly accessible
            )

            # Generate public URL
            public_url = self.generate_url(s3_key)

            _logger.info(f"Successfully uploaded {filename} to S3: {s3_key}")

            return s3_key, public_url

        except NoCredentialsError:
            _logger.error("AWS credentials not found or invalid")
            raise ValueError("AWS credentials not found or invalid")
        except ClientError as e:
            _logger.exception(f"Failed to upload file to S3: {e}")
            raise ValueError(f"Failed to upload file to S3: {str(e)}")

    def delete_file(self, s3_key):
        """
        Delete file from S3

        Args:
            s3_key (str): S3 object key

        Returns:
            bool: True if deleted successfully
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket,
                Key=s3_key
            )
            _logger.info(f"Successfully deleted {s3_key} from S3")
            return True
        except ClientError as e:
            _logger.warning(f"Failed to delete {s3_key} from S3: {e}")
            return False

    def generate_url(self, s3_key):
        """
        Generate public URL for S3 object

        Args:
            s3_key (str): S3 object key

        Returns:
            str: Public URL
        """
        # Get endpoint from client config
        endpoint = self.s3_client.meta.endpoint_url

        if endpoint and 'amazonaws.com' not in endpoint:
            # Custom endpoint (MinIO, DigitalOcean Spaces, etc.)
            return f"{endpoint}/{self.bucket}/{s3_key}"
        else:
            # Standard AWS S3 URL
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{s3_key}"

    def file_exists(self, s3_key):
        """
        Check if file exists in S3

        Args:
            s3_key (str): S3 object key

        Returns:
            bool: True if file exists
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket, Key=s3_key)
            return True
        except ClientError:
            return False

    def get_file_content(self, s3_key):
        """
        Download file content from S3

        Args:
            s3_key (str): S3 object key

        Returns:
            bytes: File content
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=s3_key)
            return response['Body'].read()
        except ClientError as e:
            _logger.exception(f"Failed to download file from S3: {e}")
            raise ValueError(f"Failed to download file from S3: {str(e)}")
