import hlt
import math

class EnemyData:
    def __init__(self, ship_id, x, y):
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
        self.x2 = self.x1
        self.y2 = self.y1
        self.x1 = x
        self.y1 = y
        
        #update speed
        if not self.x1 == self.x2 and not self.y1 == self.y2:
            #we have enough data to put together vector components
            delta_x = self.x1 - self.x2
            delta_y = self.y1 - self.y2
            
            self.speed = math.sqrt((delta_x ** 2) + (delta_y ** 2))
        else:
            speed = 0
            
        #update angle
        