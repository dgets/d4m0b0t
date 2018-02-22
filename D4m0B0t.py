import hlt
import logging
import bot_routines

game = hlt.Game("D4m0b0t - v3.0a")

#I do believe we'll toss globals up here for now; it's a better place to remember how ugly they are.
#Maybe it'll motivate me to coding a little less lazily here.

#global constants
class GConstants:
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

#globals
class GVariables:
    planets_to_avoid = []
    dock_process_list = {}
    undock_process_list = {}
    enemy_data = {}

    turn = 0

class Actions:
    def docked_actions(current_ship):
        """
        Determine what to do with our docked ship
        :param Ship current_ship:
        :return: command to append to the command_queue
        :rtype: List
        """
        if GConstants.DEBUGGING['method_entry']:
            log.debug("docked_actions():")

        if GConstants.DEBUGGING['ship_loop']:
            log.debug("-+=Docked ship #" + str(current_ship.id) + "=+-")

        # did we just complete docking?
        if current_ship in GVariables.dock_process_list.keys():
            if GConstants.DEBUGGING['docking_procedures']:
                log.debug(" - completed docking")

            GVariables.dock_process_list.remove(current_ship)

        if GConstants.ALGORITHM['boobytrapping']:  # fully docked
            # is it time to bid thee farewell?
            if current_ship.planet.remaining_resources <= (
                    current_ship.planet.num_docking_spots * GConstants.DOCKING_TURNS * GConstants.PRODUCTION) + 10:
                # syntax/logic in the following conditional (specifically the 'not') may be phrased wrong
                if not current_ship.planet in GVariables.planets_to_avoid:
                    if GConstants.DEBUGGING['boobytrapping']:
                        log.debug("Leaving a present")

                    GVariables.planets_to_avoid.append(current_ship.planet)
                    GVariables.undock_process_list[current_ship] = current_ship.planet
                    command_queue.append(ship.undock(current_ship.planet))


    def undocked_actions(current_ship):
        """
        Determine what to do with the undocked ship
        :param Ship current_ship:
        :return: command to append to the command_queue
        :rtype: List
        """
        if GConstants.DEBUGGING['method_entry']:
            log.debug("undocked_actions():")

        if GConstants.DEBUGGING['ship_loop']:
            log.debug("-+=Undocked ship #" + str(current_ship.id) + "=+-")

        # did we just complete undocking?
        if current_ship in GVariables.undock_process_list.keys():
            if GConstants.DEBUGGING['docking_procedures']:
                log.debug(" - completed undocking")

            GVariables.undock_process_list.remove(current_ship)

        success = False
        ranked_planets_by_distance = bot_routines.Analytics.entity_sort_by_distance(current_ship, game_map.all_planets())
        ranked_our_planets_by_docked = bot_routines.Analytics.planet_sort_ours_by_docked(game_map.all_planets())
        ranked_untapped_planets = \
            bot_routines.Analytics.remove_tapped_planets(ranked_planets_by_distance, GVariables.planets_to_avoid)
        enemies = bot_routines.Analytics.get_enemy_ships()

        # get our command, if navigation to/docking with a planet is the best course of action
        # else None
        navigate_command = GVariables.target_planet( \
                                        current_ship, ranked_planets_by_distance, ranked_our_planets_by_docked, \
                                        ranked_untapped_planets)

        if not navigate_command:
            # potential_angle = other_entities_in_vicinity(current_ship, enemies, ranked_untapped_planets[0]['distance'])
            if GConstants.ALGORITHM['offense']:  # and potential_angle:
                navigate_command = bot_routines.Offense.go_offensive(current_ship, enemies)
            elif GConstants.ALGORITHM['reinforce'] and len(ranked_our_planets_by_docked) > 0:
                navigate_command = \
                    Navigation.reinforce_planet(current_ship, ranked_our_planets_by_docked, ranked_untapped_planets)

        return navigate_command

#entrance
log = logging.getLogger(__name__)
logging.info("D4m0b0t v3.0a active")

# begin primary game loop
while True:
    if GConstants.DEBUGGING['ship_loop']:
        log.debug("-+Beginning turn+-")

    game_map = game.update_map()
    my_id = game_map.get_me().id
    # default_speed = int(hlt.constants.MAX_SPEED / 2)
    # default_speed = int(hlt.constants.MAX_SPEED / 1.75)
    default_speed = hlt.constants.MAX_SPEED

    command_queue = []
    targeted_list = []

    for ship in game_map.get_me().all_ships():
        if ship.docking_status == ship.DockingStatus.DOCKED:
            new_command = docked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
        elif ship.docking_status == ship.DockingStatus.UNDOCKED:
            new_command = undocked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
    # end per-ship iteration

    turn += 1
    game.send_command_queue(command_queue)
