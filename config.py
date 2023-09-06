
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

robber_boss_hp = 100
robber_boss_xp = 1
robber_boss_damage = 35
robber_boss_speed = 2

enemy_weapon_cooldown = 1500
blindtime_robber = 600

#Layer
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4





ABOUT_GAME = "A walker with RPG elements. The goal of the game is to kill as many enemies on the map as possible. For "
ABOUT_GAME1 = "killing you get experience. The more experience, the higher the level. The higher the level,the"
ABOUT_GAME2 = "The higher the level, the easier it is to play, but the enemies also become stronger, so be careful!"



layers_of_map = [
    read_csv('../projectravil/csv_files/map_rpg_block.csv'),  # map border   index-0
    read_csv('../projectravil/csv_files/map_rpg_trees.csv'),  # trees         index-1
    read_csv('../projectravil/csv_files/map_rpg_robbers.csv'), # robbers        index-2
    read_csv('../projectravil/csv_files/map_rpg_boss.csv') # bosses index-3
]

