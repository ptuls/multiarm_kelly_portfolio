#!/usr/bin python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import sys

import numpy as np
from numpy.random import choice

from core.kelly import compute_optimal_allocation
from core.portfolio import ThompsonSamplingPortfolio, OptimalPortfolio
from core.util import cagr
import matplotlib.pyplot as plt

log = logging.getLogger()
log.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def main():
    num_races = 10000

    probabilities = np.array([0.5, 0.1, 0.4])
    odds = np.array([1.3, 7.0, 3.0])

    initial_wealth = 1
    burn_in_period = 100
    thompson_samp_portfolio = ThompsonSamplingPortfolio(len(odds), initial_wealth)
    optimal_portfolio = OptimalPortfolio(len(odds), initial_wealth)

    thompson_samp_portfolio_history = []
    optimal_portfolio_history = []
    total_trials = num_races + burn_in_period
    for trial in range(total_trials):
        log.info('Trial: %d' % (trial + 1))
        thompson_samp_portfolio.allocation = compute_optimal_allocation(
            thompson_samp_portfolio,
            odds,
            np.asarray(thompson_samp_portfolio.draw())
        )
        optimal_portfolio.allocation = compute_optimal_allocation(
            optimal_portfolio,
            odds,
            probabilities
        )

        win_index = simulate(probabilities)
        log.info('Horse %d wins' % win_index)
        thompson_samp_portfolio.update(win_index)
        optimal_portfolio.update(win_index)
        if trial > burn_in_period:
            thompson_samp_portfolio.update_wealth(win_index, odds)
            optimal_portfolio.update_wealth(win_index, odds)

            thompson_samp_portfolio_history.append(thompson_samp_portfolio.wealth)
            optimal_portfolio_history.append(optimal_portfolio.wealth)

    log.info('------------------------------------------------')
    log.info('estimate, true, odds')
    estimates = thompson_samp_portfolio.mean()
    for i, estimate in enumerate(estimates):
        log.info('%i: %f, %f, %f' % (i, estimate, probabilities[i], odds[i]))

    bandit_cagr = cagr(initial_wealth, thompson_samp_portfolio.wealth, num_races)
    optimal_cagr = cagr(initial_wealth, optimal_portfolio.wealth, num_races)
    log.info('Final CAGR (Thompson): {:.2f}%'.format(bandit_cagr))
    log.info('Final CAGR (optimal): {:.2f}%'.format(optimal_cagr))

    plot_wealth(thompson_samp_portfolio_history, optimal_portfolio_history, num_races)


def plot_wealth(thompson_samp_portfolio_history, optimal_portfolio_history, num_races):
    plot_range = np.arange(1, num_races, 1)
    fig, ax = plt.subplots()
    ax.semilogy(plot_range, thompson_samp_portfolio_history, 'b', label='Thompson Samp')
    ax.semilogy(plot_range, optimal_portfolio_history, 'r', label='Optimal')
    plt.xlabel('Race')
    plt.ylabel('Wealth ($)')
    plt.legend(loc='upper left')
    plt.show()


def simulate(probabilities):
    return choice(len(probabilities), p=probabilities)


if __name__ == '__main__':
    main()
