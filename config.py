
from working_with_csv_files import read_csv

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

blindtime = 500

#enemyis settings
robber_hp = 50
robber_xp = 1
robber_damage = 20

robber_boss_hp = 300
robber_boss_xp = 1
robber_boss_damage = 35
robber_boss_speed = 1

enemy_weapon_cooldown = 1500
blindtime_robber = 600

#Layer
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4



ABOUT_GAME = "Genre: Battle royale. From 2 to 4 players. The goal: to survive last. There are mobs on the map, killing which "
ABOUT_GAME1 = "earns experience points, which go to improve characteristics, and money that goes to buy and improve  "
ABOUT_GAME2 = "equipment. There is a boss on the map (like Roshan from Dota), killing which you get a bonus."


layers_of_map = [
    read_csv('../projectravil/csv_files/map_rpg_block.csv'),  # map border   index-0
    read_csv('../projectravil/csv_files/map_rpg_trees.csv'),  # trees         index-1
    read_csv('../projectravil/csv_files/map_rpg_robbers.csv'), # robbers        index-2
    read_csv('../projectravil/csv_files/map_rpg_boss.csv') # bosses index-3
]

