class UUID():
    def __init__(self):
        self.uuid = 0

    def genUUID(self):
        self.uuid += 1
        return self.uuid
