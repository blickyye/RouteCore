from authx import AuthX, AuthXConfig

from app.config import settings

config = AuthXConfig()

config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_TOKEN_LOCATION = ['headers']

security = AuthX(config=config)