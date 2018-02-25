import logging
from . import myglobals, analytics

class Primary_Action:
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
        myglobals.ranked_planets_by_distance = analytics.entity_sort_by_distance(current_ship, game_map.all_planets())
        myglobals.ranked_our_planets_by_docked = analytics.planet_sort_ours_by_docked(game_map.all_planets())
        myglobals.ranked_untapped_planets = \
            analytics.remove_tapped_planets(ranked_planets_by_distance, GVariables.planets_to_avoid)
        enemies = analytics.get_enemy_ships()

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