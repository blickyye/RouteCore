from authx import AuthX, AuthXConfig

config = AuthXConfig()

config.JWT_SECRET_KEY = 'secret_key'
config.JWT_TOKEN_LOCATION = ['headers']

security = AuthX(config=config)