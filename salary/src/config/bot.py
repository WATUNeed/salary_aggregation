from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BOT_')

    token: str

    skip_updates: bool = False
    debug: bool = True

    def get_bot_attributes(self) -> Dict[str, str]:
        return {
            'token': self.token
        }


BOT_CONFIG = BotConfig()
