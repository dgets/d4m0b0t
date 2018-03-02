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
        self.coord = {"x": x, "y": y}
        #self.x1 = x
        #self.y1 = y

        self.vector = {"angle": None, "magnitude": None}
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
        self.past_coord = {"x": self.coord["x"], "y": self.coord["y"]}
        #self.x2 = self.x1
        #self.y2 = self.y1
        self.coord = {"x": x, "y": y}
        #self.x1 = x
        #self.y1 = y
        
        #self.turn_number += 1
        
        #update vector info?
        if not self.coord["x"] == self.past_coord["x"] and not self.coord["y"] == self.past_coord["y"]:
            #we have enough data to put together vector components
            delta_x = self.coord["x"] - self.past_coord["x"]
            delta_y = self.coord["y"] - self.past_coord["y"]
            
            self.vector = {"angle": atan2(delta_y, delta_x), "magnitude": sqrt((delta_x ** 2) + (delta_y ** 2))}
            
            if myglobals.DEBUGGING['enemy_data']:
                myglobals.log.debug("Enemy (id #" + str(self.id) + ") speed is " + str(self.vector["magnitude"]) + 
                                    ", angle is " + str(self.vector["angle"]) + " degrees @ (" + str(self.coord["x"]) + "," +
                                    str(self.coord["y"]) + ")")
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
        
        hit = check_group_for_intersect(myglobals.game_map.all_planets())
        if not hit:
            hit = check_group_for_intersect(analytics.get_enemy_ships())
            if not hit:
                hit = check_group_for_intersect(myglobals.game_map.get_me().all_ships())
                
        if not hit:
            if myglobals.DEBUGGING['enemy_data']:
                myglobals.log.debug(" found no potential target/destination for enemy #" + str(self.id))
            
            if self.target_weight > 0:
                self.target_weight -= 1
            
            if self.target_weight == 0:
                self.probable_target = None
            
    def check_group_for_intersect(self, potential_intersect_targets):
        """
        Checks whether or not, within the allowable fudge factor, this enemy's
        vector will cause it to intersect with one of the potential targets
        passed to the method
        
        Returns a boolean value depending on whether or not a potential
        target was found in the values passed or not.
        """
        
        hit = False
        
        for potential_target in potential_intersect_targets:
            if hlt.intersect_segment_circle(
                self.ship_entity, potential_target, {"x": self.coord["x"], "y": self.coord["y"],
                                                         "r": potential_target.radius * myglobals.TARGET_INTERCEPT_FUDGE}):
                if myglobals.DEBUGGING['enemy_data']:
                    myglobals.log.debug(" entity #" + str(self.id) + "'s trajectory intersects entity #" +
                                        str(potential_target.id))
                hit = True
                if self.probable_target == potential_target and self.target_weight < myglobals.TARGET_WEIGHT_LIMIT:
                    self.target_weight += 1
                elif self.probable_target != potential_target and self.target_weight > 0:
                    self.target_weight -= 1
                else:
                    self.probable_target = potential_target
                        
                break
                
        return hit
    