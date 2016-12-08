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
                if 'indexed' in kwargs and kwargs['indexed']:
                    self.operation = '{}_{}'.format(self.operation, 'indexed')
                else:
                    self.operation = self.operation.replace('_indexed', '')
                    
                while True:
                    start = time()
                    dbsystem, length = next(g)
                    elapsed = time() - start
                    self.logger.info("[%s][%s][%s] time: %.3fs" % (length, self.operation, dbsystem, elapsed))
            except StopIteration:
                return
        return wrapper
