import logging
from . import myglobals, analytics, navigation, offense

def docked_actions(current_ship):
    """
    Determine what to do with our docked ship
    :param Ship current_ship:
    :return: command to append to the command_queue
    :rtype: List
    """
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("docked_actions():")

    if myglobals.DEBUGGING['ship_loop']:
        myglobals.log.debug("-+=Docked ship #" + str(current_ship.id) + "=+-")

    # did we just complete docking?
    if current_ship in myglobals.dock_process_list.keys():
        if myglobals.DEBUGGING['docking_procedures']:
            myglobals.log.debug(" - completed docking")

        myglobals.dock_process_list.remove(current_ship)

    if myglobals.ALGORITHM['boobytrapping']:  # fully docked
        # is it time to bid thee farewell?
        if current_ship.planet.remaining_resources <= (
                current_ship.planet.num_docking_spots * myglobals.DOCKING_TURNS * myglobals.PRODUCTION) + 10:
            # syntax/logic in the following conditional (specifically the 'not') may be phrased wrong
            if not current_ship.planet in myglobals.planets_to_avoid:
                if myglobals.DEBUGGING['boobytrapping']:
                    log.debug("Leaving a present")

                myglobals.planets_to_avoid.append(current_ship.planet)
                myglobals.undock_process_list[current_ship] = current_ship.planet
                #command_queue.append(ship.undock(current_ship.planet))

                return ship.undock(current_ship.planet)

def undocked_actions(current_ship):
    """
    Determine what to do with the undocked ship
    :param Ship current_ship:
    :return: command to append to the command_queue
    :rtype: List
    """
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("undocked_actions():")

    if myglobals.DEBUGGING['ship_loop']:
        myglobals.log.debug("-+=Undocked ship #" + str(current_ship.id) + "=+-")

    # did we just complete undocking?
    if current_ship in myglobals.undock_process_list.keys():
        if myglobals.DEBUGGING['docking_procedures']:
            myglobals.log.debug(" - completed undocking")

        myglobals.undock_process_list.remove(current_ship)

    success = False
    myglobals.ranked_planets_by_distance = analytics.entity_sort_by_distance(current_ship, myglobals.game_map.all_planets())
    myglobals.ranked_our_planets_by_docked = analytics.planet_sort_ours_by_docked(myglobals.game_map.all_planets())
    myglobals.ranked_untapped_planets = \
        analytics.remove_tapped_planets(myglobals.ranked_planets_by_distance, myglobals.planets_to_avoid)
    enemies = analytics.get_enemy_ships()

    # get our command, if navigation to/docking with a planet is the best course of action
    # else None
    navigate_command = navigation.target_planet(current_ship, myglobals.ranked_planets_by_distance, 
                                                myglobals.ranked_our_planets_by_docked, myglobals.ranked_untapped_planets)

    if not navigate_command:
        # potential_angle = other_entities_in_vicinity(current_ship, enemies, ranked_untapped_planets[0]['distance'])
        if myglobals.ALGORITHM['offense']:  # and potential_angle:
            navigate_command = offense.go_offensive(current_ship, enemies)
        elif myglobals.ALGORITHM['reinforce'] and len(myglobals.ranked_our_planets_by_docked) > 0:
            navigate_command = \
                navigation.reinforce_planet(current_ship, myglobals.ranked_our_planets_by_docked, 
                                            myglobals.ranked_untapped_planets)

    return navigate_command
