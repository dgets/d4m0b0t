import hlt

from math import atan2, degrees, sqrt
from . import myglobals

class EnemyData:
    def __init__(self, ship_id, x, y):
        if myglobals.DEBUGGING['enemy_data']:
            myglobals.log.debug("Initializing EnemyData for id: " + ship_id)
            
        self.ship_id = ship_id

        #this is only run @ instantiation; too much shit is in here
        #self.x2 = self.x1
        self.x1 = x
        #self.y2 = self.y1
        self.y1 = y

        speed = None
        angle = None
        
    def new_turn(self, x, y):
        #update coordinates
        #NOTE: change coordinates & speed+angle to associative/tuples
        self.x2 = self.x1
        self.y2 = self.y1
        self.x1 = x
        self.y1 = y
        
        #update vector info?
        if not self.x1 == self.x2 and not self.y1 == self.y2:
            #we have enough data to put together vector components
            delta_x = self.x1 - self.x2
            delta_y = self.y1 - self.y2
            
            self.speed = math.sqrt((delta_x ** 2) + (delta_y ** 2))
            self.angle = math.atan2(delta_y, delta_x)
            
            if myglobals.DEBUGGING['enemy_data']:
                myglobals.log.debug("Enemy (id #" + self.ship_id + ") speed is " + self.speed + ", angle is " + self.angle +
                                    " degrees @ (" + self.x1 + "," + self.x2 + ")")
        else:
            self.speed = 0
            self.angle = None
        