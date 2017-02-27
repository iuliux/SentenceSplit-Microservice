from .settings import *


INSTALLED_APPS += [
    'storages',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sent_split',
        'USER': 'sent_split',
        'PASSWORD': 'iddqdidkfa',
        'HOST': 'sent-split-microservice.cfhmbfywn92g.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


AWS_ACCESS_KEY_ID = 'AKIAJJYNXM63VQWA7R5Q'

AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = 'zappa-a5q9128wh'
