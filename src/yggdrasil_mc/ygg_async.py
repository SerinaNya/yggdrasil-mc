import json
from base64 import b64decode
from datetime import date
from typing import Literal

import aiohttp
from pydantic import BaseModel, root_validator


class YggdrasilPlayerUuidApi(BaseModel):
    id: str | None = None
    name: str | None = None
    existed: bool = True

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_root}/users/profiles/minecraft/{username}"
            ) as resp:
                if resp.status == 204:  # No content
                    return cls(existed=False)
                return cls.parse_raw(await resp.text())

    @classmethod
    async def getBlessingSkinServer(cls, api_root: str, username: str):
        return await cls.get(f"{api_root}/api", username)

    @classmethod
    async def getMojangServer(cls, username: str):
        return await cls.get("https://api.mojang.com", username)


def _make_hash(cls, values):
    url: str = values["url"]
    last_slash_location = url.rindex("/")
    real_hash = url[last_slash_location + 1 :]
    values["hash"] = real_hash
    return values


class YggdrasilTextures(BaseModel):
    class _Skin(BaseModel):
        class MetaData(BaseModel):
            model: Literal["default", "slim"] = "default"

        url: str | None = None
        hash: str | None = None
        metadata: MetaData | None = MetaData(model="default")
        _hash: str | None = None

        root_validator(pre=True, allow_reuse=True)(_make_hash)

    class _Cape(BaseModel):
        url: str | None = None
        hash: str | None = None
        _hash: str | None = None

        root_validator(pre=True, allow_reuse=True)(_make_hash)

    skin: _Skin | None = _Skin()
    cape: _Cape | None = _Cape()


class YggdrasilPropertiesTextures(BaseModel):
    timestamp: date
    profileId: str
    profileName: str
    textures: YggdrasilTextures


class YggdrasilGameProfileApi(BaseModel):
    class Properties(BaseModel):
        textures: YggdrasilPropertiesTextures

    id: str
    name: str
    properties: Properties  # a bit difference between API

    @root_validator(pre=True)
    def pre_processer(cls, values):
        # Doc: https://wiki.vg/Mojang_API#UUID_-.3E_Profile_.2B_Skin.2FCape
        # base64 decode and a little change
        values["properties"][0]["textures"] = json.loads(
            b64decode(values["properties"][0]["value"])
        )
        # array is useless while mojang is interesting
        values["properties"] = values["properties"][0]
        return values

    @classmethod
    async def get(cls, api_root: str, player_uuid: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_root}/session/minecraft/profile/{player_uuid}"
            ) as resp:
                return cls.parse_raw(await resp.text())

    @classmethod
    async def getBlessingSkinServer(cls, api_root: str, player_uuid: str):
        return await cls.get(f"{api_root}/sessionserver", player_uuid)

    @classmethod
    async def getMojangServer(cls, player_uuid: str):
        return await cls.get("https://sessionserver.mojang.com", player_uuid)
