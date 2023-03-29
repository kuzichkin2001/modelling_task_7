from simulation import Simulation


if __name__ == '__main__':
    mu = 2
    lambd = 1

    simulation_time = 10000
    max_queue_size = 4
    max_demands_count = 5

    Simulation.run(mu=mu,
        lambd=lambd,
        simulation_time=simulation_time,
        max_queue_size=max_queue_size,
        max_demands_count=max_demands_count)
