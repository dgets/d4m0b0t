import hlt
import logging
import bot_routines

game = hlt.Game("D4m0b0t - v3.0a")
bot_routines.myglobals.game_map = game.update_map()
bot_routines.myglobals.my_id = bot_routines.myglobals.game_map.get_me().id
bot_routines.myglobals.default_speed = hlt.constants.MAX_SPEED

#entrance
logging.info("D4m0b0t v3.0a active")

# begin primary game loop
while True:
    if bot_routines.myglobals.DEBUGGING['ship_loop']:
        bot_routines.myglobals.log.debug("-+Beginning turn+-")

    if bot_routines.myglobals.turn > 0:
        bot_routines.myglobals.game_map = game.update_map()
    
    command_queue = []
    #targeted_list = []    #not certain if this needs to be here, or in globals
    #would it improve efficiency to have the following entry be in globals?  ie less passing of it around?
    enemies = bot_routines.analytics.get_enemy_ships()
    
    #clean up any ships that've been destroyed
    for enemy_telemetry_entry in bot_routines.myglobals.enemy_telemetry:
        if not enemy_telemetry_entry.still_alive(enemies):
            bot_routines.myglobals.enemy_telemetry.remove(enemy_telemetry_entry)

    #figger out wzza for each of their ships
    for ship in enemies:    #bot_routines.analytics.get_enemy_ships():
        found = False
        
        #if len(bot_routines.myglobals.enemy_telemetry) > 0:
        for enemy_telemetry_entry in bot_routines.myglobals.enemy_telemetry:
            if ship.id == enemy_telemetry_entry.id:
                found = True
                enemy_telemetry_entry.update(ship.x, ship.y)
                break
        
        if found:
            continue
        else:
            #create new telemetry entry
            bot_routines.myglobals.enemy_telemetry.append(bot_routines.telemetry.EnemyData(ship.id, ship.x, ship.y))
            
    #here we should probably check to see if we need to remove entries from telemetry

    #figger out wzza for each of my ships
    for ship in bot_routines.myglobals.game_map.get_me().all_ships():
        if ship.docking_status == ship.DockingStatus.DOCKED:
            new_command = bot_routines.primary_action.docked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
        elif ship.docking_status == ship.DockingStatus.UNDOCKED:
            new_command = bot_routines.primary_action.undocked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
    # end per-ship iteration

    bot_routines.myglobals.turn += 1
    game.send_command_queue(command_queue)
