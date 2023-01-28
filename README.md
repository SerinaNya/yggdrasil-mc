# yggdrasil-mc

![GitHub Repo stars](https://img.shields.io/github/stars/jinzhijie/yggdrasil-mc?style=social) ![PyPI](https://img.shields.io/pypi/v/yggdrasil-mc?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yggdrasil-mc?style=flat-square) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/jinzhijie/yggdrasil-mc/main?style=flat-square) ![GitHub](https://img.shields.io/github/license/jinzhijie/yggdrasil-mc?style=flat-square)

A simple Python lib to get player info and texture from Mojang and Blessing Skin.

一个简单的 Python 库，可从 Mojang 和 Blessing Skin 获取玩家的信息和材质。

## Attention

This package can run in **Python 3.10+ ONLY**.

## Usage

1. Download the package from PyPI
    ```bash
    pip3 install -U yggdrasil-mc
    ```

2.  ```python
    from yggdrasil_mc.ygg import YggdrasilPlayerUuidApi

    player_name = "w84"
    player = YggdrasilPlayerUuidApi.getMojangServer(player_name)
    if player.existed:
        print(player.id)
    ```

After you run these snippet, you will get the following output:
```plain
ca244462f8e5494791ec98f0ccf505ac
```

Note that this package also provide the asyncio version which is powered by aiohttp:
```python
from yggdrasil_mc.ygg_async import YggdrasilPlayerUuidApi

player_name = "w84"

async get_player_uuid(player_name: str = player_name)
    player = await YggdrasilPlayerUuidApi.getMojangServer(player_name)
    return player.id
```