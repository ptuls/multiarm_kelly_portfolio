# -*- coding: utf-8 -*-
from numpy.random import beta


class Counters(object):
    def __init__(self, num_sources):
        self._success = [0] * num_sources
        self._failure = [0] * num_sources
        self.num_sources = num_sources

    def update(self, win, pulled_index):
        if win:
            self._success[pulled_index] += 1
        else:
            self._failure[pulled_index] += 1

    def draw_counter(self, index):
        return beta(self._success[index] + 1, self._failure[index] + 1, 1)

    def draw(self):
        return [self.draw_counter(i) for i in range(self.num_sources)]

    def mean_counter(self, index):
        return (self._success[index] + 1.0) / (self._success[index] + self._failure[index] + 2.0)

    def mean(self):
        return [self.mean_counter(i) for i in range(self.num_sources)]
