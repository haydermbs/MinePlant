import pandas as pd


class Dataset:

    def __init__(self, data, columnMap=None, hasHeaders=True, isProfitPerTon=False):
        """
        Initializes the Dataset object with a given data, a column mapping, and a profit type.

        :param data: The input dataset, can be a path to a CSV file or a DataFrame.
        :param columnMap: Optional. A dictionary mapping from column indices to standard names.
        :param hasHeaders: Boolean indicating whether the dataset has headers.
        :param isProfitPerTon: Boolean indicating whether the profit is per ton (True) or per block (False).
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

        # Adjust profit if necessary
        if isProfitPerTon:
            self.adjustProfitPerTon()

        # Create block lookup
        self.blockLookup = self.createBlockLookup()

    def processDataset(self, columnMap):
        """
        Processes the dataset by selecting and renaming columns based on the column map,
        and calculates the profit column if value and cost columns are present.

        :param columnMap: A dictionary mapping from column indices to standard names.
        :return: Processed DataFrame.
        """
        processedData = self.dataSet.iloc[:, list(columnMap.keys())]
        processedData.columns = [columnMap[idx] for idx in columnMap]

        # Check if 'value' and 'cost' columns are present and calculate 'profit'
        if 'value' in processedData.columns and 'cost' in processedData.columns:
            processedData['profit'] = processedData['value'] - \
                processedData['cost']

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

    def adjustProfitPerTon(self):
        """
        Adjusts the profit column if the profit is per ton.
        It multiplies the profit by the tonnage to get the total profit per block.
        """
        if 'profit' in self.dataSet.columns and 'tonn' in self.dataSet.columns:
            self.dataSet['profit'] = self.dataSet['profit'] * \
                self.dataSet['tonn']
