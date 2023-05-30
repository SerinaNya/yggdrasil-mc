from yggdrasil_mc import YggdrasilPlayer

player_name = "w84"
ygg = YggdrasilPlayer()
player = ygg.Uuid.getMojang(player_name)
if player.existed:
    print(ygg.Profile.getMojang(player.id))

# OUTPUT >>>
# id='ca244462f8e5494791ec98f0ccf505ac' name='w84' properties=Properties(...
