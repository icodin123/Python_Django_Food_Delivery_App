"""
File that contains settings of our project
"""

import os
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(5qpl&b-b48^jszl@nz02#lgbw%tp(o)_wb!)b&k(j9*kueh@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'farazkhosh.pythonanywhere.com']


##########
# EMAIL SETTINGS

EMAIL_HOST_USER = 'feedingcanadiankids.dev@gmail.com'
EMAIL_USE_TLS = True

EMAIL_HOST_PASSWORD = 'feeding123!'
DEFAULT_FROM_EMAIL = 'Feeding Canadian Kids Support'
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

##########
# Only for the purpose of testing
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
##########


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'profiles',
    'applications',
    'documents',
    'pairings'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'homepage.notification_middleware.NotificationsGetter',
    'homepage.settings_middleware.SettingsGetter'
]

ROOT_URLCONF = 'homepage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'homepage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'feeding_canadian_kids',
    #     'USER': 'django',
    #     'PASSWORD': 'djangoapp123!',
    #     'HOST': 'feeding-canadian-kids.czlvfzqrl00h.us-east-1.rds.amazonaws.com',
    #     'PORT': '3306',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_USER_MODEL = 'profiles.UserClass'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]

NOTIFICATION_THRESHOLD = 10

GOOGLE_API_KEY = "AIzaSyBDrmH6WKjD2uUgpJabFudN6oe8IJxpUJ4"
