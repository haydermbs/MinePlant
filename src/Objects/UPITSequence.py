from Objects.Dataset import Dataset
from Objects.Parameters import Parameters
from Objects.UPIT import UPIT
import time


class UPITSequence:

    def __init__(self, dataset, parameters):
        self.dataset = dataset
        self.UPITParam = Parameters(
            parameters.inclinationLimit, None, None, parameters.reach)
        self.sequenceParam = parameters
        self.summary = []

    def run(self):
        t0 = time.time()
        self.upit = UPIT(self.dataset, self.UPITParam)
        self.upit.run()
        blocksMined = self.upit.getBlocksMined()
        blocksAvailable = blocksMined
        count = 0
        while True:
            upitInstance = UPIT(Dataset(blocksAvailable), self.sequenceParam)
            upitInstance.run()
            blocksAvailable = upitInstance.getNotMined()

            # Store only relevant data instead of the entire UPIT model
            iterationSummary = {
                'iteration': count,
                'blocksMined': upitInstance.getBlocksMined(),
                'blocksToPlant': upitInstance.getBlocksToPlant(),
                'objectiveValue': upitInstance.model.objVal
            }
            self.summary.append(iterationSummary)

            if count > 1 and (iterationSummary['objectiveValue'] / sum(item['objectiveValue'] for item in self.summary) < 0.01):
                break
            count += 1

        t1 = time.time()
        print(f"The code took {t1-t0} seconds to run!")
        return self.summary
