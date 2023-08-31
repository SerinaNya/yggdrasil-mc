import httpx

from . import model


class YggdrasilPlayerUuidApi(model.YggdrasilPlayerUuidApiModel):
    @classmethod
    async def get(cls, api_root: str, player_name: str):
        async with httpx.AsyncClient(http2=True) as client:
            resp = await client.get(
                f"{api_root}/users/profiles/minecraft/{player_name}"
            )
        if resp.status_code in [204, 404]:  # No Content & Not Found
                return cls(existed=False)
        return cls.model_validate_json(resp.text)

    @classmethod
    async def getYggdrasilServer(cls, api_root: str, player_name: str):
        return await cls.get(f"{api_root}/api", player_name)

    @classmethod
    async def getMojangServer(cls, player_name: str):
        return await cls.get("https://api.mojang.com", player_name)


class YggdrasilGameProfileApi(model.YggdrasilGameProfileApiModel):
    @classmethod
    async def get(cls, api_root: str, player_uuid: str):
        async with httpx.AsyncClient(http2=True) as client:
            resp = await client.get(
                f"{api_root}/session/minecraft/profile/{player_uuid}"
            )
        return cls.model_validate_json(resp.text)

    @classmethod
    async def getYggdrasilServer(cls, api_root: str, player_uuid: str):
        return await cls.get(f"{api_root}/sessionserver", player_uuid)

    @classmethod
    async def getMojangServer(cls, player_uuid: str):
        return await cls.get("https://sessionserver.mojang.com", player_uuid)
