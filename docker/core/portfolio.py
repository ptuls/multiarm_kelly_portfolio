# -*- coding: utf-8 -*-
import numpy as np
from numpy.random import dirichlet


class Portfolio(object):
    def __init__(self, num_sources, initial_wealth, name):
        self.wealth = initial_wealth
        self._success = [0] * num_sources
        self.num_sources = num_sources
        self.allocation = [1.0 / (num_sources + 1)] * (num_sources + 1)
        self.name = name.upper()

    def update(self, win_index):
        self._success[win_index] += 1

    def update_wealth(self, win_index, odds, log):
        safe_wealth = self.wealth * self.allocation[0]
        amount_won = self.wealth * odds[win_index] * self.allocation[win_index + 1]
        net_wealth_change = self.wealth * (self.allocation[0] - 1.0) + amount_won
        net_wealth_change_pct = net_wealth_change / self.wealth * 100.0
        self.wealth = safe_wealth + amount_won
        self.__print_info(safe_wealth, amount_won, net_wealth_change_pct, log)

    def __print_info(self, safe_wealth, amount_won, net_wealth_change_pct, log):
        log.info("------- {0} ----------".format(self.name))
        log.info("Allocation: {0}".format(self.allocation))
        log.info("Safe wealth: {:.2f}".format(safe_wealth))
        log.info("Amount won: {:.2f}".format(amount_won))
        log.info("Net wealth change: {:.2f}%".format(net_wealth_change_pct))


class BayesianUpdatePortfolio(Portfolio):
    def __init__(self, num_sources, initial_wealth):
        super(BayesianUpdatePortfolio, self).__init__(
            num_sources, initial_wealth, "bayesian update"
        )

    def mean_counter(self, index):
        total_sum = sum(self._success) + self.num_sources
        return (self._success[index] + 1.0) / total_sum

    def mean(self):
        return [self.mean_counter(i) for i in range(self.num_sources)]

    def concentration_params(self):
        return self._success + np.ones(self.num_sources)

    # the conjugate prior distribution of a categorical distribution (used to model the horse that wins the race
    # in each round) is a Dirichlet distribution
    def draw(self):
        return dirichlet(self.concentration_params())


class OptimalPortfolio(Portfolio):
    def __init__(self, num_sources, initial_wealth):
        super(OptimalPortfolio, self).__init__(num_sources, initial_wealth, "optimal")


class UniformAllocationPortfolio(Portfolio):
    def __init__(self, num_sources, initial_wealth):
        super(UniformAllocationPortfolio, self).__init__(num_sources, initial_wealth, "uniform")
