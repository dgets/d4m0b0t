class Navigation:
    def target_planet(current_ship, planets_ranked_by_distance, planets_ranked_ours_by_docked, planets_ranked_untapped):
        """
        Determine if a planet is a viable target for mining; create the navigation command if so
        :param Ship current_ship:
        :param List of Tuples planets_ranked_by_distance:
        :param List of Tuples planets_ranked_ours_by_docked:
        :param List of Tuples planets_ranked_untapped:
        :return: navigation command for command_queue or None
        :rtype: String or None
        """
        navigate_command = None

        # do we navigate to a planet, reinforce, or go offensive?
        # navigate to a planet or begin docking (this also currently handles reinforcing)
        for potential_planet in remove_held_planets(planets_ranked_untapped):
            if (potential_planet['entity_object'] in targeted_list) or \
                    (potential_planet['entity_object'].num_docking_spots == len(
                        potential_planet['entity_object'].all_docked_ships())):
                if DEBUGGING['targeting']:
                    log.debug(" - skipping already targeted or full planet #" + str(potential_planet['entity_object'].id))

                continue
            if current_ship.can_dock(potential_planet['entity_object']):  # why ship & not current_ship again?
                if DEBUGGING['planet_selection']:
                    log.debug(" - docking with planet #" + str(potential_planet['entity_object'].id))

                # dock_process_list[current_ship] = potential_planet['entity_object']
                navigate_command = current_ship.dock(potential_planet['entity_object'])
                if potential_planet['entity_object'] in targeted_list:
                    if DEBUGGING['planet_selection']:
                        log.debug(
                            " - removing planet #" + str(potential_planet['entity_object'].id) + " from targeted_list")

                    targeted_list.remove(potential_planet['entity_object'])
                break
            elif potential_planet['entity_object'] not in targeted_list:
                if DEBUGGING['targeting']:
                    log.debug(" - navigating to planet #" + str(potential_planet['entity_object'].id))

                targeted_list.append(potential_planet['entity_object'])
                navigate_command = current_ship.navigate(
                    current_ship.closest_point_to(potential_planet['entity_object']),
                    game_map,
                    speed=default_speed,
                    ignore_ships=False)
                break

        return navigate_command


    def reinforce_planet(current_ship, our_planets_by_docked, our_ranked_untapped_planets):
        """
        Create navigation command to reinforce the nearest planet with an open docking spot
        NOTE: This is currently not utilized, and almost certainly broken
        :param Ship current_ship: derp
        :param List our_planets_by_docked: List of Tuples
        :param List our_ranked_untapped_planets: List of Tuples
        :return String navigation_command:
        :rtype: String
        """
        navigation_command = None

        # reinforce that sucker
        if DEBUGGING['reinforce']:
            log.debug("Reinforcing planet #" + str(ranked_our_planets_by_docked[0]['entity_object'].id))

        if current_ship.can_dock(ranked_our_planets_by_docked[0]['entity_object']):
            if DEBUGGING['reinforce']:
                log.debug(" - docking @ planet #" + str(ranked_our_planets_by_docked[0]['entity_object'].id))

            navigate_command = current_ship.dock(ranked_our_planets_by_docked[0]['entity_object'])
        else:
            if DEBUGGING['reinforce']:
                log.debug(" - navigating to reinforce planet #" + str(ranked_untapped_planets[0]['entity_object']))

            navigate_command = current_ship.navigate(
                current_ship.closest_point_to(ranked_untapped_planets[0]['entity_object']),
                game_map,
                speed=default_speed,
                ignore_ships=False)

        return navigation_command
