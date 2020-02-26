# from ..model.parts.timestamp import DAYS_PER_TIMESTEP

#simulation configuration parameters
DAYS_PER_TIMESTEP = 1
SIMULATION_TIME_YEARS = 1
SIMULATION_TIME_STEPS = int(SIMULATION_TIME_YEARS * 365 / DAYS_PER_TIMESTEP)
# SIMULATION_TIME_STEPS = 10

MONTE_CARLO_RUNS = 1 # N monte carlo runs