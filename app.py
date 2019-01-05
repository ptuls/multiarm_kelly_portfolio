#!/usr/bin python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import sys

import numpy as np
from numpy.random import choice
from scipy.optimize import minimize

from core.portfolio import BayesianPortfolio, OptimalPortfolio
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
    num_trials = 2000

    # probabilities = random(10)
    # probabilities /= np.sum(probabilities)
    # odds = random(10) * 10.0

    probabilities = np.array([0.5, 0.1, 0.4])
    odds = np.array([1.3, 10.0, 3.0])

    initial_wealth = 1
    burn_in_period = round(0.3 * num_trials)
    bayesian_portfolio = BayesianPortfolio(len(odds), initial_wealth)
    optimal_portfolio = OptimalPortfolio(len(odds), initial_wealth)

    bayesian_portfolio_history = []
    optimal_portfolio_history = []
    for trial in range(num_trials):
        log.info('Trial: %d' % (trial + 1))
        bayesian_portfolio.allocation = compute_allocation(bayesian_portfolio, odds)
        optimal_portfolio.allocation = compute_optimal_allocation(
            optimal_portfolio,
            odds,
            probabilities
        )

        win_index = simulate(probabilities)
        log.info('Horse %d wins' % win_index)
        bayesian_portfolio.update(win_index)
        optimal_portfolio.update(win_index)
        if trial > burn_in_period:
            bayesian_portfolio.update_wealth(win_index, odds)
            optimal_portfolio.update_wealth(win_index, odds)

            bayesian_portfolio_history.append(bayesian_portfolio.wealth)
            optimal_portfolio_history.append(optimal_portfolio.wealth)

    log.info('-----------------------------')
    log.info('estimate, true, odds')
    estimates = bayesian_portfolio.mean()
    for i, estimate in enumerate(estimates):
        log.info('%i: %f, %f, %f' % (i, estimate, probabilities[i], odds[i]))

    bandit_cagr = cagr(initial_wealth, bayesian_portfolio.wealth, num_trials)
    optimal_cagr = cagr(initial_wealth, optimal_portfolio.wealth, num_trials)
    log.info('Final CAGR: {:.2f}%'.format(bandit_cagr))
    log.info('Final CAGR (optimal): {:.2f}%'.format(optimal_cagr))

    plot_wealth(bayesian_portfolio_history, optimal_portfolio_history, num_trials, burn_in_period)


def plot_wealth(bayesian_portfolio_history, optimal_portfolio_history, num_trials, burn_in_period):
    plot_range = np.arange(1, num_trials - burn_in_period, 1)
    fig, ax = plt.subplots()
    ax.semilogy(plot_range, bayesian_portfolio_history, 'b', label='Bayesian')
    ax.semilogy(plot_range, optimal_portfolio_history, 'r', label='Optimal')
    plt.xlabel('Trial')
    plt.ylabel('Wealth')
    plt.legend(loc='upper left')
    plt.show()


def simulate(probabilities):
    return choice(len(probabilities), p=probabilities)


def objective(frac, probs, odds, eps=1e-20):
    return -np.dot(probs, np.log2(frac[0] + frac[1:] * odds + eps))


def compute_allocation(portfolio, odds):
    estimates = np.asarray(portfolio.draw())
    current_allocation = np.asarray(portfolio.allocation)
    nonnegative = tuple([(0.0, 1.0) for _ in range(len(current_allocation))])
    optimum = minimize(objective,
                       current_allocation,
                       args=(estimates, odds),
                       bounds=nonnegative,
                       constraints=({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.})
                       )
    log.info('Optimal Kelly exponent: {:.4f}'.format(-optimum.fun))
    return optimum.x


def compute_optimal_allocation(portfolio, odds, probs):
    current_allocation = np.asarray(portfolio.allocation)
    nonnegative_constraints = tuple([(0.0, 1.0) for _ in range(len(current_allocation))])
    optimum = minimize(objective,
                       current_allocation,
                       args=(probs, odds),
                       bounds=nonnegative_constraints,
                       constraints=({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.})
                       )
    log.info('Optimal Kelly exponent: {:.4f}'.format(-optimum.fun))
    return optimum.x


if __name__ == '__main__':
    main()
