# Kelly Allocation with Multiarm Bandits

Simulating the combination of a solution of the multiarm bandits problem, Thompson sampling, with the Kelly criterion 
for portfolio allocation.

## Brief overview

The [Kelly criterion](http://www.herrold.com/brokerage/kelly.pdf), developed by John L. Kelly Jr. 
at Bell Labs, is an optimal sizing of bets, given an initial pool of wealth, to maximize 
the doubling rate of wealth in a repeated bets scenario. This has been applied to various games, 
including horse racing.

However, the major difficulty in applying the criterion is that it assumes that the true probabilities of 
an event occurring, say for instance, a horse winning a race, is known to the bettor. In reality, 
these probabilities have to be estimated by the bettor. The criterion is sensitive to the estimated probabilities,
and since the criterion maximizes the wealth doubling exponent, mistakes made in the estimated probabilities can
easily ruin the bettor over time.

For concreteness, we cast the problem to the specific problem of betting on horses at a race track.
In order to estimate the probabilities, we use a known solution of the multiarm bandit problem 
called [Thompson sampling](https://www.dropbox.com/s/yhn9prnr5bz0156/1933-thompson.pdf).

## Simulation details

In this simulator, given *k* horses, each horse *i* has a probability of winning *p(i)*. The sum of all probabilties
over all *p(i)*, *i=1, 2, ..., k* is equal to 1. This is no longer equivalent to the classic Beta-Bernoulli scenario
as studied in introductory multiarm bandit literature due to the dependency between the probabilities. Instead, the 
conjugate prior in this scenario is the [Dirichlet distribution](https://en.wikipedia.org/wiki/Dirichlet_distribution).

Each horse has an *odd* associated with it, determining the payout if a bet is place on the horse and the horse wins.
According to the Kelly criterion, a bet is only placed if the probability and the odd exceeds a certain threshold in
a sub-fair odds scenario. Essentially, computation of the Kelly criterion under this scenario results in a 
water-filling algorithm (see Chapter 6 of 
[Elements of Information Theory, 2nd ed.](https://www.wiley.com/en-us/Elements+of+Information+Theory%2C+2nd+Edition-p-9780471241959)).

A *burn-in* period is required to get a reasonably good estimate of the probabilities before betting begins. Typically
about 100 trials are required, but this is subject to more work. A final compound growth rate (CGR) over the total
number of races the bettor has participated is computed. A plot of the growth of the wealth of the bettor under
the Thompson sampling portfolio against the optimal portfolio, i.e., where the bettor has knowledge of the exact
winning probabilities, will be plotted.


