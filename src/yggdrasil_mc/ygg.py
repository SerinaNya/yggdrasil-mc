import json
from base64 import b64decode

import requests
from pydantic import root_validator

from . import model


class YggdrasilPlayerUuidApi(model.YggdrasilPlayerUuidApi):
    @classmethod
    def get(cls, api_root: str, username: str):
        resp = requests.get(f"{api_root}/users/profiles/minecraft/{username}")
        if resp.status_code == 204:  # No content
            return cls(existed=False)
        return cls.parse_raw(resp.text)

    @classmethod
    def getBlessingSkinServer(cls, api_root: str, username: str):
        return cls.get(f"{api_root}/api", username)

    @classmethod
    def getMojangServer(cls, username: str):
        return cls.get("https://api.mojang.com", username)


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
    def get(cls, api_root: str, player_uuid: str):
        resp = requests.get(f"{api_root}/session/minecraft/profile/{player_uuid}")
        return cls.parse_raw(resp.text)

    @classmethod
    def getBlessingSkinServer(cls, api_root: str, player_uuid: str):
        return cls.get(f"{api_root}/sessionserver", player_uuid)

    @classmethod
    def getMojangServer(cls, player_uuid: str):
        return cls.get("https://sessionserver.mojang.com", player_uuid)
