import json

class Recordable(object):
    """ Constructor Loads Jsonfile of POSIX OS """
    def __init__(self, dirName="saved-game", name="base"):
        self.file = dirName + "/" + name + ".json"
        self.name = name
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text)

    def load(self):
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text)
        return self.data

    def write(self):
        with open(self.file, 'w') as f:
            f.write(json.dumps(self.data, sort_keys=True,
                               indent=4, separators=(',',':')))
            f.close()

    def __repr__(self):
        obj = "The object " + self.name + '\n'
        obj += "Has keys: " + '\n'
        for array_key in self.data.keys():
            obj += array_key + ", "
        return obj
