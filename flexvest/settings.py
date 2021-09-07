"""
Django settings for flexvest project.

Generated by 'django-admin startproject' using Django 2.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ssktzkcc4xvult8on$52)9w=rws%4o!g17zhqp1zspb%85^*a*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'account',
    'phonenumber_field',
    'django_countries',
    'cryptocurrency_payment.apps.CryptocurrencyPaymentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flexvest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'flexvest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# CRYPT SETTINGS
CRYPTOCURRENCY_PAYMENT = {
    "BITCOIN": {
        "CODE": "btc",
        "BACKEND": "merchant_wallet.backends.btc.BitcoinBackend",
        "FEE": 0.00,
        "REFRESH_PRICE_AFTER_MINUTE": 15,
        "REUSE_ADDRESS": False,
        "ACTIVE": True,
        "MASTER_PUBLIC_KEY": 'xpub6C8RUkUxnLAQtBqGPLAGtHLtUfXm2Qc1eosBpuiydkmj9bbFfEkhBtRjEq8QcxURYiBFDni5f1B4RpuvaVxnVMiRrwAntV1Um8PsxaRteGJ',
        "CANCEL_UNPAID_PAYMENT_HRS": 24,
        "CREATE_NEW_UNDERPAID_PAYMENT": True,
        "IGNORE_UNDERPAYMENT_AMOUNT": 10,
        "IGNORE_CONFIRMED_BALANCE_WITHOUT_SAVED_HASH_MINS": 20,
        "BALANCE_CONFIRMATION_NUM": 1,
        "ALLOW_ANONYMOUS_PAYMENT": True,
    }
 }






SITE_ID = 1
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# REDIRECTS
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


#HTTPS SETTINGS
# SECURE_HSTS_SECONDS = 31536000 # 1 YEAR
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE= True
# CSRF_COOKIE_SECURE = True
# Application definition