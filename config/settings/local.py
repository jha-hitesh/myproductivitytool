from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "productivity",
        "USER": "productivityuser",
        "PASSWORD": "productivitypassword",
        "HOST": "postgresql",
        "PORT": "",
    }
}

DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
DROPBOX_OAUTH2_TOKEN = "FaI7rwoM11AAAAAAAAAAFLw0WpW1QSGOK2D3kP4bQ3dJbzEBCSuCM7CKjaS2c4xJ"

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
