import recordable

class Map:
    def __init__(self, mapRecordable):

        self.file = mapRecordable
        self.data = self.file.load()

    def load(self):
        self.data = self.file.load()

    def move(self, direction, location):
        """ Return the new location when a character moves,
        when provided with room and direction"""
        if location in self.data:
            if direction in self.data[location]:
                newLocation = self.data[location][direction]
                return newLocation
        return None

    def getDanger(self, location):
        """ Return Dangers in a (str)Location """
        if location in self.data:
            if 'danger' in self.data[location]:
                return self.data[location]['danger']
            else:
                return None
