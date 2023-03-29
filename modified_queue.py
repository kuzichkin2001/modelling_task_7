from queue import Queue
from demand import Demand


class ModifiedQueue(Queue):
    def __init__(self, maxsize: int = int(1e4)):
        super().__init__(maxsize)

        self.current_size = 0

    def get(self, *args, **kwargs) -> Demand:
        if not self.empty():
            self.current_size -= 1
            return super().get(*args, **kwargs)
        else:
            return None

    def put(self, *args, **kwargs) -> None:
        if self.current_size < self.maxsize:
            self.current_size += 1
            super().put(*args, **kwargs)
