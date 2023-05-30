# yggdrasil-mc

![GitHub Repo stars](https://img.shields.io/github/stars/jinzhijie/yggdrasil-mc?style=social) ![PyPI](https://img.shields.io/pypi/v/yggdrasil-mc?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yggdrasil-mc?style=flat-square) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/jinzhijie/yggdrasil-mc/main?style=flat-square) ![GitHub](https://img.shields.io/github/license/jinzhijie/yggdrasil-mc?style=flat-square)

A simple Python lib to get player info and texture from Mojang and Yggdrasil APIs.

一个简单的 Python 库，可从 Mojang 和 Yggdrasil APIs 获取玩家的信息和材质。

## Attention

This package can run in **Python 3.10+ ONLY**.

## Usage

1. Download the package from PyPI

    ```bash
    pip3 install -U yggdrasil-mc
    ```

2. ```python
    from yggdrasil_mc import YggdrasilPlayer

    player_name = "w84"
    ygg = YggdrasilPlayer()
    player = ygg.Uuid.getMojang(player_name)
    if player.existed:
        print(ygg.Profile.getMojang(player.id))
    ```

After you run these snippet, you will get the following output:

```plain
id='ca244462f8e5494791ec98f0ccf505ac' name='w84' properties=Properties(...
```

Note that this package also provide the asyncio version which is powered by aiohttp:

```python
from yggdrasil_mc import YggdrasilPlayer

player_name = "w84"
ygg = YggdrasilPlayer()
player = await ygg.Uuid.getMojangAsync(player_name)
if player.existed:
    print(await ygg.Profile.getMojangAsync(player.id))
```
