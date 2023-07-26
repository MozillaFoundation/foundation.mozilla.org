"""
Django settings for networkapi project.

Gnerated by 'django-admin startproject' using Django 1.10.3.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import logging.config
import os
import sys
from typing import Dict, Literal

import dj_database_url
import environ
from django.utils.translation import gettext_lazy
from wagtail.embeds.oembed_providers import youtube

app = environ.Path(__file__) - 1
root = app - 1

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    APP_ENVIRONMENT=(str, ""),
    APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION=(str, ""),
    APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST=(str, ""),
    ASSET_DOMAIN=(str, ""),
    AWS_LOCATION=(str, ""),
    BASKET_URL=(str, ""),
    BUYERS_GUIDE_VOTE_RATE_LIMIT=(str, "200/hour"),
    CONTENT_TYPE_NO_SNIFF=bool,
    CORS_ALLOWED_ORIGIN_REGEXES=(tuple, ()),
    CORS_ALLOWED_ORIGINS=(tuple, ()),
    CSP_INCLUDE_NONCE_IN=(list, []),
    DATA_UPLOAD_MAX_NUMBER_FIELDS=(int, 2500),
    DATABASE_URL=(str, None),
    DEBUG=(bool, False),
    DEBUG_TOOLBAR_ENABLED=(bool, False),
    DJANGO_LOG_LEVEL=(str, "INFO"),
    FEED_CACHE_TIMEOUT=(int, 60 * 60 * 24),
    DOMAIN_REDIRECT_MIDDLEWARE_ENABLED=(bool, False),
    FEED_LIMIT=(int, 10),
    FILEBROWSER_DEBUG=(bool, False),
    FILEBROWSER_DIRECTORY=(str, ""),
    FORCE_500_STACK_TRACES=(bool, False),
    FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN=(str, ""),
    FRONTEND_CACHE_CLOUDFLARE_ZONEID=(str, ""),
    GITHUB_TOKEN=(str, ""),
    HEROKU_APP_NAME=(str, ""),
    HEROKU_BRANCH=(str, ""),
    HEROKU_PR_NUMBER=(str, ""),
    HEROKU_RELEASE_VERSION=(str, None),
    INDEX_PAGE_CACHE_TIMEOUT=(int, 60 * 60 * 24),
    MOZFEST_DOMAIN_REDIRECT_ENABLED=(bool, False),
    NETWORK_SITE_URL=(str, ""),
    PETITION_TEST_CAMPAIGN_ID=(str, ""),
    PNI_STATS_DB_URL=(str, None),
    PULSE_API_DOMAIN=(str, ""),
    PULSE_DOMAIN=(str, ""),
    RANDOM_SEED=(int, None),
    REDIS_URL=(str, ""),
    REFERRER_HEADER_VALUE=(str, ""),
    REVIEW_APP=(bool, False),
    SENTRY_DSN=(str, None),
    SENTRY_ENVIRONMENT=(str, None),
    SET_HSTS=bool,
    SLACK_WEBHOOK_RA=(str, ""),
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, None),
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, None),
    SSL_REDIRECT=bool,
    STATIC_HOST=(str, ""),
    TARGET_DOMAINS=(list, []),
    USE_COMMENTO=(bool, False),
    USE_S3=(bool, True),
    USE_X_FORWARDED_HOST=(bool, False),
    WAGTAILIMAGES_INDEX_PAGE_SIZE=(int, 60),
    WAGTAILLOCALIZE_GIT_URL=(str, ""),
    WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH=(str, ""),
    WAGTAILLOCALIZE_GIT_CLONE_DIR=(str, ""),
    WAGTAIL_LOCALIZE_PRIVATE_KEY=(str, ""),
    WEB_MONETIZATION_POINTER=(str, ""),
    XROBOTSTAG_ENABLED=(bool, False),
    XSS_PROTECTION=bool,
    SCOUT_KEY=(str, ""),
    WAGTAILADMIN_BASE_URL=(str, ""),
)

# Read in the environment
if os.path.exists(f"{root - 1}/.env") is True:
    environ.Env.read_env(f"{root - 1}/.env")
else:
    environ.Env.read_env()

SENTRY_DSN = env("SENTRY_DSN")
HEROKU_RELEASE_VERSION = env("HEROKU_RELEASE_VERSION")
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT")

# This is used by Wagtail's email notifications for constructing absolute
# URLs. It should be set to the domain that users will access the admin site.
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(  # type: ignore
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        release=HEROKU_RELEASE_VERSION,
        environment=SENTRY_ENVIRONMENT,
        ignore_errors=[
            # Ignore security scan spam
            "DisallowedHost",
            # Ignore failing gunicorn threads
            "SystemExit",
        ],
    )

# At True when running on a review app
REVIEW_APP = env("REVIEW_APP", default=False)

APP_ENVIRONMENT = env("APP_ENVIRONMENT")

# Apple Pay domain association
APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION = env("APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION")
APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST = env("APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

# Basket client configuration
BASKET_URL = env("BASKET_URL")

APP_DIR = app()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FILEBROWSER_DEBUG = env("DEBUG")
DEBUG_TOOLBAR_ENABLED = env("DEBUG_TOOLBAR_ENABLED")

# SECURITY WARNING: same as above!
FORCE_500_STACK_TRACES = env("FORCE_500_STACK_TRACES")

# whether or not to send the X-Robots-Tag header
XROBOTSTAG_ENABLED = env("XROBOTSTAG_ENABLED")

# Force permanent redirects to the domains specified in TARGET_DOMAINS
DOMAIN_REDIRECT_MIDDLEWARE_ENABLED = env("DOMAIN_REDIRECT_MIDDLEWARE_ENABLED")
TARGET_DOMAINS = env("TARGET_DOMAINS")

# Temporary Redirect for Mozilla Festival domain
MOZFEST_DOMAIN_REDIRECT_ENABLED = env("MOZFEST_DOMAIN_REDIRECT_ENABLED")

if env("FILEBROWSER_DEBUG") or DEBUG != env("FILEBROWSER_DEBUG"):
    FILEBROWSER_DEBUG = env("FILEBROWSER_DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
ALLOWED_REDIRECT_HOSTS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")

HEROKU_APP_NAME = env("HEROKU_APP_NAME")
HEROKU_PR_NUMBER = env("HEROKU_PR_NUMBER")
HEROKU_BRANCH = env("HEROKU_BRANCH")

if HEROKU_APP_NAME:
    herokuAppHost = env("HEROKU_APP_NAME") + ".herokuapp.com"
    ALLOWED_HOSTS.append(herokuAppHost)

SITE_ID = 1

# Use social authentication if there are key/secret values defined
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_SIGNIN = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY is not None and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET is not None

USE_S3 = env("USE_S3")

# Detect if Django is running normally, or in test mode through "manage.py test"
TESTING = "test" in sys.argv or "pytest" in sys.argv

INSTALLED_APPS = list(
    filter(
        None,
        [
            "scout_apm.django",
            "whitenoise.runserver_nostatic",
            "networkapi.filebrowser_s3" if USE_S3 else None,
            "social_django" if SOCIAL_SIGNIN else None,
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django.contrib.redirects",
            "django.contrib.sitemaps",
            "django.contrib.humanize",
            "networkapi.wagtailcustomization",
            "wagtailmetadata",
            "wagtail.embeds",
            "wagtail.sites",
            "wagtail.users",
            "wagtail.snippets",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.search",
            "wagtail.admin",
            "wagtail.contrib.legacy.richtext",
            "wagtail",
            "wagtail.contrib.forms",
            "wagtail.contrib.redirects",
            "wagtail.contrib.routable_page",
            "wagtail.contrib.styleguide" if DEBUG else None,
            "wagtail.contrib.table_block",
            "wagtail.contrib.modeladmin",
            "wagtail.contrib.frontend_cache",
            "wagtail.contrib.settings",
            "wagtail_color_panel",
            "wagtailmedia",
            "wagtailinventory",
            "wagtail_footnotes",
            "modelcluster",
            "taggit",
            # Base wagtail localization
            "wagtail_localize",
            "wagtail_localize.locales",
            # git integration for localization
            "wagtail_localize_git",
            # other third party
            "rest_framework",
            "django_filters",
            "django_htmx",
            "debug_toolbar" if DEBUG_TOOLBAR_ENABLED else None,
            "gunicorn",
            "corsheaders",
            "storages",
            "adminsortable",
            "querystring_tag",
            # the network site
            "networkapi",
            "networkapi.campaign",
            "networkapi.events",
            "networkapi.news",
            "networkapi.people",
            "networkapi.utility",
            # possibly still used?
            "networkapi.highlights",
            # wagtail-specific app prefixed so that it can be localised
            "networkapi.wagtailpages",
            "networkapi.mozfest",
            "networkapi.donate",
            "pattern_library" if PATTERN_LIBRARY_ENABLED else None,
            "networkapi.project_styleguide" if PATTERN_LIBRARY_ENABLED else None,
        ],
    )
)

MIDDLEWARE = list(
    filter(
        None,
        [
            "csp.middleware.CSPMiddleware",
            "corsheaders.middleware.CorsMiddleware",
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            "networkapi.utility.middleware.ReferrerMiddleware",
            "networkapi.utility.middleware.XRobotsTagMiddleware" if XROBOTSTAG_ENABLED else None,
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.middleware.gzip.GZipMiddleware",
            "debug_toolbar.middleware.DebugToolbarMiddleware" if DEBUG_TOOLBAR_ENABLED else None,
            "networkapi.utility.middleware.TargetDomainRedirectMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            #
            # should be after SessionMiddleware and before CommonMiddleware
            "django.middleware.locale.LocaleMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            #
            # instead of 'wagtail.contrib.redirects.middleware.RedirectMiddleware':
            "networkapi.wagtailcustomization.redirects.middleware.RedirectMiddleware",
            #
            # instead of 'django.middleware.csrf.CsrfViewMiddleware':
            "networkapi.wagtailcustomization.csrf.middleware.CustomCsrfViewMiddleware",
            #
            "django_htmx.middleware.HtmxMiddleware",
        ],
    )
)

if SOCIAL_SIGNIN:
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = env("SOCIAL_AUTH_LOGIN_REDIRECT_URL", None)

    AUTHENTICATION_BACKENDS = [
        "social_core.backends.google.GoogleOAuth2",
        "django.contrib.auth.backends.ModelBackend",
    ]

    # See https://python-social-auth.readthedocs.io/en/latest/pipeline.html
    SOCIAL_AUTH_PIPELINE = (
        "social_core.pipeline.social_auth.social_details",
        "social_core.pipeline.social_auth.social_uid",
        "social_core.pipeline.social_auth.auth_allowed",
        "social_core.pipeline.social_auth.social_user",
        "social_core.pipeline.user.get_username",
        "social_core.pipeline.user.create_user",
        "social_core.pipeline.social_auth.associate_user",
        "social_core.pipeline.social_auth.load_extra_data",
        "social_core.pipeline.user.user_details",
    )

ROOT_URLCONF = "networkapi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            app("templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": list(
                filter(
                    None,
                    [
                        "social_django.context_processors.backends" if SOCIAL_SIGNIN else None,
                        "social_django.context_processors.login_redirect" if SOCIAL_SIGNIN else None,
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.template.context_processors.static",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                        "networkapi.context_processor.review_app",
                        "networkapi.context_processor.canonical_path",
                        "networkapi.context_processor.canonical_site_url",
                        "wagtail.contrib.settings.context_processors.settings",
                    ],
                )
            ),
            "libraries": {
                "bg_nav_tags": "networkapi.wagtailpages.templatetags.bg_nav_tags",
                "blog_tags": "networkapi.wagtailpages.templatetags.blog_tags",
                "card_tags": "networkapi.wagtailpages.templatetags.card_tags",
                "class_tags": "networkapi.wagtailpages.templatetags.class_tags",
                "debug_tags": "networkapi.wagtailpages.templatetags.debug_tags",
                "formassembly_helper": "networkapi.utility.templatetags.formassembly_helper",
                "mofo_common": "networkapi.utility.templatetags.mofo_common",
                "homepage_tags": "networkapi.wagtailpages.templatetags.homepage_tags",
                "localization": "networkapi.wagtailpages.templatetags.localization",
                "mini_site_tags": "networkapi.wagtailpages.templatetags.mini_site_tags",
                "custom_image_tags": "networkapi.wagtailpages.templatetags.custom_image_tags",
                "nav_tags": "networkapi.utility.templatetags.nav_tags",
                "primary_page_tags": "networkapi.wagtailpages.templatetags.primary_page_tags",
                "settings_value": "networkapi.utility.templatetags.settings_value",
                "wagtailcustom_tags": "networkapi.wagtailcustomization.templatetags.wagtailcustom_tags",
            },
        },
    },
]

if env("REDIS_URL"):
    connection_pool_kwargs: Dict[str, Literal[None]] = {}

    if env("REDIS_URL").startswith("rediss"):
        connection_pool_kwargs["ssl_cert_reqs"] = None

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # timeout for read/write operations after a connection is established
                "SOCKET_TIMEOUT": 120,
                # timeout for the connection to be established
                "SOCKET_CONNECT_TIMEOUT": 30,
                # Enable compression
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                # Ignore exceptions, redis only used for caching (i.e. if redis fails, will use database)
                "IGNORE_EXCEPTIONS": True,
                "CONNECTION_POOL_KWARGS": connection_pool_kwargs,
            },
        }
    }
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

# network asset domain used in templates
ASSET_DOMAIN = env("ASSET_DOMAIN")

WSGI_APPLICATION = "networkapi.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

DATABASE_URL = env("DATABASE_URL")

if DATABASE_URL is not None:
    DATABASES["default"].update(dj_database_url.config())

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # type: ignore

RANDOM_SEED = env("RANDOM_SEED")

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth" ".password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth" ".password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth" ".password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth" ".password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en"
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = (
    ("en", gettext_lazy("English")),
    ("de", gettext_lazy("German")),
    ("es", gettext_lazy("Spanish")),
    ("fr", gettext_lazy("French")),
    ("fy-NL", gettext_lazy("Frisian")),
    ("nl", gettext_lazy("Dutch")),
    ("pl", gettext_lazy("Polish")),
    ("pt-BR", gettext_lazy("Portuguese (Brazil)")),
    ("sw", gettext_lazy("Swahili")),
)

WAGTAILLOCALIZE_GIT_URL = env("WAGTAILLOCALIZE_GIT_URL")
WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH = env("WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH")
WAGTAILLOCALIZE_GIT_CLONE_DIR = env("WAGTAILLOCALIZE_GIT_CLONE_DIR")
WAGTAIL_LOCALIZE_PRIVATE_KEY = env("WAGTAIL_LOCALIZE_PRIVATE_KEY")

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
    os.path.join(BASE_DIR, "networkapi/templates/pages/buyersguide/about/locale"),
    os.path.join(BASE_DIR, "networkapi/wagtailpages/templates/wagtailpages/pages/locale"),
    os.path.join(
        BASE_DIR,
        "networkapi/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2021/locale",
    ),
    os.path.join(
        BASE_DIR,
        "networkapi/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2022/locale",
    ),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


WHITENOISE_INDEX_FILE = True

# Enable CloudFront for staticfiles
STATIC_HOST = env("STATIC_HOST") if not DEBUG and not REVIEW_APP else ""

STATIC_URL = STATIC_HOST + "/static/"
STATIC_ROOT = root("staticfiles")
STATICFILES_DIRS = [app("frontend")]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WAGTAIL_SITE_NAME = "Mozilla Foundation"
WAGTAIL_SLIM_SIDEBAR = False
WAGTAILIMAGES_INDEX_PAGE_SIZE = env("WAGTAILIMAGES_INDEX_PAGE_SIZE")
WAGTAIL_USAGE_COUNT_ENABLED = True
WAGTAIL_I18N_ENABLED = True

# Wagtail Frontend Cache Invalidator Settings

if env("FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"):
    WAGTAILFRONTENDCACHE = {
        "cloudflare": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "BEARER_TOKEN": env("FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"),
            "ZONEID": env("FRONTEND_CACHE_CLOUDFLARE_ZONEID"),
        }
    }


# Wagtail Embeds

DATAWRAPPER_PROVIDER = {
    "endpoint": "https://api.datawrapper.de/v3/oembed",
    "urls": [
        r"^https:\/\/datawrapper\.dwcdn\.net\/(?:[\d\w]{5}\/){1}(?:[\d]+\/)?$",
    ],
}

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
        "providers": [youtube, DATAWRAPPER_PROVIDER],
    }
]

# Wagtail search

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ]
}

# Storage for user generated files
if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = "networkapi.filebrowser_s3.storage.S3MediaStorage"
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
    AWS_LOCATION = env("AWS_LOCATION")
    MEDIA_URL = "https://" + AWS_S3_CUSTOM_DOMAIN + "/"
    MEDIA_ROOT = ""
    # This is a workaround for https://github.com/wagtail/wagtail/issues/3206
    AWS_S3_FILE_OVERWRITE = False

    FILEBROWSER_DIRECTORY = env("FILEBROWSER_DIRECTORY")

else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root("media/")
    MEDIA_URL = "/media/"

# CORS
CORS_ALLOW_CREDENTIALS = False

if "*" in env("CORS_ALLOWED_ORIGINS"):
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
    CORS_ALLOWED_ORIGIN_REGEXES = env("CORS_ALLOWED_ORIGIN_REGEXES")

# CSP
CSP_DEFAULT = "'self'"

CSP_DEFAULT_SRC = env("CSP_DEFAULT_SRC", default=CSP_DEFAULT)
CSP_SCRIPT_SRC = env("CSP_SCRIPT_SRC", default=CSP_DEFAULT)
CSP_IMG_SRC = env("CSP_IMG_SRC", default=CSP_DEFAULT)
CSP_OBJECT_SRC = env("CSP_OBJECT_SRC", default=None)
CSP_MEDIA_SRC = env("CSP_MEDIA_SRC", default=None)
CSP_FRAME_SRC = env("CSP_FRAME_SRC", default=None)
CSP_FONT_SRC = env("CSP_FONT_SRC", default=CSP_DEFAULT)
CSP_CONNECT_SRC = env("CSP_CONNECT_SRC", default=None)
CSP_STYLE_SRC = env("CSP_STYLE_SRC", default=CSP_DEFAULT)
CSP_BASE_URI = env("CSP_BASE_URI", default=None)
CSP_CHILD_SRC = env("CSP_CHILD_SRC", default=None)
CSP_FRAME_ANCESTORS = env("CSP_FRAME_ANCESTORS", default=None)
CSP_FORM_ACTION = env("CSP_FORM_ACTION", default=None)
CSP_SANDBOX = env("CSP_SANDBOX", default=None)
CSP_REPORT_URI = env("CSP_REPORT_URI", default=None)
CSP_WORKER_SRC = env("CSP_WORKER_SRC", default=CSP_DEFAULT)
CSP_INCLUDE_NONCE_IN = env("CSP_INCLUDE_NONCE_IN", default=[])

# Security
SECURE_BROWSER_XSS_FILTER = env("XSS_PROTECTION")
SECURE_CONTENT_TYPE_NOSNIFF = env("CONTENT_TYPE_NO_SNIFF")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SET_HSTS")
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 31 * 6
SECURE_SSL_REDIRECT = env("SSL_REDIRECT")
# Heroku goes into an infinite redirect loop without this.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if env("SSL_REDIRECT") is True:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

X_FRAME_OPTIONS = env("X_FRAME_OPTIONS")
REFERRER_HEADER_VALUE = env("REFERRER_HEADER_VALUE")


# Remove the default Django loggers and configure new ones
LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "formatters": {"verbose": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},
    "handlers": {
        "debug": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "verbose",
        },
        "error": {"level": "ERROR", "class": "logging.StreamHandler"},
        "debug-error": {
            "level": "ERROR",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "info": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["debug"], "level": "DEBUG"},
        "django.server": {
            "handlers": ["debug"],
            "level": "DEBUG",
        },
        "django.request": {"handlers": ["error"], "propagate": False, "level": "ERROR"},
        "django.template": {"handlers": ["debug-error"], "level": "ERROR"},
        "django.db.backends": {"handlers": ["debug-error"], "level": "ERROR"},
        "django.utils.autoreload": {"handlers": ["debug-error"], "level": "ERROR"},
        "networkapi": {
            "handlers": ["info"],
            "level": "INFO",
        },
    },
}
DJANGO_LOG_LEVEL = env("DJANGO_LOG_LEVEL")
logging.config.dictConfig(LOGGING)

# Frontend
FRONTEND = {
    "PULSE_API_DOMAIN": env("PULSE_API_DOMAIN"),
    "PULSE_DOMAIN": env("PULSE_DOMAIN"),
    "NETWORK_SITE_URL": env("NETWORK_SITE_URL"),
    "TARGET_DOMAINS": env("TARGET_DOMAINS"),
    "SENTRY_DSN": env("SENTRY_DSN"),
    "RELEASE_VERSION": env("HEROKU_RELEASE_VERSION"),
    "SENTRY_ENVIRONMENT": env("SENTRY_ENVIRONMENT"),
}

# Review apps' slack bot
GITHUB_TOKEN = env("GITHUB_TOKEN")
SLACK_WEBHOOK_RA = env("SLACK_WEBHOOK_RA")

# Used by load_fake_data to ensure we have petitions that actually work
PETITION_TEST_CAMPAIGN_ID = env("PETITION_TEST_CAMPAIGN_ID")

# Buyers Guide Rate Limit Setting
BUYERS_GUIDE_VOTE_RATE_LIMIT = env("BUYERS_GUIDE_VOTE_RATE_LIMIT")

# Commento.io flag
USE_COMMENTO = env("USE_COMMENTO")

# privacynotincluded statistics DB
PNI_STATS_DB_URL = env("PNI_STATS_DB_URL")

# Use network_url to check if we're running prod or not
NETWORK_SITE_URL = env("NETWORK_SITE_URL")

# Blog/Campaign index cache setting
INDEX_PAGE_CACHE_TIMEOUT = env("INDEX_PAGE_CACHE_TIMEOUT")

# RSS / ATOM settings
FEED_CACHE_TIMEOUT = env("FEED_CACHE_TIMEOUT")
FEED_LIMIT = env("FEED_LIMIT")

# Support pages with a large number of fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = env("DATA_UPLOAD_MAX_NUMBER_FIELDS")

# Web Monetization: https://webmonetization.org/
WEB_MONETIZATION_POINTER = env("WEB_MONETIZATION_POINTER")

if env("SCOUT_KEY"):
    SCOUT_MONITOR = True
    SCOUT_KEY = env("SCOUT_KEY")
    SCOUT_NAME = env("SCOUT_NAME", default="foundation")


TAGGIT_CASE_INSENSITIVE = False

REVIEW_APP_HEROKU_API_KEY = env("REVIEW_APP_HEROKU_API_KEY", default=None)
REVIEW_APP_CLOUDFLARE_ZONE_ID = env("REVIEW_APP_CLOUDFLARE_ZONE_ID", default=None)
REVIEW_APP_CLOUDFLARE_TOKEN = env("REVIEW_APP_CLOUDFLARE_TOKEN", default=None)
REVIEW_APP_DOMAIN = env("REVIEW_APP_DOMAIN", default=None)

# Make sure the docker internal IP is a known internal IP, so that "debug" in templates works
if DEBUG:
    import os  # only if you haven't already imported this
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
