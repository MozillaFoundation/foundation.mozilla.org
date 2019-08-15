"""
Django settings for networkapi project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import sys

import os
import environ
import logging.config
import dj_database_url
from django.utils.translation import gettext_lazy as _

app = environ.Path(__file__) - 1
root = app - 1

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    ASSET_DOMAIN=(str, ''),
    AWS_LOCATION=(str, ''),
    # old SQS information (x4)
    AWS_SQS_ACCESS_KEY_ID=(str, None),
    AWS_SQS_SECRET_ACCESS_KEY=(str, None),
    AWS_SQS_REGION=(str, None),
    PETITION_SQS_QUEUE_URL=(str, None),
    # new SQS information (x4)
    CRM_AWS_SQS_ACCESS_KEY_ID=(str, None),
    CRM_AWS_SQS_SECRET_ACCESS_KEY=(str, None),
    CRM_AWS_SQS_REGION=(str, None),
    CRM_PETITION_SQS_QUEUE_URL=(str, None),
    CONTENT_TYPE_NO_SNIFF=bool,
    CORS_REGEX_WHITELIST=(tuple, ()),
    CORS_WHITELIST=(tuple, ()),
    DATABASE_URL=(str, None),
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    DOMAIN_REDIRECT_MIDDLWARE_ENABLED=(bool, False),
    FILEBROWSER_DEBUG=(bool, False),
    FILEBROWSER_DIRECTORY=(str, ''),
    RANDOM_SEED=(int, None),
    HEROKU_APP_NAME=(str, ''),
    NETWORK_SITE_URL=(str, ''),
    PETITION_TEST_CAMPAIGN_ID=(str, ''),
    PULSE_API_DOMAIN=(str, ''),
    PULSE_DOMAIN=(str, ''),
    SET_HSTS=bool,
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, None),
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, None),
    SSL_REDIRECT=bool,
    DOMAIN_REDIRECT_MIDDLEWARE_ENABLED=(bool, False),
    MOZFEST_DOMAIN_REDIRECT_ENABLED=(bool, False),
    TARGET_DOMAINS=(list, []),
    USE_S3=(bool, True),
    USE_X_FORWARDED_HOST=(bool, False),
    XSS_PROTECTION=bool,
    REFERRER_HEADER_VALUE=(str, ''),
    GITHUB_TOKEN=(str, ''),
    SLACK_WEBHOOK_RA=(str, ''),
    BUYERS_GUIDE_VOTE_RATE_LIMIT=(str, '200/hour'),
    CORAL_TALK_SERVER_URL=(str, None),
    PNI_STATS_DB_URL=(str, None),
    CORAL_TALK_API_TOKEN=(str, None),
    REDIS_URL=(str, ''),
    USE_CLOUDINARY=(bool, False),
    CLOUDINARY_CLOUD_NAME=(str, ''),
    CLOUDINARY_API_KEY=(str, ''),
    CLOUDINARY_API_SECRET=(str, ''),
)

# Read in the environment
if os.path.exists(f'{root - 1}/.env') is True:
    environ.Env.read_env(f'{root - 1}/.env')
else:
    environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

APP_DIR = app()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FILEBROWSER_DEBUG = env('DEBUG')

# Force permanent redirects to the domains specified in TARGET_DOMAINS
DOMAIN_REDIRECT_MIDDLEWARE_ENABLED = env('DOMAIN_REDIRECT_MIDDLEWARE_ENABLED')
TARGET_DOMAINS = env('TARGET_DOMAINS')

# Temporary Redirect for Mozilla Festival domain
MOZFEST_DOMAIN_REDIRECT_ENABLED = env('MOZFEST_DOMAIN_REDIRECT_ENABLED')

if env('FILEBROWSER_DEBUG') or DEBUG != env('FILEBROWSER_DEBUG'):
    FILEBROWSER_DEBUG = env('FILEBROWSER_DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
ALLOWED_REDIRECT_HOSTS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')

HEROKU_APP_NAME = env('HEROKU_APP_NAME')

if HEROKU_APP_NAME:
    herokuAppHost = env('HEROKU_APP_NAME') + '.herokuapp.com'
    ALLOWED_HOSTS.append(herokuAppHost)

SITE_ID = 1

# Use social authentication if there are key/secret values defined
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_SIGNIN = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY is not None and \
                    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET is not None

USE_S3 = env('USE_S3')
USE_CLOUDINARY = env('USE_CLOUDINARY')

INSTALLED_APPS = list(filter(None, [

    'networkapi.filebrowser_s3' if USE_S3 else None,
    'social_django' if SOCIAL_SIGNIN else None,

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.sitemaps',

    'networkapi.wagtailcustomization',

    'wagtailmetadata',

    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.styleguide' if DEBUG else None,
    'wagtail.contrib.modeladmin',
    'experiments',
    'wagtailinventory',

    'modelcluster',
    'taggit',

    'whitenoise.runserver_nostatic',
    'rest_framework',
    'django_filters',
    'gunicorn',
    'corsheaders',
    'storages',
    'adminsortable',
    'cloudinary',

    # the network site
    'networkapi',
    'networkapi.campaign',
    'networkapi.news',
    'networkapi.people',
    'networkapi.utility',

    # possibly still used?
    'networkapi.highlights',
    'networkapi.milestones',

    # wagtail localisation app
    'networkapi.wagtail_l10n_customization',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',

    # wagtail-specific app prefixed so that it can be localised
    'networkapi.wagtailpages',
    'networkapi.buyersguide',
    'networkapi.mozfest',
]))

MIDDLEWARE = list(filter(None, [
    'networkapi.utility.middleware.TargetDomainRedirectMiddleware',

    'csp.middleware.CSPMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'networkapi.utility.middleware.ReferrerMiddleware',

    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # should be after SessionMiddleware and before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]))

if SOCIAL_SIGNIN:
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = env(
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL',
        None
    )

    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    ]

    # See https://python-social-auth.readthedocs.io/en/latest/pipeline.html
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

ROOT_URLCONF = 'networkapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            app('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': list(filter(None, [
                'social_django.context_processors.backends'
                if SOCIAL_SIGNIN else None,
                'social_django.context_processors.login_redirect'
                if SOCIAL_SIGNIN else None,
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'networkapi.context_processor.review_app',
                'networkapi.context_processor.cloudinary',
            ])),
            'libraries': {
                'localization': 'networkapi.wagtailpages.templatetags.localization',
                'settings_value': 'networkapi.utility.templatetags.settings_value',
                'mini_site_tags': 'networkapi.wagtailpages.templatetags.mini_site_tags',
                'homepage_tags': 'networkapi.wagtailpages.templatetags.homepage_tags',
                'card_tags': 'networkapi.wagtailpages.templatetags.card_tags',
                'primary_page_tags': 'networkapi.wagtailpages.templatetags.primary_page_tags',
                'multi_image_tags': 'networkapi.wagtailpages.templatetags.multi_image_tags',
                'nav_tags': 'networkapi.utility.templatetags.nav_tags',
                'bg_nav_tags': 'networkapi.buyersguide.templatetags.bg_nav_tags',
                'wagtailcustom_tags': 'networkapi.wagtailcustomization.templatetags.wagtailcustom_tags',
            }
        },
    },
]

if env('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                # timeout for read/write operations after a connection is established
                'SOCKET_TIMEOUT': 120,
                # timeout for the connection to be established
                'SOCKET_CONNECT_TIMEOUT': 30,
                # Enable compression
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                # Ignore exceptions, redis only used for caching (i.e. if redis fails, will use database)
                'IGNORE_EXCEPTIONS': True
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

# network asset domain used in templates
ASSET_DOMAIN = env('ASSET_DOMAIN')

WSGI_APPLICATION = 'networkapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = env('DATABASE_URL')

if DATABASE_URL is not None:
    DATABASES['default'].update(dj_database_url.config())

DATABASES['default']['ATOMIC_REQUESTS'] = True

RANDOM_SEED = env('RANDOM_SEED')

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('pt', _('Portuguese')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('pl', _('Polish')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


WHITENOISE_ROOT = app('frontend')
WHITENOISE_INDEX_FILE = True

STATIC_URL = '/static/'
STATIC_ROOT = root('staticfiles')
STATICFILES_STORAGE = 'networkapi.utility.staticfiles.NonStrictCompressedManifestStaticFilesStorage'

WAGTAIL_SITE_NAME = 'Mozilla Foundation'

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ]
}

# SQS information (if any) for google sheet petition data
AWS_SQS_ACCESS_KEY_ID = env('AWS_SQS_ACCESS_KEY_ID')
AWS_SQS_SECRET_ACCESS_KEY = env('AWS_SQS_SECRET_ACCESS_KEY')
AWS_SQS_REGION = env('AWS_SQS_REGION')
PETITION_SQS_QUEUE_URL = env('PETITION_SQS_QUEUE_URL')

# SQS information (if any) for CRM petition data
CRM_AWS_SQS_ACCESS_KEY_ID = env('CRM_AWS_SQS_ACCESS_KEY_ID')
CRM_AWS_SQS_SECRET_ACCESS_KEY = env('CRM_AWS_SQS_SECRET_ACCESS_KEY')
CRM_AWS_SQS_REGION = env('CRM_AWS_SQS_REGION')
CRM_PETITION_SQS_QUEUE_URL = env('CRM_PETITION_SQS_QUEUE_URL')

if USE_CLOUDINARY:
    CLOUDINARY_CLOUD_NAME = env('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = env('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = env('CLOUDINARY_API_SECRET')

    CLOUDINARY_URL = 'https://res.cloudinary.com/' + CLOUDINARY_CLOUD_NAME + '/image/upload/'

# Storage for user generated files
if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'networkapi.filebrowser_s3.storage.S3MediaStorage'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')
    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
    MEDIA_ROOT = ''
    # This is a workaround for https://github.com/wagtail/wagtail/issues/3206
    AWS_S3_FILE_OVERWRITE = False

    FILEBROWSER_DIRECTORY = env('FILEBROWSER_DIRECTORY')

else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

# CORS
CORS_ALLOW_CREDENTIALS = False

if '*' in env('CORS_WHITELIST'):
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = env('CORS_WHITELIST')
    CORS_ORIGIN_REGEX_WHITELIST = env('CORS_REGEX_WHITELIST')

# CSP
CSP_DEFAULT = (
    '\'self\''
)

CSP_DEFAULT_SRC = env('CSP_DEFAULT_SRC', default=CSP_DEFAULT)
CSP_SCRIPT_SRC = env('CSP_SCRIPT_SRC', default=CSP_DEFAULT)
CSP_IMG_SRC = env('CSP_IMG_SRC', default=CSP_DEFAULT)
CSP_OBJECT_SRC = env('CSP_OBJECT_SRC', default=None)
CSP_MEDIA_SRC = env('CSP_MEDIA_SRC', default=None)
CSP_FRAME_SRC = env('CSP_FRAME_SRC', default=None)
CSP_FONT_SRC = env('CSP_FONT_SRC', default=CSP_DEFAULT)
CSP_CONNECT_SRC = env('CSP_CONNECT_SRC', default=None)
CSP_STYLE_SRC = env('CSP_STYLE_SRC', default=CSP_DEFAULT)
CSP_BASE_URI = env('CSP_BASE_URI', default=None)
CSP_CHILD_SRC = env('CSP_CHILD_SRC', default=None)
CSP_FRAME_ANCESTORS = env('CSP_FRAME_ANCESTORS', default=None)
CSP_FORM_ACTION = env('CSP_FORM_ACTION', default=None)
CSP_SANDBOX = env('CSP_SANDBOX', default=None)
CSP_REPORT_URI = env('CSP_REPORT_URI', default=None)
CSP_WORKER_SRC = env('CSP_WORKER_SRC', default=CSP_DEFAULT)

# Security
SECURE_BROWSER_XSS_FILTER = env('XSS_PROTECTION')
SECURE_CONTENT_TYPE_NOSNIFF = env('CONTENT_TYPE_NO_SNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SET_HSTS')
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 31 * 6
SECURE_SSL_REDIRECT = env('SSL_REDIRECT')
# Heroku goes into an infinite redirect loop without this.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if env('SSL_REDIRECT') is True:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')
REFERRER_HEADER_VALUE = env('REFERRER_HEADER_VALUE')


# Remove the default Django loggers and configure new ones
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler'
        },
        'debug-error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler'
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        },
        'django.server': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['error'],
            'propagate': False,
            'level': 'ERROR'
        },
        'django.template': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'django.db.backends': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'django.utils.autoreload': {
            'handlers': ['debug-error'],
            'level': 'ERROR'
        },
        'networkapi': {
            'handlers': ['info'],
            'level': 'INFO',
        }
    }
}
DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')
logging.config.dictConfig(LOGGING)

# Frontend
FRONTEND = {
    'PULSE_API_DOMAIN': env('PULSE_API_DOMAIN'),
    'PULSE_DOMAIN': env('PULSE_DOMAIN'),
    'NETWORK_SITE_URL': env('NETWORK_SITE_URL'),
    'TARGET_DOMAINS': env('TARGET_DOMAINS'),
}

# Review apps' slack bot
GITHUB_TOKEN = env('GITHUB_TOKEN')
SLACK_WEBHOOK_RA = env('SLACK_WEBHOOK_RA')

# Used by load_fake_data to ensure we have petitions that actually work
PETITION_TEST_CAMPAIGN_ID = env('PETITION_TEST_CAMPAIGN_ID')

# Buyers Guide Rate Limit Setting
BUYERS_GUIDE_VOTE_RATE_LIMIT = env('BUYERS_GUIDE_VOTE_RATE_LIMIT')

# Detect if Django is running normally, or in test mode through "manage.py test"
TESTING = 'test' in sys.argv

# Coral Talk Server URL

CORAL_TALK_SERVER_URL = env('CORAL_TALK_SERVER_URL')

# privacynotincluded statistics DB
PNI_STATS_DB_URL = env('PNI_STATS_DB_URL')
CORAL_TALK_API_TOKEN = env('CORAL_TALK_API_TOKEN')

# Use network_url to check if we're running prod or not
NETWORK_SITE_URL = env('NETWORK_SITE_URL')
