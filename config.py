SIZE = (1080, 720)
TILESIZE = 32
FPS = 60
FONT = 'fonts/Oswald-Medium.ttf'
FONT_SIZE = 32

BAR_W = 150
BAR_H = 20

#color
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

#player settings
min_speed_player = 0
start_speed_player = 2
max_speed_player = 8

start_hp_player = 100
max_hp_player = 150

start_damage_player = 20
max_damage_player = 30

player_weapon_cooldown = 1000

start_exp_player = 200

#enemyis settings
robber_hp = 50
robber_xp = 1
robber_damage = 1

enemy_weapon_cooldown = 1500

#Layer
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4



ABOUT_GAME = "Genre: Battle royale. From 2 to 4 players. The goal: to survive last. There are mobs on the map, killing which "
ABOUT_GAME1 = "earns experience points, which go to improve characteristics, and money that goes to buy and improve  "
ABOUT_GAME2 = "equipment. There is a boss on the map (like Roshan from Dota), killing which you get a bonus."

tilemap = [
    'BBBBBBBBBBBBBBBBBBBBB',
    'B...................B',
    'B..R............BB..B',
    'B...................B',
    'B...................B',
    'B...........P.......B',
    'B...................B',
    'B.....BBB.......R...B',
    'B.......B......B....B',
    'B.......B......BBB..B',
    'B...................B',
    'B........RRRR.RRRR......B',
    'B...............R....B',
    'BBBBBBBBBBBBBBBBBBBBB',
]
