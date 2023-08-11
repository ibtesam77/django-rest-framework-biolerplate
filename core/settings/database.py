from .environment import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DATABASE_NAME", default="postgres"),
        'USER': env("DATABASE_USER", default="postgres"),
        'PASSWORD': env("DATABASE_PASSWORD", default=""),
        'HOST': env("DATABASE_HOST", default="localhost"),
        'PORT': env("DATABASE_PORT", default="5432"),
    }
}
