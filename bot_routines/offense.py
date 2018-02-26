import hlt
from . import analytics, myglobals

def go_offensive(current_ship, enemies):
    """
    Returns navigation command for offense, or None if not the best course of action at this juncture
    :param Ship current_ship:
    :param List of Tuples enemies:
    :return navigation_command or None:
    :rtype: String or None
    """
    navigate_command = None

    if myglobals.DEBUGGING['offense']:
        myglobals.log.debug("Engaging enemy")

    close_enemies = analytics.entity_sort_by_distance(current_ship, enemies)
    closest_enemy = close_enemies[0]['entity_object']
    close_friendlies = analytics.entity_sort_by_distance(current_ship, myglobals.game_map.get_me().all_ships())

    # implementation of kamikaze was never completed
    if myglobals.ALGORITHM['kamikaze']:
        potential_kamikaze_angle = analytics.other_entities_in_vicinity(current_ship, enemies,
                                                          100)  # note '100' was for debugging

        if myglobals.DEBUGGING['kamikaze']:
            myglobals.log.debug(" - potential_kamikaze_angle: " + str(potential_kamikaze_angle))

        if potential_kamikaze_angle:
            if myglobals.DEBUGGING['kamikaze'] and myglobals.DEBUGGING['offense']:
                myglobals.log.debug(" - going kamikaze")

            navigate_command = current_ship.thrust(hlt.constants.MAX_SPEED, potential_kamikaze_angle)

    if not myglobals.ALGORITHM['kamikaze'] or not navigate_command:
        if myglobals.DEBUGGING['offense']:
            myglobals.log.debug(" - engaging ship #" + str(closest_enemy.id))

        num_enemies_in_range = analytics.count_ships_in_firing_range(current_ship, close_enemies, myglobals.MAX_FIRING_DISTANCE)
        num_friendlies_in_range = analytics.count_ships_in_firing_range(current_ship, close_friendlies, \
                myglobals.MAX_FIRING_DISTANCE)

        if not myglobals.ALGORITHM['ram_ships_when_weak'] or (closest_enemy.health <= current_ship.health and
                                                                num_enemies_in_range <= num_friendlies_in_range):
            # standard offense, stay with 'em and shoot 'em
            if myglobals.DEBUGGING['ram_ships_when_weak']:
                myglobals.log.debug("   - firing on enemy, not ramming")

            navigate_command = current_ship.navigate(
                current_ship.closest_point_to(closest_enemy),
                myglobals.game_map,
                speed=myglobals.default_speed,
                ignore_ships=False)
        else:
            # RAMMING SPEED!
            if myglobals.DEBUGGING['ram_ships_when_weak'] and (num_enemies_in_range <= num_friendlies_in_range):
                myglobals.log.debug("   - ship #" + str(closest_enemy.id) + " is stronger w/" + \
                        str(closest_enemy.health) + \
                        " health vs my " + str(current_ship.health) + " - ramming speed!")
            elif myglobals.DEBUGGING['ram_ships_when_weak']:
                myglobals.log.debug(
                    "   - my ship #" + str(current_ship.id) + " is outnumbered " + str(num_enemies_in_range) + ":" + \
                    str(num_friendlies_in_range) + " - ramming speed!")

            navigate_command = current_ship.navigate(
                closest_enemy,
                myglobals.game_map,
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
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("offensive_targeting():")

    enemy_intercept_angle = analytics.other_entities_in_vicinity(current_entity, other_entities, 5)

    if enemy_intercept_angle:
        return enemy_intercept_angle
    else:
        return None
