from urllib.parse import urljoin
from uuid import UUID

import httpx

from yggdrasil_mc.exceptions import PlayerNotFoundError
from yggdrasil_mc.models import PlayerProfile, PlayerUuid


class YggdrasilMC:
    api_root: str | None

    def __init__(self, api_root: str | None = None):
        """
        Initializes the class instance.

        Parameters:
            api_root (str | None): The root URL of the API. If None, the default Mojang server is used.

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
            player_uuid (str | PlayerUuid | UUID): The UUID / PlayerUuid of the player.

        Returns:
            PlayerProfile: The player's profile.

        Raises:
            PlayerNotFoundError: If the player is not found.
            ValueError: If an unexpected error occurs.
        """

        # Convert player_uuid to a string or UUID if necessary
        player_uuid: str | UUID = (
            player_uuid.id if isinstance(player_uuid, PlayerUuid) else player_uuid
        )
        # Convert player_uuid to a hex string if necessary
        player_uuid: str = player_uuid.hex if isinstance(player_uuid, UUID) else player_uuid

        async with httpx.AsyncClient(
            http2=True,
            base_url=urljoin(self.api_root, "sessionserver")
            if self.api_root
            else "https://sessionserver.mojang.com",
        ) as client:
            response = await client.get(f"/session/minecraft/profile/{player_uuid}")

        match response.status_code:
            case httpx.codes.OK:  # 200
                return PlayerProfile.model_validate(response.json())
            case httpx.codes.NO_CONTENT:  # 204
                raise PlayerNotFoundError(
                    f"Server has responded 204 No Content, {player_uuid=}"
                )
            case httpx.codes.BAD_REQUEST:  # 400
                raise PlayerNotFoundError(response.text)
            case _:
                raise ValueError(response.text)

    async def by_name_async(self, player_name: str) -> PlayerProfile:
        """
        Get a player's profile by their name. (async)

        Args:
            player_name (str): The name of the player to retrieve the profile for.

        Returns:
            PlayerProfile: The player's profile.

        Raises:
            PlayerNotFoundError: If the player is not found.
            ValueError: If an unexpected error occurs.
        """

        async with httpx.AsyncClient(
            http2=True,
            base_url=urljoin(self.api_root, "api")
            if self.api_root
            else "https://api.mojang.com",
        ) as client:
            response = await client.get(f"/users/profiles/minecraft/{player_name}")

        match response.status_code:
            case httpx.codes.OK:  # 200
                player_uuid = PlayerUuid.model_validate(response.json())
            case httpx.codes.NOT_FOUND:  # 404
                raise PlayerNotFoundError(response.text)
            case _:
                raise ValueError(response.text)

        return await self.by_uuid_async(player_uuid)
