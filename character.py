import cavemap
class Character(object):
    def __init__(self,recordables = []):
        self.recordables = recordables

        # Assign Location, Life, Status, and Inventory
        for jsonFile in self.recordables:
            if jsonFile.name == "inventory":
                self.inventory = jsonFile.data
                self.inventoryFile = jsonFile
            if jsonFile.name == "alive":
                self.alive = jsonFile.data
                self.aliveFile = jsonFile
                self.playerIsAlive = self.aliveFile.data['alive']
            if jsonFile.name == "status":
                self.status = jsonFile.data
                self.statusFile = jsonFile
            if jsonFile.name == "location":
                self.location = jsonFile.data
                self.locationFile = jsonFile
            if jsonFile.name == "relationship":
                self.relationship = jsonFile.data
                self.relationshipFile = jsonFile
                self.isPlayer = False

    def move(self, direction, mapObject):
        movement = direction.lower()
        if movement in ["north","south","east","west"]:
            if mapObject.move(movement, self.location['location']) is not None:
                self.locationFile.data['location'] = mapObject.move(movement, self.location['location'])
                self.locationFile.write()

                self.checkLocation(mapObject)
                if self.inDangerOf:                         # Check is Not None
                    if 'entry' in self.inDangerOf.keys():
                        status = self.inDangerOf['entry']
                        self.statusFile.data[status] = True
                        self.statusFile.write()
                        self.aliveFile.data['alive'] = False
                        self.aliveFile.write()
                        self.playerIsAlive = False

    def checkLocation(self, mapObject):
        """ check to see location has traps """
        self.inDangerOf = mapObject.getDanger(self.location['location'])
