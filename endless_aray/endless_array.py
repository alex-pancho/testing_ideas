

class EndlessAray():

    def __init__(self):
        self.array = {}
        self.all = None


    def set(self, index, value):
        self.array[index] = value


    def get(self, index):
        """if not exist - None"""
        return self.array.get(index, self.all)


    def set_all(self, value):
        """set all index to val"""
        self.all = value
        for index in self.array:
            self.set(index, value)

if __name__ == "__main__":
    pass
