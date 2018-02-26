import logging

#class MyGlobals:
# 'constants'
DEBUGGING = {
    'ship_loop': True,
    'docking_procedures': False,
    'reinforce': False,
    'offense': True,
    'ram_ships_when_weak': True,
    'kamikaze': False,
    'planet_selection': False,
    'targeting': False,
    'boobytrapping': False,
    'enemy_data': True,
    'method_entry': True
}
ALGORITHM = {
    'reinforce': False,
    'offense': True,
    'ram_ships_when_weak': True,
    'kamikaze': False,
    'boobytrapping': True
}
 
PRODUCTION = 6
DOCKING_TURNS = 5
MAX_FIRING_DISTANCE = 5
 
# variables
planets_to_avoid = []
targeted_list = []
enemy_telemetry = []
dock_process_list = {}
undock_process_list = {}
enemy_data = {}
#enemy_telemetry = {}
 
turn = 0
log = logging.getLogger(__name__)
game_map = None
default_speed = None
my_id = None

