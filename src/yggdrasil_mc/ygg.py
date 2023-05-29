import httpx

from . import model


class YggdrasilPlayerUuidApi(model.YggdrasilPlayerUuidApiModel):
    @classmethod
    def get(cls, api_root: str, player_name: str):
        resp = httpx.get(f"{api_root}/users/profiles/minecraft/{player_name}")
        if resp.status_code == 204:  # No content
            return cls(existed=False)
        return cls.parse_raw(resp.text)

    @classmethod
    def getYggdrasilServer(cls, api_root: str, player_name: str):
        return cls.get(f"{api_root}/api", player_name)

    @classmethod
    def getMojangServer(cls, player_name: str):
        return cls.get("https://api.mojang.com", player_name)


class YggdrasilGameProfileApi(model.YggdrasilGameProfileApiModel):
    @classmethod
    def get(cls, api_root: str, player_uuid: str):
        resp = httpx.get(f"{api_root}/session/minecraft/profile/{player_uuid}")
        return cls.parse_raw(resp.text)

    @classmethod
    def getYggdrasilServer(cls, api_root: str, player_uuid: str):
        return cls.get(f"{api_root}/sessionserver", player_uuid)

    @classmethod
    def getMojangServer(cls, player_uuid: str):
        return cls.get("https://sessionserver.mojang.com", player_uuid)
