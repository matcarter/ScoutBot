class Player:
    def __init__(self, name):
        self.name = name
        self.level = "NA"
        self.accountId = "NA"
        self.id = "NA"

    def to_string(self):
        ret = 'Name: ' + self.name + '\n'
        ret += '\tLevel: ' + self.level + '\n'
        ret += '\tAccount ID: ' + self.accountId + '\n'
        ret += '\tID: ' + self.id + '\n'

        return ret
