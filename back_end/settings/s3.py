import os
from base import USE_S3

try: 
    from local import USE_S3
except ImportError:
    pass

if USE_S3:
    AWS_STORAGE_BUCKET_NAME = 'nox-app'
    AWS_ACCESS_KEY_ID = 'AKIAIENZYKYEP57Y6T6Q'
    AWS_SECRET_ACCESS_KEY = '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'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL