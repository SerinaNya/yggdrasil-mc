from yggdrasil_mc import YggPlayerUuid, YggPlayerProfile

player_name = "w84"
player = YggPlayerUuid().getMojang(player_name)
if player.existed:
    print(YggPlayerProfile().getMojang(player.id))

# OUTPUT >>>
# id='ca244462f8e5494791ec98f0ccf505ac' name='w84' properties=Properties(...
