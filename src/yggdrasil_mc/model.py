import json
from base64 import b64decode
from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

from pydantic import model_validator, BaseModel, Field, root_validator


class YggdrasilPlayerUuidApiModel(BaseModel):
    id: str | None = None
    name: str | None = None
    existed: bool = True


def get_hash(cls, values):
    url = values.get("url")
    if url:
        parsed = urlparse(url)
        # get last path element
        values["hash"] = parsed.path.split("/")[-1]
    return values


class _SkinMetaData(BaseModel):
    model: Literal["default", "slim"] = "default"


class _Skin(BaseModel):
    url: str | None = None
    hash: str | None = None
    metadata: _SkinMetaData | None = _SkinMetaData(model="default")
    _get_hash = model_validator(mode="before")(get_hash)


class _Cape(BaseModel):
    url: str | None = None
    hash: str | None = None
    _get_hash = model_validator(mode="before")(get_hash)


class YggdrasilTexturesModel(BaseModel):
    skin: _Skin = Field(default=_Skin(), alias="SKIN")
    cape: _Cape = Field(default=_Cape(), alias="CAPE")


class YggdrasilPropertiesTexturesModel(BaseModel):
    timestamp: datetime
    profileId: str
    profileName: str
    textures: YggdrasilTexturesModel


class YggdrasilGameProfileApiModel(BaseModel):
    class Properties(BaseModel):
        textures: YggdrasilPropertiesTexturesModel

    id: str
    name: str
    properties: Properties  # a bit difference between API

    @model_validator(mode="before")
    @classmethod
    def pre_processer(cls, values):
        # Doc: https://wiki.vg/Mojang_API#UUID_-.3E_Profile_.2B_Skin.2FCape
        # base64 decode and a little change
        values["properties"][0]["textures"] = json.loads(
            b64decode(values["properties"][0]["value"])
        )
        # array is useless while mojang is interesting
        values["properties"] = values["properties"][0]
        return values
