# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice
from core.kelly import compute_optimal_allocation
from core.portfolio import ThompsonSamplingPortfolio, OptimalPortfolio


def plot_wealth(
    thompson_samp_portfolio_history,
    optimal_portfolio_history,
    num_races
):
    plot_range = np.arange(1, num_races, 1)
    fig, ax = plt.subplots()
    ax.semilogy(plot_range, thompson_samp_portfolio_history, 'b', label='Thompson Samp')
    ax.semilogy(plot_range, optimal_portfolio_history, 'r', label='Optimal')
    plt.xlabel('Race')
    plt.ylabel('Wealth ($)')
    plt.legend(loc='upper left')
    plt.figure(figsize=(20, 20))
    plt.show()


def simulate(
    initial_wealth,
    probabilities,
    odds,
    num_races,
    burn_in_period,
    log
):
    thompson_samp_portfolio = ThompsonSamplingPortfolio(len(odds), initial_wealth)
    optimal_portfolio = OptimalPortfolio(len(odds), initial_wealth)

    thompson_samp_portfolio_history = []
    optimal_portfolio_history = []
    total_trials = num_races + burn_in_period
    for trial in range(total_trials):
        log.info('Race: %d' % (trial + 1))
        thompson_samp_portfolio.allocation, thompson_samp_kelly_exponent = compute_optimal_allocation(
            thompson_samp_portfolio,
            odds,
            np.asarray(thompson_samp_portfolio.draw())
        )
        optimal_portfolio.allocation, optimal_kelly_exponent = compute_optimal_allocation(
            optimal_portfolio,
            odds,
            probabilities
        )

        log.info('Thompson sampling Kelly exponent : {:.4f}'.format(thompson_samp_kelly_exponent))
        log.info('Optimal Kelly exponent : {:.4f}'.format(optimal_kelly_exponent))

        win_index = race_result(probabilities)
        log.info('Horse %d wins' % win_index)
        thompson_samp_portfolio.update(win_index)
        optimal_portfolio.update(win_index)

        if trial > burn_in_period:
            thompson_samp_portfolio.update_wealth(win_index, odds, log)
            optimal_portfolio.update_wealth(win_index, odds, log)

            thompson_samp_portfolio_history.append(thompson_samp_portfolio.wealth)
            optimal_portfolio_history.append(optimal_portfolio.wealth)

    log.info('------------------------------------------------')
    log.info('estimate, true, odds')
    estimates = thompson_samp_portfolio.mean()
    for i, estimate in enumerate(estimates):
        log.info('%i: %f, %f, %f' % (i, estimate, probabilities[i], odds[i]))

    return thompson_samp_portfolio_history, optimal_portfolio_history, thompson_samp_portfolio, optimal_portfolio


def race_result(probabilities):
    return choice(len(probabilities), p=probabilities)
