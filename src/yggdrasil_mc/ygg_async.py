import json
from base64 import b64decode

import aiohttp
from pydantic import root_validator

from . import model


class YggdrasilPlayerUuidApi(model.YggdrasilPlayerUuidApi):
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


class YggdrasilGameProfileApi(model.YggdrasilGameProfileApi):
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
