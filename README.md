<div align="center">

# yggdrasil-mc

_A simple Python lib to get player info and texture from Mojang and Yggdrasil APIs._

> 一个简单的 Python 库，可从 Mojang 和 Yggdrasil APIs 获取玩家的信息和材质。
</div>

<p align="center">
<img src="https://img.shields.io/github/stars/SerinaNya/yggdrasil-mc?style=social" alt="GitHub Repo stars">
<img src="https://img.shields.io/pypi/v/yggdrasil-mc?style=flat-square" alt="PyPI">
<img src="https://img.shields.io/pypi/pyversions/yggdrasil-mc?style=flat-square" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/last-commit/SerinaNya/yggdrasil-mc/main?style=flat-square" alt="GitHub last commit (branch)">
<img src="https://img.shields.io/github/license/SerinaNya/yggdrasil-mc?style=flat-square" alt="GitHub">
</p>



## Attention

This package can be used with **Python 3.10+ ONLY**.

## Usage

``` shell
pip3 install yggdrasil-mc
```

``` python
from yggdrasil_mc.client import YggdrasilMC

ygg = YggdrasilMC()
await ygg.by_name_async("SerinaNya")
```
