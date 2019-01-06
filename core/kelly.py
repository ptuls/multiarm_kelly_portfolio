# -*- coding: utf-8 -*-
import logging
import numpy as np
from scipy.optimize import minimize

log = logging.getLogger()


def objective(frac, probs, odds, eps=1e-20):
    return -np.dot(probs, np.log2(frac[0] + frac[1:] * odds + eps))


def compute_optimal_allocation(portfolio, odds, probs):
    current_allocation = np.asarray(portfolio.allocation)
    nonnegative_constraints = tuple([(0.0, 1.0) for _ in range(len(current_allocation))])
    optimum = minimize(objective,
                       current_allocation,
                       args=(probs, odds),
                       bounds=nonnegative_constraints,
                       constraints=({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.})
                       )
    return optimum.x, -optimum.fun
