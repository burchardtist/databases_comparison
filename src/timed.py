from time import time

from setup_logger import setup_logger


class Timed:
    def __init__(self, operation):
        self.operation = operation
        self.logger = setup_logger('performance')

    def __call__(self, gen):
        def wrapper(*args, **kwargs):
            g = gen(*args, **kwargs)
            try:
                while True:
                    start = time()
                    dbsystem = next(g)
                    elapsed = time() - start
                    print("[%s][%s] time: %.3fs\n" % (self.operation, dbsystem, elapsed))
                    self.logger.info("[%s][%s] time: %.3fs" % (self.operation, dbsystem, elapsed))
            except StopIteration:
                return

        return wrapper


