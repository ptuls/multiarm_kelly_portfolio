# Kelly Allocation with Multi-armed Bandits

Simulating the combination of a solution of the multi-armed bandits problem, Thompson sampling, with the Kelly criterion 
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
In order to estimate the probabilities, we update the probabilities by using Bayesian updating.

## Using the notebook

For convenience, the simulation is packaged into an IPython notebook. To run the notebook, at the
root directory, run
```$xslt
./run.sh
```
