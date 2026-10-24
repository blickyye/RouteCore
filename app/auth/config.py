from authx import AuthX, AuthXConfig

config = AuthXConfig()

config.JWT_SECRET_KEY = 'super-secret-key-that-is-at-least-32-bytes-long-for-security'
config.JWT_TOKEN_LOCATION = ['headers']

security = AuthX(config=config)