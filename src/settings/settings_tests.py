import logging

ADMINS = ()

DEBUG = False
COMPRESS_ENABLED = False
STATICFILES_STORAGE = None
ALLOWED_HOSTS = ['*']

logging.disable(logging.CRITICAL)

EMAIL_BACKEND = 'django.core.mail.outbox'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
