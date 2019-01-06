#!/usr/bin python3
# -*- coding: utf-8 -*-
import logging
import sys
import matplotlib.pyplot as plt
import numpy as np
from core.simulate import simulate


def main(log):
    num_races = 10000

    probabilities = np.array([0.5, 0.1, 0.4])
    odds = np.array([1.3, 7.0, 3.0])

    initial_wealth = 1
    burn_in_period = 100
    thompson_samp_portfolio_history, optimal_portfolio_history, thompson_samp_cgr, optimal_cgr = simulate(
        initial_wealth,
        probabilities,
        odds,
        num_races,
        burn_in_period,
        log
    )

    log.info('Final CGR (Thompson): {:.2f}%'.format(thompson_samp_cgr))
    log.info('Final CGR (optimal): {:.2f}%'.format(optimal_cgr))
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


def create_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


if __name__ == '__main__':
    logger = create_logger()
    main(logger)
