from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    refresh_token_expire_days = 30
    access_token_expire_minutes: int = 60


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    auth_jwt: AuthJWT = AuthJWT()

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}"
            f":{self.DB_PORT}/{self.DB_NAME}"
        )

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def test_database_url(self):
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}"
            f":{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file="/home/pavel/PycharmProjects/BusinessControlSystem_FastAPI /.env"
    )


settings = Settings()
