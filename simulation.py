from random import expovariate

from clock import Clock
from configuration import Configuration
from demand import Demand
from statistics import Statistics
from add_settings import AddSettings


class Simulation:
    @classmethod
    def run(cls, mu: float, lambd: float, simulation_time: float, max_queue_size: int, max_demands_count: int) -> None:
        times = Clock()
        settings = AddSettings(max_queue_size=max_queue_size, max_demands_count=max_demands_count)
        system = Configuration(mu, lambd).initialize(mu, lambd, settings)
        statistics = Statistics()

        cls.loop(simulation_time, times, system, statistics)

    @classmethod
    def loop(cls, simulation_time: float,
             times: Clock,
             system: Configuration,
             statistics: Statistics) -> None:
        times.update_arrival_time(system.lambd)
        while times.current <= simulation_time:
            times.current = get_time_of_nearest_event(times)
            if times.current == times.arrival:
                cls.add(times, system)
                continue
            if times.current == times.service_start:
                cls.service(times, system)
                continue
            if times.current == times.leaving:
                cls.remove(times, system, statistics)
                continue
        print()
        print(f"Математическое ожидание длительности пребывания требований в системе обслуживания "
              f"{statistics.average_time / statistics.leaving_count}")
        print(f"Математическое ожидание длительности ожидания требований в очереди системы обслуживания "
              f"{statistics.average_time_awaiting / statistics.leaving_count}")

    @classmethod
    def add(cls, times: Clock,
            system: Configuration) -> None:
        print("* Поступление требования", times.current, end="\t###\t")
        demand = Demand(times.arrival)
        print("номер требования:", demand.id)
        if system.queue.empty() and not system.device.serves:
            times.service_start = times.current
        system.queue.put(demand)
        times.update_arrival_time(system.lambd)

    @classmethod
    def service(cls, times: Clock,
                system: Configuration) -> None:
        print("* Обработка требования", times.current, end="\t###\t")
        times.leaving = times.current + expovariate(system.mu)
        system.device.to_occupy(system.queue.get())
        print("номер требования:", system.device.demand.id)
        system.device.demand.service_start_time = times.current
        times.service_start = float('inf')

    @classmethod
    def remove(cls, times: Clock,
               system: Configuration,
               statistics: Statistics) -> None:
        print("* Удаление требования", times.current, end="\t###\t")
        demand = system.device.get_demand()
        print("номер требования:", demand.id)
        system.device.to_free()
        demand.set_leaving_time(times.current)
        statistics.update(demand)

        if not system.queue.empty():
            times.service_start = times.current
        times.leaving = float('inf')


def get_time_of_nearest_event(times: Clock) -> float:
    return min(times.arrival, times.service_start, times.leaving)
