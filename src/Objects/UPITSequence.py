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

    def run_inverse(self):
        t0 = time.time()
        self.upit = UPIT(self.dataset, self.UPITParam)
        self.upit.run()
        blocks_mined_upit = self.upit.getBlocksMined()
        total_mass = blocks_mined_upit.tonn.sum()
        blocksAvailable = blocks_mined_upit
        count = 0
        mined_ids_set = set()

        while True:
            adjusted_mine_capacity = total_mass - \
                (count + 1) * self.sequenceParam.annualMineCapacity
            adjusted_plant_capacity = total_mass - \
                (count + 1) * self.sequenceParam.annualPlantCapacity
            adjusted_params = Parameters(self.sequenceParam.inclinationLimit,
                                         adjusted_mine_capacity, adjusted_plant_capacity, self.sequenceParam.reach)

            upitInstance = UPIT(Dataset(blocksAvailable), adjusted_params)
            upitInstance.run()
            blocksAvailable = upitInstance.getBlocksMined()
            print(upitInstance.model.objVal)

            iterationSummary = {
                'iteration': count,
                'blocksMined': upitInstance.getBlocksMined(),
                'blocksToPlant': upitInstance.getBlocksToPlant(),
                'objectiveValue': upitInstance.model.objVal
            }
            self.summary.append(iterationSummary)

            total_tonnage = upitInstance.getBlocksMined().tonn.sum()
            count += 1
            if total_tonnage <= self.sequenceParam.annualMineCapacity:
                break

        self.summary = self.summary[::-1]
        self.filter_duplicates()
        self.recalculate_objective_values()

        t1 = time.time()
        print(f"The inverse code took {t1-t0} seconds to run!")

    def filter_duplicates(self):
        all_mined_ids = set()
        all_planted_ids = set()

        for iteration in self.summary:
            current_mined_ids = set(iteration['blocksMined']['id'].values)
            current_planted_ids = set(iteration['blocksToPlant']['id'].values)

            unique_mined_ids = current_mined_ids - all_mined_ids
            unique_planted_ids = current_planted_ids - all_planted_ids

            iteration['blocksMined'] = iteration['blocksMined'][iteration['blocksMined']['id'].isin(
                unique_mined_ids)]
            iteration['blocksToPlant'] = iteration['blocksToPlant'][iteration['blocksToPlant']['id'].isin(
                unique_planted_ids)]

            all_mined_ids.update(unique_mined_ids)
            all_planted_ids.update(unique_planted_ids)

    def recalculate_objective_values(self):
        for iteration in self.summary:
            blocks_mined = iteration['blocksMined']
            blocks_to_plant = iteration['blocksToPlant']
            objective_value = (sum(
                (blocks_to_plant.iloc[i]['profit'] * blocks_to_plant.iloc[i]['tonn'] for i in range(len(blocks_to_plant))))
                - sum((blocks_mined.iloc[i]['tonn'] *
                       0.9 for i in range(len(blocks_mined)))))
            iteration['objectiveValue'] = objective_value
