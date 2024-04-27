from base64 import b64decode
from uuid import UUID

import httpx

from yggdrasil_mc.exceptions import PlayerNotFoundError
from yggdrasil_mc.models import PlayerProfile, PlayerUuid
from yggdrasil_mc.utils import urlstrjoin


class YggdrasilMC:
    api_root: str | None

    def __init__(self, api_root: str | None = None):
        """
        Initialize YggdrasilMC.

        Parameters:
            `api_root` (`str | None`): The root URL of the API. If None, Mojang server will be used.

        Returns:
            None
        """
        self.api_root = api_root

    async def by_uuid_async(
        self, player_uuid: str | PlayerUuid | UUID
    ) -> PlayerProfile:
        """
        Get a player's profile by their UUID. (async)

        Args:
            `player_uuid: str | PlayerUuid | UUID` => The UUID / `PlayerUuid` of the player.

        Returns:
            `PlayerProfile`: The player's profile.

        Raises:
            PlayerNotFoundError: If the player is not found.
            httpx.HTTPStatusError or ValueError: If an unexpected http status error occurs.
        """

        # Convert player_uuid to string
        if isinstance(player_uuid, UUID):
            _player_uuid = player_uuid.hex
        elif isinstance(player_uuid, PlayerUuid):
            _player_uuid = player_uuid.id
        else:
            _player_uuid = player_uuid

        async with httpx.AsyncClient(
            http2=True,
            base_url=urlstrjoin(self.api_root, "sessionserver")
            if self.api_root
            else "https://sessionserver.mojang.com",
        ) as client:
            response = await client.get(f"/session/minecraft/profile/{_player_uuid}")

        match response.status_code:
            case httpx.codes.OK:  # 200
                return PlayerProfile.model_validate_json(
                    b64decode(response.json().get("properties")[0].get("value"))
                )
            case httpx.codes.NO_CONTENT:  # 204
                raise PlayerNotFoundError(
                    f"Server has responded 204 No Content, {_player_uuid=}"
                )
            case httpx.codes.BAD_REQUEST:  # 400
                raise PlayerNotFoundError(response.text)
            case _:
                response.raise_for_status()
                raise ValueError(f"Unexpected HTTP status code: {response.status_code}")

    async def by_name_async(self, player_name: str) -> PlayerProfile:
        """
        Get a player's profile by their name. (async)

        Args:
            player_name (str): The name of the player to retrieve the profile for.

        Returns:
            PlayerProfile: The player's profile.

        Raises:
            PlayerNotFoundError: If the player is not found.
            httpx.HTTPStatusError or ValueError: If an unexpected http status error occurs.
        """

        async with httpx.AsyncClient(
            http2=True,
            base_url=urlstrjoin(self.api_root, "api")
            if self.api_root
            else "https://api.mojang.com",
        ) as client:
            response = await client.get(f"/users/profiles/minecraft/{player_name}")

        match response.status_code:
            case httpx.codes.OK:  # 200
                player_uuid = PlayerUuid(**response.json())
            case httpx.codes.NOT_FOUND:  # 404
                raise PlayerNotFoundError(response.text)
            case _:
                response.raise_for_status()
                raise ValueError(f"Unexpected HTTP status code: {response.status_code}")

        return await self.by_uuid_async(player_uuid)
