from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'authentication_backend',
    'cart',
    'order',
    'product',
    
    # allauth
    'django.contrib.sites',  # Required by allauth

    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers (e.g., Google, GitHub, Facebook)
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JamaKaporConfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #-------------Social Login-----------------
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

SOCIALACCOUNT_QUERY_EMAIL = True

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'JamaKaporConfig.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT", "5432"),
        'OPTIONS': {
            'sslmode': 'require',
            'channel_binding': 'require',
        }
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # For development
STATIC_ROOT = BASE_DIR / 'staticfiles'    # For collectstatic (in production)

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "site_title": "Jama Kapor Admin",
    "site_header": "Jama Kapor Dashboard",
    "site_brand": "JamaKapor",
    "site_logo": "logo.jpeg",  # optional path to logo
    "site_icon": "https://www.google.com/imgres?q=logo&imgurl=https%3A%2F%2Fthumbs.dreamstime.com%2Fb%2Fcreative-simple-dragons-silhouettes-logo-stylized-vector-illustrations-simple-dragons-silhouettes-logo-130475058.jpg&imgrefurl=https%3A%2F%2Fwww.dreamstime.com%2Fillustration%2Fsimple-logo.html&docid=EhJin307zIPANM&tbnid=yiV8FntXkJJc9M&vet=12ahUKEwjNi9vFw9WOAxUm7zgGHVCVMAgQM3oECBEQAA..i&w=800&h=800&hcb=2&ved=2ahUKEwjNi9vFw9WOAxUm7zgGHVCVMAgQM3oECBEQAA",
    "welcome_sign": "Welcome to Jama Kapor Admin",
    "copyright": "Jama Kapor",

    # "search_model": ["auth.User", "yourapp.YourModel"],

    "user_avatar": None,  # Or 'profile.image' if you have a custom profile


    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": ["auth", "yourapp", "anotherapp"],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        # "yourapp.YourModel": "fas fa-tshirt",
    },

    "changeform_format": "horizontal_tabs",  # or "collapsible" or "carousel"

    "related_modal_active": True,
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # Clean, soft contrast, easy on the eyes
    "dark_mode_theme": "solar",  # Optional dark mode fallback
    "navbar": "navbar-light bg-light",  # Light navbar
    "accent": "accent-info",  # Subtle blue accents
    "body_small_text": False,  # Default text size for readability
    "footer_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,  # Use default theme color
    "button_classes": {
        "primary": "btn btn-outline-primary",
        "secondary": "btn btn-outline-secondary"
    },
    "actions_sticky_top": True,  # Keep save buttons at top
}

# JAZZMIN_SETTINGS = {
#     "custom_links": {
#         "yourapp.YourModel": [{
#             "name": "Custom Action",
#             "url": "custom_view",
#             "icon": "fas fa-cogs",
#             "permissions": ["yourapp.change_yourmodel"]
#         }]
#     },
#     "model_icons": {
#         "yourapp.YourModel": "fas fa-box"
#     },
#     "app_icons": {
#         "yourapp": "fas fa-store"
#     }
# }
# "site_logo": "https://img.freepik.com/premium-vector/ecommerce-logo-design_624194-152.jpg?semt=ais_hybrid&w=740",  # Path relative to your STATICFILES_DIRS
