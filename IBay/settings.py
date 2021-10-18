

import os
from pathlib import Path

from django.contrib import messages


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = os.path.join(BASE_DIR, 'media')


SECRET_KEY = 'django-insecure-fdn0y3@a#qz@-+6(k3dh%-yhv$(e5i=mri60v+k2k3p7(l(k+2'


DEBUG = True # need to convert false before depoloy

ALLOWED_HOSTS = []


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # need remover  before host. jst for 
    #developing purupse only





INSTALLED_APPS = [
  
    'adminlte3',
    
    'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'IBay',
    'Location',
    'Products',
    'Stores',
    'Marketing',
    'OrderApp',
    'UserApp',
    'rest_framework',
    'mptt',
    'crispy_forms',
    'widget_tweaks',
    # new appa for gmail 
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',    
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook', 
    #for google auth
    
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

ROOT_URLCONF = 'IBay.urls'

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
                'Stores.context_processors.categories',
                                
            ],
        },
    },
]



WSGI_APPLICATION = 'IBay.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=os.environ.get('EMAIL_USE_TLS')
EMAIL_PORT=os.environ.get('EMAIL_PORT')




MESSAGE_TAGS={
    messages.ERROR:'danger'
}




# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


MEDIA_URL = '/media/'

MEDIA_ROOT = MEDIA_DIR


SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        #'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v7.0',
    }
}




AUTH_USER_MODEL = 'UserApp.UserBase'



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_AUTO_FIELD ='django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
        
    'django.contrib.auth.backends.ModelBackend',    
    'allauth.account.auth_backends.AuthenticationBackend',
    #'social_core.backends.facebookOAuth2',
        
]


SOCIAL_AUTH_FACEBOOK_KEY = '831029154229131'
SOCIAL_AUTH_FACEBOOK_SECRET = 'bfe1de2c6e3ffad726b5eedefbc71d7e'

LOGIN_REDIRECT_URL = 'home'

ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_QUERY_EMAIL = True

ACCOUNT_SESSION_REMEMBER = True
