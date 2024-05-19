import gurobipy as gp
from .Precedence import Precedence
import time
import pandas as pd


class UPIT:

    def __init__(self, dataset, parameters):
        t0 = time.time()
        self.dataset = dataset
        self.parameters = parameters
        self.model = gp.Model()

        # To make the model stop running when the increase is less than 10%
        self.model.setParam('MIPGap', 0.1)

        # Variables
        self.mine = [self.model.addVar(vtype='B') for i in dataset.blockId]
        self.plant = [self.model.addVar(vtype='B') for i in dataset.blockId]

        # Capacity constraints if applicable
        if self.parameters.annualMineCapacity:
            self.model.addConstr(gp.quicksum(
                [self.dataset.tonnage[i] * self.mine[i] for i in range(len(self.dataset.dataSet))]) <= self.parameters.annualMineCapacity
            )

        if self.parameters.annualPlantCapacity:
            self.model.addConstr(gp.quicksum(
                [self.dataset.tonnage[i] * self.plant[i] for i in range(len(self.dataset.dataSet))]) <= self.parameters.annualPlantCapacity
            )

        # Initialize Precedence here
        self.precedence = Precedence(
            self.model, self.mine, self.dataset,
            self.parameters.inclinationLimit, self.parameters.reach
        )
        t1 = time.time()
        # print(t1 - t0)

    def run(self):
        t0 = time.time()

        # Optimization objective
        self.model.setObjective(sum(
            (self.plant[i] * self.dataset.profit[i] * self.dataset.tonnage[i]
             - self.mine[i] * 0.9 * self.dataset.tonnage[i])
            for i in range(len(self.dataset.dataSet))
        ), gp.GRB.MAXIMIZE)

        # Precedence constraints
        self.precedence.createPrecedenceConstraints()
        t1 = time.time()
        # print(t1 - t0)

        # Mine-Plant constraints
        for idx, row in self.dataset.dataSet.iterrows():
            self.model.addConstr(self.mine[idx] >= self.plant[idx])

        result = self.model.optimize()
        t2 = time.time()
        # print(t2 - t1)

        return result

    def getBlocksMined(self):
        minedBlocksIds = [self.dataset.blockId[i] for i in range(
            len(self.dataset.blockId)) if self.mine[i].X == 1]
        filteredData = self.dataset.dataSet[self.dataset.dataSet['id'].isin(
            minedBlocksIds)]
        self.blocksMined = pd.DataFrame({
            'id': filteredData['id'].tolist(),
            'x': filteredData['x'].tolist(),
            'y': filteredData['y'].tolist(),
            'z': filteredData['z'].tolist(),
            'tonn': filteredData['tonn'].tolist(),
            'profit': filteredData['profit'].tolist()
        })
        return self.blocksMined

    def getNotMined(self):
        notMinedBlocksIds = [self.dataset.blockId[i] for i in range(
            len(self.dataset.blockId)) if self.mine[i].X == 0]
        filteredData = self.dataset.dataSet[self.dataset.dataSet['id'].isin(
            notMinedBlocksIds)]
        self.notMinedBlocks = pd.DataFrame({
            'id': filteredData['id'].tolist(),
            'x': filteredData['x'].tolist(),
            'y': filteredData['y'].tolist(),
            'z': filteredData['z'].tolist(),
            'tonn': filteredData['tonn'].tolist(),
            'profit': filteredData['profit'].tolist()
        })
        return self.notMinedBlocks

    def getBlocksToPlant(self):
        plantBlocksIds = [self.dataset.blockId[i] for i in range(
            len(self.dataset.blockId)) if self.plant[i].X == 1]
        filteredData = self.dataset.dataSet[self.dataset.dataSet['id'].isin(
            plantBlocksIds)]
        self.blocksToPlant = pd.DataFrame({
            'id': filteredData['id'].tolist(),
            'x': filteredData['x'].tolist(),
            'y': filteredData['y'].tolist(),
            'z': filteredData['z'].tolist(),
            'tonn': filteredData['tonn'].tolist(),
            'profit': filteredData['profit'].tolist()
        })
        return self.blocksToPlant
