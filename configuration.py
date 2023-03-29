from dataclasses import dataclass
from modified_queue import ModifiedQueue

from device import Device
from add_settings import AddSettings


@dataclass
class Configuration:
    mu: float
    lambd: float
    queue: ModifiedQueue = ModifiedQueue()
    device: Device = Device()

    def initialize(self, mu, lambd, settings: AddSettings):
        self.mu = mu
        self.lambd = lambd
        self.queue = ModifiedQueue(settings.max_queue_size)
        self.device = Device()

        return self
