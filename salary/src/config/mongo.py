from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MONGO_')

    driver: str
    host: str
    port: int
    user: str
    password: str
    db: str

    def connection_string(self) -> str:
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/'


MONGO_CONFIG = MongoConfig()
