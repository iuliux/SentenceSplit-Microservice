from .settings import *


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
