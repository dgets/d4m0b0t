import hlt

from math import atan2, degrees, sqrt
from . import myglobals, analytics

class EnemyData:
    """
    Class represents an entry in the telemetry data for one enemy.  Currently
    this only holds positional data for the past 2 turns, and target weight
    based on the last 5 turns.
    """
    
    def __init__(self, ship_id, x, y):
        if myglobals.DEBUGGING['enemy_data']:
            myglobals.log.debug("Initializing EnemyData for id: " + str(ship_id))
            
        self.ship_entity = myglobals.game_map.get_me().get_ship(ship_id)
        self.id = ship_id

        #this is only run @ instantiation; too much shit is in here
        #self.x2 = self.x1
        self.x1 = x
        #self.y2 = self.y1
        self.y1 = y

        self.vector = {"angle": None, "magnitude": None}
        #self.speed = None
        #self.angle = None
        self.target_weight = 0
        #self.turn_number = 0
        
    def update(self, x, y):
        """
        Updates object fields.  Specifically, adds and/or properly rotates x &
        y coordinates, processes data (beginning @ 2nd turn after obtaining
        valid data), and stores the results while valid.
        """
        
        if myglobals.DEBUGGING['method_entry']:
            myglobals.log.debug("EnemyData.update():")
            
        #update coordinates
        #NOTE: change coordinate pairs to associative/tuples (?)
        self.x2 = self.x1
        self.y2 = self.y1
        self.x1 = x
        self.y1 = y
        
        #self.turn_number += 1
        
        #update vector info?
        if not self.x1 == self.x2 and not self.y1 == self.y2:
            #we have enough data to put together vector components
            delta_x = self.x1 - self.x2
            delta_y = self.y1 - self.y2
            
            self.vector = {"angle": atan2(delta_y, delta_x), "magnitude": sqrt((delta_x ** 2) + (delta_y ** 2))}
            #self.speed = sqrt((delta_x ** 2) + (delta_y ** 2))
            #self.angle = atan2(delta_y, delta_x)
            
            if myglobals.DEBUGGING['enemy_data']:
                myglobals.log.debug("Enemy (id #" + str(self.id) + ") speed is " + str(self.vector["magnitude"]) + 
                                    ", angle is " + str(self.vector["angle"]) + " degrees @ (" + str(self.x1) + "," +
                                    str(self.x2) + ")")
        else:
            self.speed = 0
            self.angle = None
    
    def still_alive(self, enemy_list):
        """
        Returns a boolean signifying whether or not the entity represented
        is still active.
        """
        
        if myglobals.DEBUGGING['method_entry']:
            myglobals.log.debug("EnemyData.still_alive():")
            
        for enemy in enemy_list:
            if self.id == enemy.id:
                return True
            
        return False
    
    def determine_probable_target(self):
        """
        Tries (with rudimentary trajectory analysis, at this point) to
        determine the probable target (planet or entity) of this enemy.
        Hopefully, despite how simple this determination is made, it will
        still be valid enough of the time to yield an improvement in 'smart'
        decision making.
        """
        #NOTE: This method should be broken up a little bit more
        
        if myglobals.DEBUGGING['method_entry']:
            myglobals.log.debug("EnemyData.determine_probable_target():")
            
        if self.vector['speed'] == 0:
            #if speed is 0, but docked at a planet, we probably want to keep the target set at the docked planet :P
            #also are we going to have issues here because the speed component of the vector was a double?
            self.probable_target = None
            self.target_weight = 0
            return
        
        hit = False
        for potential_destination in myglobals.game_map.all_planets():
            if hlt.intersect_segment_circle(
                self.ship_entity, potential_destination, {"x": self.x, "y": self.y, 
                                                          "r": potential_destination.radius * myglobals.TARGET_INTERCEPT_FUDGE}):
                if myglobals.DEBUGGING['enemy_data']:
                    myglobals.log.debug("  enemy #" + str(self.id) + "'s trajectory intersects planet #" + 
                                        str(potential_destination.id))
                hit = True
                if self.probable_target == potential_destination and self.target_weight < myglobals.TARGET_WEIGHT_LIMIT:
                    self.target_weight += 1
                elif self.probable_target != potential_destination and self.target_weight > 0:
                    self.target_weight -= 1
                else: #if self.probable_target != potential_destination:
                    self.probable_target = potential_destinion
                    
                #I do believe we'll weight on implementing target weight for a bit here
                break

        if not hit:
            for potential_target in analytics.get_enemy_ships():
                if hlt.intersect_segment_circle(
                    self.ship_entity, potential_target, {"x": self.x, "y": self.y,
                                                         "r": potential_target.radius * myglobals.TARGET_INTERCEPT_FUDGE}):
                    if myglobals.DEBUGGING['enemy_data']:
                        myglobals.log.debug(" enemy #" + str(self.id) + "'s trajectory intersects enemy ship #" +
                                            str(potential_target.id))
                    hit = True
                    if self.probable_target == potential_target and self.target_weight < myglobals.TARGET_WEIGHT_LIMIT:
                        self.target_weight += 1
                    elif self.probable_target != potential_target and self.target_weight > 0:
                        self.target_weight -= 1
                    else:
                        self.probable_target = potential_target
                        
                    break
                
        if not hit:
            for potential_target in bot_routines.myglobals.game_map.get_me().all_ships():
                if hlt.intersect_segment_circle(
                    self.ship_entity, potential_target, {"x": self.x, "y": self.y,
                                                         "r": potential_target.radius * myglobals.TARGET_INTERCEPT_FUDGE}):
                    if myglobals.DEBUGGING['enemy_data']:
                        myglobals.log.debug(" enemy #" + str(self.id) + "'s trajectory intersects friendly ship #" +
                                            str(potential_target.id))
                    hit = True
                    if self.probable_target == potential_target and self.target_weight < myglobals.TARGET_WEIGHT_LIMIT:
                        self.target_weight += 1
                    elif self.probable_target != potential_target and self.target_weight > 0:
                        self.target_weight -= 1
                    else:
                        self.probable_target = potential_target
                        
                    break
                
        if not hit:
            if myglobals.DEBUGGING['enemy_data']:
                myglobals.log.debug(" found no potential target/destination for enemy #" + str(self.id))
            self.probable_target = None
            
        