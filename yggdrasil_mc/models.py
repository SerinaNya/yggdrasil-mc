from typing import Literal

from pydantic import AliasPath, BaseModel, Field, HttpUrl


class PlayerUuid(BaseModel):
    id: str | None
    name: str | None

    @property
    def existed(self) -> bool:
        """
        Returns a boolean value indicating whether the player is existed.
        """
        return self.id is not None


class PlayerSkin_MetaData(BaseModel):
    model: Literal["default", "slim"] = Field(default="default")


class PlayerTexutureBase(BaseModel):
    url: HttpUrl | None

    @property
    def hash(self) -> str | None:
        """
        Returns the hash part of the texture URL.
        """
        return str(self.url).split("/")[-1] if self.url else None


class PlayerSkin(PlayerTexutureBase):
    metadata: PlayerSkin_MetaData | None = Field(default_factory=PlayerSkin_MetaData)


class PlayerCape(PlayerTexutureBase):
    ...


class PlayerProfile(BaseModel):
    id: str = Field(..., validation_alias="profileId")
    name: str =  Field(..., validation_alias="profileName")
    skin: PlayerSkin | None = Field(default=None, validation_alias=AliasPath("textures", "SKIN"))
    cape: PlayerCape | None = Field(default=None, validation_alias=AliasPath("textures", "CAPE"))
