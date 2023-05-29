from . import ygg, ygg_async


class YggApiBase(object):
    api_root: str | None = None

    def __init__(self, api_root: str) -> None:
        self.api_root = api_root


class YggPlayerUuid(YggApiBase):
    getMojang = ygg.YggdrasilPlayerUuidApi.getMojangServer
    getMojangAsync = ygg_async.YggdrasilPlayerUuidApi.getMojangServer

    def get3rd(self, player_name: str):
        return ygg.YggdrasilPlayerUuidApi.getBlessingSkinServer(
            api_root=self.api_root, player_name=player_name
        )

    async def get3rdAsync(self, player_name: str):
        return await ygg_async.YggdrasilPlayerUuidApi.getBlessingSkinServer(
            api_root=self.api_root, player_name=player_name
        )


class YggPlayerProfile(YggApiBase):
    getMojang = ygg.YggdrasilGameProfileApi.getMojangServer
    getMojangAsync = ygg_async.YggdrasilGameProfileApi.getMojangServer

    def get3rd(self, player_uuid: str):
        return ygg.YggdrasilGameProfileApi.getBlessingSkinServer(
            api_root=self.api_root, player_uuid=player_uuid
        )

    async def get3rdAsync(self, player_uuid: str):
        return await ygg_async.YggdrasilGameProfileApi.getBlessingSkinServer(
            api_root=self.api_root, player_uuid=player_uuid
        )
