DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'music_database',
        'USER': 'SimpleUser',
        'PASSWORD': '1524SU',
        'HOST': 'localhost',
        'PORT': '',
    }
}