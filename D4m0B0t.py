import hlt
import logging
import bot_routines
#from bot_routines import myglobals
#from bot_routines import Navigation, Analytics, Offense, Primary_Action
#from bot_routines import primary_action

game = hlt.Game("D4m0b0t - v3.0a")

#entrance
logging.info("D4m0b0t v3.0a active")

# begin primary game loop
while True:
    if bot_routines.myglobals.DEBUGGING['ship_loop']:
        bot_routines.myglobals.log.debug("-+Beginning turn+-")

    game_map = game.update_map()
    my_id = game_map.get_me().id
    # default_speed = int(hlt.constants.MAX_SPEED / 2)
    # default_speed = int(hlt.constants.MAX_SPEED / 1.75)
    default_speed = hlt.constants.MAX_SPEED

    command_queue = []
    targeted_list = []

    for ship in game_map.get_me().all_ships():
        if ship.docking_status == ship.DockingStatus.DOCKED:
            new_command = bot_routines.Primary_Action.docked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
        elif ship.docking_status == ship.DockingStatus.UNDOCKED:
            new_command = bot_routines.Primary_Action.undocked_actions(ship)
            if new_command:
                command_queue.append(new_command)
            continue
    # end per-ship iteration

    bot_routines.myglobals.turn += 1
    game.send_command_queue(command_queue)
