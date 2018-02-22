#include D4m0B0t.py

def go_offensive(current_ship, enemies):
    """
    Returns navigation command for offense, or None if not the best course of action at this juncture
    :param Ship current_ship:
    :param List of Tuples enemies:
    :return navigation_command or None:
    :rtype: String or None
    """
    navigate_command = None

    if D4m0B0t.DEBUGGING['offense']:
        log.debug("Engaging enemy")

    close_enemies = entity_sort_by_distance(current_ship, enemies)
    closest_enemy = close_enemies[0]['entity_object']
    close_friendlies = entity_sort_by_distance(current_ship, game_map.get_me().all_ships())

    # implementation of kamikaze was never completed
    if ALGORITHM['kamikaze']:
        potential_kamikaze_angle = other_entities_in_vicinity(current_ship, enemies,
                                                              100)  # note '100' was for debugging

        if DEBUGGING['kamikaze']:
            log.debug(" - potential_kamikaze_angle: " + str(potential_kamikaze_angle))

        if potential_kamikaze_angle:
            if DEBUGGING['kamikaze'] and DEBUGGING['offense']:
                log.debug(" - going kamikaze")

            navigate_command = current_ship.thrust(hlt.constants.MAX_SPEED, potential_kamikaze_angle)

    if not ALGORITHM['kamikaze'] or not navigate_command:
        if DEBUGGING['offense']:
            log.debug(" - engaging ship #" + str(closest_enemy.id))

        num_enemies_in_range = count_ships_in_firing_range(current_ship, close_enemies, MAX_FIRING_DISTANCE)
        num_friendlies_in_range = count_ships_in_firing_range(current_ship, close_friendlies, MAX_FIRING_DISTANCE)

        if not ALGORITHM['ram_ships_when_weak'] or (closest_enemy.health <= current_ship.health and
                                                    num_enemies_in_range <= num_friendlies_in_range):
            # standard offense, stay with 'em and shoot 'em
            if DEBUGGING['ram_ships_when_weak']:
                log.debug("   - firing on enemy, not ramming")

            navigate_command = current_ship.navigate(
                current_ship.closest_point_to(closest_enemy),
                game_map,
                speed=default_speed,
                ignore_ships=False)
        else:
            # RAMMING SPEED!
            if DEBUGGING['ram_ships_when_weak'] and (num_enemies_in_range <= num_friendlies_in_range):
                log.debug("   - ship #" + str(closest_enemy.id) + " is stronger w/" + str(closest_enemy.health) + \
                          " health vs my " + str(current_ship.health) + " - ramming speed!")
            elif DEBUGGING['ram_ships_when_weak']:
                log.debug(
                    "   - my ship #" + str(current_ship.id) + " is outnumbered " + str(num_enemies_in_range) + ":" + \
                    str(num_friendlies_in_range) + " - ramming speed!")

            navigate_command = current_ship.navigate(
                closest_enemy,
                game_map,
                speed=hlt.constants.MAX_SPEED,
                avoid_obstacles=True,
                ignore_ships=True,
                ignore_planets=False)

    return navigate_command


def offensive_targeting(current_entity, other_entities):
    """
    Check for enemies within firing range
    :param Entity current_entity:
    :param List other_entities:
    :return: intercept angle or None
    :rtype: float
    """
    if DEBUGGING['method_entry']:
        log.debug("offensive_targeting():")

    enemy_intercept_angle = other_entities_in_vicinity(current_entity, other_entities, 5)

    if enemy_intercept_angle:
        return enemy_intercept_angle
    else:
        return None

