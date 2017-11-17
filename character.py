import cavemap

class Character(object):
    def __init__(self,recordables = []):
        self.recordables = recordables

        # Assign Location, Life, Status, and Inventory
        for jsonFile in self.recordables:
            if jsonFile.name == "inventory":
                self.inventory = jsonFile.data
            if jsonFile.name == "alive":
                self.alive = jsonFile.data
            if jsonFile.name == "status":
                self.status = jsonFile.data
            if jsonFile.name == "location":
                self.location = jsonFile.data
            if jsonFile.name == "relationship":
                self.relationship = jsonFile.data
                self.isPlayer = False

    def move(self, direction, rooms = cavemap.Map()):
        if direction.lower() == "north" and self.rooms[self.x][self.y-1] is not None:
            self.location = self.rooms[self.x][self.y-1]
            self.y -= 1
        if direction.lower() == "south" and self.rooms[self.x][self.y+1] is not None:
            self.location = self.rooms[self.x][self.y+1]
            self.y += 1
        if direction.lower() == "east" and self.rooms[self.x+1][self.y] is not None:
            self.location = self.rooms[self.x+1][self.y]
            self.x = 1
        if direction.lower() == "west" and self.rooms[self.x-1][self.y] is not None:
            self.location = self.rooms[self.x+1][self.y]

    def checkLocation(self):
        """ check to see location has traps """
        return
