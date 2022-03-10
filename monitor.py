

from multiprocessing import Condition, Lock 

class Table():
    def __init__(self, NPHIL, manager):
        self.fforks = manager.list([True for _ in range(NPHIL)])
        self.mutex = Lock()
        self.free_fork = Condition(self.mutex)
        self.current_phil = None
        self.NPHIL = NPHIL

    def set_current_phil(self, phil):
        self.current_phil = phil

    def get_current_phil(self):
        return self.current_phil

    def are_free_fork(self):
        phil = self.current_phil
        return self.fforks[phil] and self.fforks[(phil + 1) % self.NPHIL]

    def wants_eat(self, phil):
        self.mutex.acquire()
        self.free_fork.wait_for(self.are_free_fork)
        self.fforks[phil] = False
        self.fforks[(phil + 1) % self.NPHIL] = False
        self.mutex.release()

    def wants_think(self, phil):
        self.mutex.acquire()
        self.fforks[phil] = True
        self.fforks[(phil + 1) % self.NPHIL] = True
        self.free_fork.notify_all()
        self.mutex.release()
