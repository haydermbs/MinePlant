import pandas as pd


class Dataset:

    def __init__(self, *args, **kwargs):
        if args:
            if isinstance(args[0], str):
                # If a string (file path) is provided as an argument
                self.dataSet = pd.read_csv(args[0])
            elif isinstance(args[0], pd.DataFrame):
                # If a DataFrame is provided as an argument
                self.dataSet = args[0]
            else:
                raise ValueError(
                    "Invalid argument type for Dataset initialization")
        elif kwargs:
            # If keyword arguments are provided (assuming these are columns)
            self.dataSet = pd.DataFrame(kwargs)
        else:
            raise ValueError(
                "No arguments provided for Dataset initialization")

        self.blockLookup = self.createBlockLookup()

    @property
    def blockId(self):
        return self.dataSet['id'].values

    @property
    def xCoord(self):
        return self.dataSet['x'].values

    @property
    def yCoord(self):
        return self.dataSet['y'].values

    @property
    def zCoord(self):
        return self.dataSet['z'].values

    @property
    def tonnage(self):
        return self.dataSet['tonn'].values

    @property
    def goldContent(self):
        return self.dataSet['au [ppm]'].values

    @property
    def copperContent(self):
        return self.dataSet['cu %'].values

    @property
    def profit(self):
        return self.dataSet['proc_profit'].values

    @property
    def xAxis(self):
        return list(range(self.dataSet['x'].min(), self.dataSet['x'].max() + 1))

    @property
    def yAxis(self):
        return list(range(self.dataSet['y'].min(), self.dataSet['y'].max() + 1))

    @property
    def zAxis(self):
        return list(range(self.dataSet['z'].min(), self.dataSet['z'].max() + 1))

    def createBlockLookup(self):
        blockLookup = {}
        for idx, row in self.dataSet.iterrows():
            coordinates = (int(row['x']), int(row['y']), int(row['z']))
            blockLookup[coordinates] = int(row['id'])
        return blockLookup

    def getBlockId(self, x, y, z):
        return self.blockLookup.get((int(x), int(y), int(z)), None)
