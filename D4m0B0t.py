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
