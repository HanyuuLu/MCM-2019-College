class TimeWithOutDate:
    ''' # time class without date
    - Attributes:
        seconds
    - [hanyuu](https://hanyuufurude.github.io)
    '''

    def __init__(self, **kwargs):
        self.seconds = 0
        if 'seconds' in kwargs:
            self.seconds = kwargs['seconds']
        if 'hour' in kwargs:
            self.seconds += 3600 * kwargs['hour']
        if 'minute' in kwargs:
            self.seconds += 60 * kwargs['minute']
        assert self.seconds >= 0, '[ERROR] invaild para'
        self.seconds %= 86400

    def strTime(self):
        return ('%02d:%02d:%02d' %
                (self.seconds / 3600,
                 (self.seconds / 60) % 60,
                 self.seconds % 60)
                )

    def __str__(self):
        return self.strTime()


if __name__ == '__main__':
    time = TimeWithOutDate(seconds=86398)
    print(time.strTime())
    timea = TimeWithOutDate(seconds=8)
    print(timea.strTime())
    print(help(TimeWithOutDate))
