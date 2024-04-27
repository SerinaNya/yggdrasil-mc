from typing import Literal, Annotated

from pydantic import AliasPath, BaseModel, Field, AnyHttpUrl


class PlayerUuid(BaseModel):
    id: str
    name: str

    @property
    def existed(self) -> bool:
        """
        Returns a boolean value indicating whether the player is existed.
        """
        return self.id is not None


class PlayerSkin_MetaData(BaseModel):
    model: Literal["default", "slim"] = "default"


class PlayerTexutureBase(BaseModel):
    url: AnyHttpUrl

    @property
    def hash(self) -> str | None:
        """
        Returns the hash part of the texture URL.
        """
        return str(self.url).split("/")[-1] if self.url else None


class PlayerSkin(PlayerTexutureBase):
    metadata: Annotated[PlayerSkin_MetaData, Field(default_factory=PlayerSkin_MetaData)]


class PlayerCape(PlayerTexutureBase):
    ...


class PlayerProfile(BaseModel):
    id: Annotated[str, Field(..., validation_alias="profileId")]
    name: Annotated[str, Field(..., validation_alias="profileName")]

    skin: Annotated[
        PlayerSkin | None,
        Field(default=None, validation_alias=AliasPath("textures", "SKIN")),
    ]
    cape: Annotated[
        PlayerCape | None,
        Field(default=None, validation_alias=AliasPath("textures", "CAPE")),
    ]
