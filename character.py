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

    def move(self, direction, mapObject):
        movement = direction.lower()
        if movement in ["north","south","east","west"]:
            self.location['location'] = mapObject.move(movement, self.location['location'])
            for jsonFile in self.recordables:
                if jsonFile.name == "location":
                    jsonFile.data['location'] = self.location['location']
                    jsonFile.write()

    def checkLocation(self):
        """ check to see location has traps """
        return
