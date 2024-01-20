import pandas as pd


class Dataset:

    def __init__(self, data, columnMap=None, hasHeaders=True):
        """
        Initializes the Dataset object with a given data and a column mapping.

        :param data: The input dataset, can be a path to a CSV file or a DataFrame.
        :param columnMap: Optional. A dictionary mapping from column indices to standard names.
        :param hasHeaders: Boolean indicating whether the dataset has headers.
        """
        # Load dataset
        if isinstance(data, str):
            if hasHeaders:
                self.dataSet = pd.read_csv(data)
            else:
                self.dataSet = pd.read_csv(data, header=None)
        elif isinstance(data, pd.DataFrame):
            self.dataSet = data.copy()
        else:
            raise ValueError(
                "Invalid argument type for Dataset initialization")

        # Process dataset based on column map
        if columnMap is not None:
            self.dataSet = self.processDataset(columnMap)

        # Create block lookup
        self.blockLookup = self.createBlockLookup()

    def processDataset(self, columnMap):
        """
        Processes the dataset by selecting and renaming columns based on the column map.

        :param columnMap: A dictionary mapping from column indices to standard names.
        :return: Processed DataFrame.
        """
        processedData = self.dataSet.iloc[:, list(columnMap.keys())]
        processedData.columns = [columnMap[idx] for idx in columnMap]
        return processedData

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
    def profit(self):
        return self.dataSet['profit'].values

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
