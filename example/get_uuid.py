from yggdrasil_mc.ygg import YggdrasilPlayerUuidApi

player_name = "w84"
player = YggdrasilPlayerUuidApi.getMojangServer(player_name)
if player.existed:
    print(player.id)


# OUTPUT >>>
# ca244462f8e5494791ec98f0ccf505ac
