from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    # mail_username: str = Field(..., env='MAIL_USERNAME')
    # mail_password: str = Field(..., env='MAIL_PASSWORD')
    # mail_from: str = Field(..., env='MAIL_FROM')
    # mail_port: str = Field(..., env='MAIL_PORT')
    # mail_server: str = Field(..., env='MAIL_SERVER')
    # mail_from_name: str = Field(..., env='MAIL_FROM_NAME')

settings = Settings()
