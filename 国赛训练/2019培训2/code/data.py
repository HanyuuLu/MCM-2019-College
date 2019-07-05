class Data:
    def __init__(self, **kwargs):
        self.chain = \
            {
                'node':\
                    {
                        'M':0.735,
                        'R':0,
                        'H':0.105
                    }
            }
        self.buoy = \
            {
                'node':\
                    {
                        'M':1000,
                        'R':1,
                        'H':2
                    },
                'Buoy':\
                    {

                    }
            }
        self.drums = \
            {
                'node':\
                    {
                        'M':100,
                        'R':0.15,
                        'H':1
                    },
                'Drums':\
                    {
                        'MBall':1200
                    }
            }
        self.pipe = \
            {
                'node':\
                    {
                        'M':1,
                        'R':0.025,
                        'H':1
                    },
                'Drums':\
                    {
                        'MBall':1200
                    }
            }