import gurobipy as gp
from .Precedence import Precedence
import time


class UPIT:

    def __init__(self, dataset, parameters):
        t0 = time.time()
        self.dataset = dataset
        self.parameters = parameters
        self.model = gp.Model()

        # Variables
        self.mine = [self.model.addVar(vtype='B') for i in dataset.blockId]
        self.plant = [self.model.addVar(vtype='B') for i in dataset.blockId]

        # Initialize Precedence here
        self.precedence = Precedence(
            self.model, self.mine, self.dataset,
            self.parameters.inclinationLimit, self.parameters.reach
        )
        t1 = time.time()
        print(t1-t0)

        # self.precedence = Precedence(
        #     1, 2, 3,
        #     4, 5
        # )

    def run(self):
        t0 = time.time()

        # Optimization objective
        self.model.setObjective(sum(
            (self.plant[i] * self.dataset.profit[i] * self.dataset.tonnage[i]
             - self.mine[i] * 0.9 * self.dataset.tonnage[i])
            for i in self.dataset.blockId), gp.GRB.MAXIMIZE)

        # Precedence constraints
        self.precedence.createPrecedenceConstraints()
        t1 = time.time()
        print(t1-t0)

        # Mine-Plant constraints
        for i in self.dataset.blockId:
            self.model.addConstr(self.mine[i] >= self.plant[i])
        self.model.write("segundo.lp")

        result = self.model.optimize()
        t2 = time.time()
        print(t2-t1)
        return result
