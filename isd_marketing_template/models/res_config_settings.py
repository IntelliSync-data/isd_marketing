# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Media Library Storage Configuration
    media_storage_method = fields.Selection([
        ('local', 'Local Server'),
        ('s3', 'AWS S3')
    ], string='Default Storage Method',
        config_parameter='isd_marketing_template.media_storage_method',
        default='local',
        help='Choose where to store uploaded media files')

    # AWS S3 Configuration
    media_s3_access_key = fields.Char(
        string='AWS Access Key ID',
        config_parameter='isd_marketing_template.media_s3_access_key',
        help='Your AWS Access Key ID'
    )

    media_s3_secret_key = fields.Char(
        string='AWS Secret Access Key',
        config_parameter='isd_marketing_template.media_s3_secret_key',
        help='Your AWS Secret Access Key'
    )

    media_s3_bucket = fields.Char(
        string='S3 Bucket Name',
        config_parameter='isd_marketing_template.media_s3_bucket',
        help='Name of your S3 bucket'
    )

    media_s3_region = fields.Selection([
        ('us-east-1', 'US East (N. Virginia)'),
        ('us-east-2', 'US East (Ohio)'),
        ('us-west-1', 'US West (N. California)'),
        ('us-west-2', 'US West (Oregon)'),
        ('ap-south-1', 'Asia Pacific (Mumbai)'),
        ('ap-northeast-1', 'Asia Pacific (Tokyo)'),
        ('ap-northeast-2', 'Asia Pacific (Seoul)'),
        ('ap-southeast-1', 'Asia Pacific (Singapore)'),
        ('ap-southeast-2', 'Asia Pacific (Sydney)'),
        ('eu-central-1', 'Europe (Frankfurt)'),
        ('eu-west-1', 'Europe (Ireland)'),
        ('eu-west-2', 'Europe (London)'),
        ('eu-west-3', 'Europe (Paris)'),
        ('sa-east-1', 'South America (São Paulo)'),
    ], string='AWS Region',
        config_parameter='isd_marketing_template.media_s3_region',
        default='us-east-1',
        help='AWS region where your bucket is located')

    media_s3_endpoint = fields.Char(
        string='Custom Endpoint URL',
        config_parameter='isd_marketing_template.media_s3_endpoint',
        help='Custom endpoint URL for S3-compatible services (MinIO, DigitalOcean Spaces, etc.)'
    )

    media_s3_use_ssl = fields.Boolean(
        string='Use SSL',
        config_parameter='isd_marketing_template.media_s3_use_ssl',
        default=True,
        help='Use HTTPS for S3 connections'
    )
