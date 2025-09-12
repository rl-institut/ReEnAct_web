# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

from pathlib import Path

import environ

from django_mapengine import setup

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# reenact/
APPS_DIR = BASE_DIR / "reenact"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Europe/Berlin"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "de-de"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_cotton",
    "rest_framework",
]

LOCAL_APPS = [
    "reenact.reenact",
    "django_oemof",
    "django_mapengine",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_mapengine.middleware.MapEngineMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Hendrik Huyskens""", "hendrik.huyskens@rl-institut.de")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
CELERY_TASK_TIME_LIMIT = 10 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
CELERY_TASK_SOFT_TIME_LIMIT = 10 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "reenact.users.adapters.AccountAdapter"
# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "reenact.users.forms.UserSignupForm"}
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "reenact.users.adapters.SocialAccountAdapter"
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "reenact.users.forms.UserSocialSignupForm"}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# Your stuff...
# ------------------------------------------------------------------------------

MAP_ENGINE_CENTER_AT_STARTUP = [13.2, 54]
MAP_ENGINE_ZOOM_AT_STARTUP = 10.8
MAP_ENGINE_MAX_BOUNDS: [[-2.54, 46.35], [23.93, 55.87]]
MAP_ENGINE_LAYERS_AT_STARTUP = [
    "municipality",
    "municipalityline",
    "municipalitylabel",
]

MAP_ENGINE_API_MVTS = {
    "municipality": [
        setup.MVTAPI(
            "municipality",
            "reenact",
            "Municipality",
            style="region-fill",
            minzoom=8,
        ),
        setup.MVTAPI(
            "municipalityline",
            "reenact",
            "Municipality",
            style="region-line",
            minzoom=8,
        ),
        setup.MVTAPI(
            "municipalitylabel",
            "reenact",
            "Municipality",
            "label_tiles",
            style="region-label",
            minzoom=8,
        ),
    ],
    "static": [
        setup.MVTAPI("agricultural_area", "reenact", "AgriculturalArea"),
        setup.MVTAPI("bird_protection_area", "reenact", "BirdProtectionArea"),
        setup.MVTAPI("fauna_flora_habitat", "reenact", "FaunaFloraHabitatArea"),
        setup.MVTAPI("forest", "reenact", "Forest"),
        setup.MVTAPI("forest_protected", "reenact", "ForestProtected"),
        setup.MVTAPI("generator_biomass", "reenact", "GeneratorBiomass"),
        setup.MVTAPI("generator_pv_ground", "reenact", "GeneratorPvGround"),
        setup.MVTAPI("generator_pv_roof", "reenact", "GeneratorPvRoof"),
        setup.MVTAPI("generator_wind_15a", "reenact", "GeneratorWind15a"),
        setup.MVTAPI("generator_wind_25a", "reenact", "GeneratorWind25a"),
        setup.MVTAPI("generator_wind", "reenact", "GeneratorWind"),
        setup.MVTAPI("grassland", "reenact", "Grassland"),
        setup.MVTAPI("landscape_protection_area", "reenact", "LandscapeProtectionArea"),
        setup.MVTAPI("meadow", "reenact", "Meadow"),
        setup.MVTAPI("natural_parks", "reenact", "NaturalParks"),
        setup.MVTAPI("nature_conservation_area", "reenact", "NatureConservationArea"),
        setup.MVTAPI("organic_soils", "reenact", "OrganicSoils"),
        setup.MVTAPI(
            "potentialarea_paludiculture_Klasse_1",
            "reenact",
            "PotentialareaPaludicultureKlasse1",
        ),
        setup.MVTAPI(
            "potentialarea_paludiculture_Klasse_2",
            "reenact",
            "PotentialareaPaludicultureKlasse2",
        ),
        setup.MVTAPI(
            "potentialarea_paludiculture_Klasse_3",
            "reenact",
            "PotentialareaPaludicultureKlasse3",
        ),
        setup.MVTAPI(
            "potentialarea_paludiculture_Moor_ohne_Feldblock",
            "reenact",
            "PotentialareaPaludicultureMoorOhneFeldblock",
        ),
        setup.MVTAPI(
            "potentialarea_paludiculture_Nicht-Eignung",
            "reenact",
            "PotentialareaPaludicultureNichtEignung",
        ),
        setup.MVTAPI("potentialarea_pv_ground", "reenact", "PotentialareaPvGround"),
        setup.MVTAPI("potentialarea_pv_roof", "reenact", "PotentialareaPvRoof"),
        setup.MVTAPI("potentialarea_wind_1000m", "reenact", "PotentialareaWind1000m"),
        setup.MVTAPI("potentialarea_wind_400m", "reenact", "PotentialareaWind400m"),
        setup.MVTAPI("potentialarea_wind_600m", "reenact", "PotentialareaWind600m"),
        setup.MVTAPI("potentialarea_wind_800m", "reenact", "PotentialareaWind800m"),
        setup.MVTAPI(
            "potentialarea_wind_rpg_2024_draft",
            "reenact",
            "PotentialareaWindRpg2024Draft",
        ),
        setup.MVTAPI("power_grid", "reenact", "PowerGrid"),
        setup.MVTAPI("protected_landscape_parts", "reenact", "ProtectedLandscapeParts"),
        setup.MVTAPI("roof_generator_pv_roof", "reenact", "RoofGeneratorPvRoof"),
        setup.MVTAPI(
            "water_and_drinking_water_protection_area",
            "reenact",
            "WaterAndDrinkingWaterProtectionArea",
        ),
    ],
}

MAP_ENGINE_STYLES_FOLDER = "reenact/reenact/config/"

MAP_ENGINE_SOURCES = [
    setup.MapSource(
        name="mv_flurstuecke",
        type="raster",
        tiles=[
            "https://www.geodaten-mv.de/dienste/inspire_cp_alkis_view"
            "?bbox={bbox-epsg-3857}&format=image/png&service=WMS&version=1.3.0&request=GetMap&crs=EPSG:3857&"
            "styles=CP.CadastralParcel.Default&width=768&height=768&transparent=true&layers=CP.CadastralParcel",
        ],
    ),
]

MAP_ENGINE_LAYERS = [
    setup.MapLayer(
        id="cadastral_parcels",
        source="mv_flurstuecke",
        style={"type": "raster"},
        minzoom=14,
    ),
]
