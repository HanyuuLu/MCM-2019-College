class Passenger:
    def __init__(self, loadTime: int):
        self.loadTime = loadTime
        self.waitTime = None


class Taxi:
    def __init__(self, loadTime: int):
        self.loadTime = loadTime
        self.waitTime = None


class NotifyCenter:
    def __init__(self, arriveData, departData):
        self.arriveData = arriveData
        self.departData = departData
