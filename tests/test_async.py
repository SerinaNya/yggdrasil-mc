import pytest

from yggdrasil_mc.client import YggdrasilMC

littleskin_api = "https://littleskin.cn/api/yggdrasil/"


@pytest.mark.asyncio
async def test_name_3rd():
    ygg = YggdrasilMC(littleskin_api)
    await ygg.by_name_async("SerinaNya")


@pytest.mark.asyncio
async def test_uuid_3rd():
    ygg = YggdrasilMC(littleskin_api)
    await ygg.by_uuid_async("a6abd9a95e4b4fe18f60777d1ab94ebb")


@pytest.mark.asyncio
async def test_name_official():
    ygg = YggdrasilMC()
    await ygg.by_name_async("SerinaNya")


@pytest.mark.asyncio
async def test_uuid_official():
    ygg = YggdrasilMC()
    await ygg.by_uuid_async("8705a5560b7447e8ba869169c31fb5ef")
