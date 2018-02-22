import hlt

class EnemyData:
    def __init__(self, ship_id, x, y):
        self.ship_id = ship_id

        self.x2 = self.x1
        self.x1 = x
        self.y2 = self.y1
        self.y1 = y

        if self.x2 != None:
            #we have enough data to put together vector components
