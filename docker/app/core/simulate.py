# -*- coding: utf-8 -*-
import numpy as np
from kelly import compute_optimal_allocation
from portfolio import ThompsonSamplingPortfolio, OptimalPortfolio
from numpy.random import choice
from util import cgr


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
        log.info('Trial: %d' % (trial + 1))
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
            thompson_samp_portfolio.update_wealth(win_index, odds)
            optimal_portfolio.update_wealth(win_index, odds)

            thompson_samp_portfolio_history.append(thompson_samp_portfolio.wealth)
            optimal_portfolio_history.append(optimal_portfolio.wealth)

    log.info('------------------------------------------------')
    log.info('estimate, true, odds')
    estimates = thompson_samp_portfolio.mean()
    for i, estimate in enumerate(estimates):
        log.info('%i: %f, %f, %f' % (i, estimate, probabilities[i], odds[i]))

    thompson_samp_cgr = cgr(initial_wealth, thompson_samp_portfolio.wealth, num_races)
    optimal_cgr = cgr(initial_wealth, optimal_portfolio.wealth, num_races)

    return thompson_samp_portfolio_history, optimal_portfolio_history, thompson_samp_cgr, optimal_cgr


def race_result(probabilities):
    return choice(len(probabilities), p=probabilities)
