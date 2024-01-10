class Parameters:
    def __init__(self, inclinationLimit, annualMineCapacity, annualPlantCapacity, reach):
        """
        Initializes the optimization parameters.

        :param inclinationLimit: The maximum allowed inclination angle (in degrees).
        :param annualMineCapacity: The maximum amount of mass that can be extracted per year.
        :param annualPlantCapacity: The maximum amount of mass that can be sent to the plant per year.
        """

        self.inclinationLimit = inclinationLimit
        self.annualMineCapacity = annualMineCapacity
        self.annualPlantCapacity = annualPlantCapacity
        self.reach = reach

    def __str__(self):
        return (f"Parameters("
                f"Inclination Limit: {self.inclinationLimit}°, "
                f"Annual Extraction Capacity: {self.annualMineCapacity}, "
                f"Annual Plant Capacity: {self.annualPlantCapacity}")
