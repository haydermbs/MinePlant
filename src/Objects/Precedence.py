import math


class Precedence:
    def __init__(self, model, mine, dataset, inclinationLimit, reach):
        self.model = model
        self.mine = mine
        self.dataset = dataset
        self.inclinationLimit = inclinationLimit
        self.reach = reach

    def findPointsAboveInclination(self):
        inclinationRadians = math.radians(self.inclinationLimit)
        tanInclination = math.tan(inclinationRadians)
        allPoints = []

        # Generate all points within the cone
        for z in range(1, self.reach + 1):
            horizontalReach = int(math.ceil(tanInclination * z))
            for x in range(-horizontalReach, horizontalReach + 1):
                for y in range(-horizontalReach, horizontalReach + 1):
                    if x == 0 and y == 0:
                        allPoints.append((x, y, z))
                        continue
                    tanAngle = z / math.sqrt(x**2 + y**2)
                    if tanAngle > tanInclination:
                        allPoints.append((x, y, z))

        # Determine surface points by checking for neighbors
        surfacePoints = []
        for point in allPoints:
            x, y, z = point
            # Neighbors in the x and y directions
            neighbors = [(x+dx, y+dy, z) for dx in (-1, 1)
                         for dy in (-1, 1)]
            # If any neighbors are not in allPoints, it is a surface point
            if not all(neighbor in allPoints for neighbor in neighbors):
                surfacePoints.append(point)
        print(allPoints)
        print(surfacePoints)

        return surfacePoints

    def createPrecedenceConstraints(self):
        # Create mining constraints based on the precedence rules. This involves determining
        # which blocks in a mine can be mined given the spatial constraints imposed by
        # the inclination. It ensures safe and efficient mining operations.

        blockDictionary = self.dataset.createBlockLookup()
        restrictions_list = [
            [0, 0, 1], [-1, 0, 1], [0, -1, 1], [0, 1, 1], [1, 0, 1],
            [-2, -2, 3], [-2, 2, 3], [2, -2, 3], [2, 2, 3],
            [4, -3, 5], [-4, 3, 5], [-3, -4, 5], [-3, 4, 5],
            [3, -4, 5], [3, 4, 5], [4, -3, 5], [4, 3, 5]
        ]
        restraintCone = self.findPointsAboveInclination()
        restraintCone = restrictions_list
        for coord, blockId in blockDictionary.items():
            for point in restraintCone:
                targetX, targetY, targetZ = point[0] + \
                    coord[0], point[1] + coord[1], point[2] + coord[2]
                if (targetX, targetY, targetZ) in blockDictionary:
                    # print(blockId, type(blockId), targetX, type(targetX))
                    self.model.addConstr(
                        self.mine[blockId] >= self.mine[blockDictionary[(targetX, targetY, targetZ)]])
