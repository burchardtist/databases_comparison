import re
from pprint import pprint

import ipdb
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


class PerformanceLogger:
    def __init__(self):
        self.performances = list()
        self.lengths = set()
        self.operations = set()
        self.systems = set()
        self.results = dict()

    def load(self):
        with open('logs/performance.log', mode='r') as f:
            for line in f:
                pattern = r'.*\s*-\s*\[(\d+)\]\[([a-z_]+)\]\[([A-Z]+)\]\s+time: ([0-9.]+)s'
                m = re.search(pattern, line)
                if m:
                    self.performances.append(dict(
                        length=m.group(1),
                        operation=m.group(2),
                        system=m.group(3),
                        time=m.group(4)
                    ))
                    self.lengths.add(m.group(1))
                    self.operations.add(m.group(2))
                    self.systems.add(m.group(3))

    def make_results(self):
        for system in self.systems:
            self.results[system] = dict()
            for length in self.lengths:
                self.results[system][length] = dict()
                for operation in self.operations:
                    times = [x['time'] for x in self.performances
                             if x['system'] == system and x['length'] == length and x['operation'] == operation]
                    try:
                        self.results[system][length][operation] = round(sum([float(x) for x in times])/len(times), 5)
                    except ZeroDivisionError:
                        self.results[system][length][operation] = 0.00

    def draw_charts(self):
        for operation in self.operations:
            for length in self.lengths:
                times = [(self.results[system][length][operation], system) for system in self.systems]
                y_pos = np.arange(len(self.systems))
                plt.bar(y_pos, [x[0] for x in times], align='center', alpha=0.5)
                plt.xticks(y_pos, self.systems)
                plt.ylabel('time (s)')
                plt.title('{}, size:{}'.format(operation, length))

                plt.savefig('logs/{}_{}.png'.format(operation, length), bbox_inches='tight')
                plt.close()

    def autolabel(self, rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')


if __name__ == '__main__':
    performance_logger = PerformanceLogger()
    performance_logger.load()
    performance_logger.make_results()
    pprint(performance_logger.results)
    performance_logger.draw_charts()
