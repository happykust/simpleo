#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023
#
# mypy: ignore-errors
# pylint: disable=no-self-argument

"""
Project configuration
"""
from typing import List, Optional, Union

import pyseto
# pylint: disable=no-name-in-module
from pydantic import AnyHttpUrl, HttpUrl, field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyseto import KeyInterface


class Settings(BaseSettings):
    """
    Settings class of app
    """
    API_V1_STR: str = "/api/v1"

    SECRET_ACCESS_KEY: str
    PUBLIC_ACCESS_KEY: str
    SECRET_REFRESH_KEY: str
    PUBLIC_REFRESH_KEY: str

    PRIVATE_SECRET_ACCESS_KEY: KeyInterface | None = None
    PRIVATE_PUBLIC_ACCESS_KEY: KeyInterface | None = None
    PRIVATE_SECRET_REFRESH_KEY: KeyInterface | None = None
    PRIVATE_PUBLIC_REFRESH_KEY: KeyInterface | None = None

    @field_validator("PRIVATE_SECRET_ACCESS_KEY", mode="before")  # noqa
    @classmethod
    def create_private_access_key(cls, _, values: FieldValidationInfo) -> KeyInterface:
        """
        Create private key for access keys
        :param _:
        :param values:
        :return:
        """
        return pyseto.Key.new(version=4, purpose="public", key=values.data.get("SECRET_ACCESS_KEY"))

    @field_validator("PRIVATE_PUBLIC_ACCESS_KEY", mode="before")  # noqa
    @classmethod
    def create_public_access_key(cls, _, values: FieldValidationInfo) -> KeyInterface:
        """
        Create public key for access keys
        :param _:
        :param values:
        :return:
        """
        return pyseto.Key.new(version=4, purpose="public", key=values.data.get("PUBLIC_ACCESS_KEY"))

    @field_validator("PRIVATE_SECRET_REFRESH_KEY", mode="before")  # noqa
    @classmethod
    def create_private_refresh_key(cls, _, values: FieldValidationInfo) -> KeyInterface:
        """
        Create private key for refresh keys
        :param _:
        :param values:
        :return:
        """
        return pyseto.Key.new(version=4, purpose="public", key=values.data.get("SECRET_REFRESH_KEY"))

    @field_validator("PRIVATE_PUBLIC_REFRESH_KEY", mode="before")  # noqa
    @classmethod
    def create_public_refresh_key(cls, _, values: FieldValidationInfo) -> KeyInterface:
        """
        Create public key for refresh keys
        :param _:
        :param values:
        :return:
        """
        return pyseto.Key.new(version=4, purpose="public", key=values.data.get("PUBLIC_REFRESH_KEY"))

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    TIMEZONE: str = "Europe/Moscow"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "https://2cac-193-41-142-236.ngrok-free.app"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")  # noqa
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Assemble CORS origins
        :param value:
        :return:
        """
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    PROJECT_NAME: str

    DB_HOST: str
    DB_USERNAME: str | None
    DB_PASSWORD: str | None
    DB_PORT: int = 5656
    DB_HTTP_URI: str | None = None
    DB_TLS_FILE_PATH: str

    @field_validator("DB_HTTP_URI", mode="before")  # noqa
    @classmethod
    def assemble_edgedb_connection(cls, value: Optional[str], values: FieldValidationInfo) -> str:
        """
        Assemble EdgeDB connection string
        :param value:
        :param values:
        :return:
        """
        if isinstance(value, str):
            return value
        return f"edgedb://{values.data.get('DB_USERNAME')}" \
               f":{values.data.get('DB_PASSWORD')}" \
               f"@{values.data.get('DB_HOST')}" \
               f":{values.data.get('DB_PORT')}"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_HTTP_URI: str | None = None

    @field_validator("REDIS_HTTP_URI", mode="before")  # noqa
    @classmethod
    def assemble_redis_connection(cls, value: Optional[str], values: FieldValidationInfo) -> str:
        """
        Assemble Redis connection string
        :param value:
        :param values:
        :return:
        """
        if isinstance(value, str):
            return value
        return f"redis://{values.data.get('REDIS_HOST')}" \
               f":{values.data.get('REDIS_PORT')}" \
               f"/{values.data.get('REDIS_DB')}"

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
