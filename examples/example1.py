import asyncio
from yggdrasil_mc.client import YggdrasilMC

littleskin_api = "https://littleskin.cn/api/yggdrasil/"


async def example_name_3rd():
    ygg = YggdrasilMC(littleskin_api)
    return await ygg.by_name_async("SerinaNya")


async def example_uuid_3rd():
    ygg = YggdrasilMC(littleskin_api)
    return await ygg.by_uuid_async("a6abd9a95e4b4fe18f60777d1ab94ebb")


async def example_name_official():
    ygg = YggdrasilMC()
    return await ygg.by_name_async("SerinaNya")


async def example_uuid_official():
    ygg = YggdrasilMC()
    return await ygg.by_uuid_async("8705a5560b7447e8ba869169c31fb5ef")


async def main():
    for func in [
        example_name_3rd,
        example_uuid_3rd,
        example_name_official,
        example_uuid_official,
    ]:
        print(repr(await func()))


asyncio.run(main())
