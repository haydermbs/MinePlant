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

    def run(self):
        t0 = time.time()
        self.upit = UPIT(self.dataset, self.UPITParam)
        self.upit.run()
        blocksMined = self.upit.getBlocksMined()
        blocksAvailable = blocksMined
        self.sequences = {}
        count = 0
        while True:
            self.sequences[count] = UPIT(
                Dataset(blocksAvailable), self.sequenceParam)
            self.sequences[count].run()
            blocksAvailable = self.sequences[count].getNotMined()
            if count > 1:
                if self.sequences[count].model.objVal / sum(upit.model.objVal for upit in self.sequences.values()) < 0.01:
                    break
            count += 1
        t1 = time.time()
        print(f"The code took {t1-t0} seconds to run!")
        return self.sequences
