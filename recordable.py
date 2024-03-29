import json
from collections import OrderedDict

class Recordable(object):
    """ Constructor Loads Jsonfile of POSIX OS """
    def __init__(self, dirName="saved-game", name="base"):
        self.file = dirName + "/" + name + ".json"
        self.name = name
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text, object_pairs_hook=OrderedDict)

    def load(self):
        with open(self.file, 'r') as f:
            text = f.read()
            self.data = json.loads(text, object_pairs_hook=OrderedDict)
        return self.data

    def write(self):
        with open(self.file, 'w') as f:
            f.write(json.dumps(self.data, sort_keys=True,
                               indent=4, separators=(',',':')) +'\n')
            f.close()
    def __eq__(self,other):
        return self.data == other.data

    def __ne__(self,other):
        return not self.data == other.data
