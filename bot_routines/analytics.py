from . import myglobals
from operator import itemgetter

def count_ships_in_firing_range(current_ship, entities_for_consideration, max_range):
    """
    Determine how many ships are within our offensive bubble
    :param Ship current_ship:
    :param List of Tuples entities_for_consideration:
    :param float max_range:
    :return int ships in range:
    :rtype: int
    """
    cntr = 0
    # enemies_potentially_in_range = entity_sort_by_distance(current_ship, enemies)
    for current_enemy in entities_for_consideration:
        if current_enemy['distance'] <= max_range:
            cntr += 1
        else:
            break  # don't waste the processing time

    return cntr

def remove_held_planets(planets_list):
    """
    Remove all planets from the list that are already held by a player
    :param List planets_list: List of Tuples containing planet_object => object
    :return List with owned planets removed:
    :rtype: List of Typles
    """
    if DEBUGGING['method_entry']:
        log.debug("remove_held_planets():")

    for possibly_owned_planet in planets_list:
        if not possibly_owned_planet:
            if DEBUGGING['targeting']:
                log.debug(" - removing owned planet #" + str(possibly_owned_planet['entity_object'].id) + " from list")

            planets_list.remove(possibly_owned_planet)

    return planets_list

def entity_sort_by_distance(current_ship, planet_list):
    """
    Sort the given solar system into planets weighted by least distance from given ship to planet
    :param Ship current_ship:
    :param List planet_list:
    :return: List of tuples containing entity_object & distance from current_ship
    :rtype: List of Tuples
    """
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("entity_sort_by_distance():")

    nang = []
    for ouah in planet_list:
        nang.append({'entity_object': ouah, 'distance': ouah.calculate_distance_between(current_ship)})

    return sorted(nang, key=itemgetter('distance'))

def planet_sort_ours_by_docked(planet_list):
    """
    Sort the given solar system into planets weighted by least ships docked
    :param List planet_list: List of planets to be weighted
    :return: List of tuples of weighted planets
    :rtype: List of Tuples
    """
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("planet_sort_by_docked():")

    nang = []
    for ouah in planet_list:
        if ouah.owner == myglobals.game_map.get_me():
            nang.append({'entity_object': ouah, 'number_docked': len(ouah.all_docked_ships())})

    if len(nang) > 0:
        # remove planets with no docking slots open
        for ouah in nang:
            if ouah['number_docked'] >= ouah['entity_object'].num_docking_spots:
                nang.remove(ouah)

    return sorted(nang, key=itemgetter('number_docked'))

def other_entities_in_vicinity(current_entity, other_entities, scan_distance):
    """
    Check to see if there are any more specified entities within the immediate vicinity
    :param Entity current_entity:
    :param List other_entities:
    :param integer scan_distance:
    :return: Collision angle if any
    :rtype: Collision angle or none
    """
    if DEBUGGING['method_entry']:
        log.debug("other_entities_in_vicinity()")

    # closest_docked_distance = scan_distance
    target_planet = None

    for other_entity in other_entities:
        # if other_entity.docking_status == current_entity.DockingStatus.DOCKED or \
        #   other_entity.docking_status == current_entity.DockingStatus.DOCKING:
        if current_entity.planet:
            continue

        proximity = int(current_entity.calculate_distance_between(other_entity))
        if DEBUGGING['kamikaze']:
            log.debug("\t- current_entity's proximity: " + str(proximity) + " vs scan_distance: " + str(scan_distance))

        if proximity < scan_distance:
            if DEBUGGING['kamikaze']:
                log.debug("\t- proximity is less than scan_distance")

        if current_entity.docking_status == current_entity.DockingStatus.DOCKED or \
                current_entity.docking_status == current_entity.DockingStatus.DOCKING:
            if DEBUGGING['kamikaze']:
                log.debug("\t\t- setting target_planet to current_entity.planet")

            target_planet = current_entity.planet
            break
        else:
            continue

    if target_planet:
        return current_entity.calculate_angle_between(target_planet)

    return None

def get_enemy_ships():
    """
    Retrieve all enemy ships
    :return: all enemy ships
    :rtype: List of ships
    """
    if DEBUGGING['method_entry']:
        log.debug("get_enemy_ships():")

    enemy_ships = []
    for jackass in game_map.all_players():
        if not jackass == game_map.get_me():
            for ship in jackass.all_ships():
                enemy_ships.append(ship)

    return enemy_ships

def remove_tapped_planets(testing_planets, avoid_planets):
    """
    Remove all avoid_planets from testing_planets
    :param List testing_planets:
    :param List avoid_planets:
    :return: planets sans tapped planets
    :rtype: List of planets
    """
    if myglobals.DEBUGGING['method_entry']:
        myglobals.log.debug("remove_tapped_planets():")

    for bogus in avoid_planets:
        if bogus in testing_planets:
            testing_planets.remove(bogus)  # this is going to fail if python passes immutably

    return testing_planets

