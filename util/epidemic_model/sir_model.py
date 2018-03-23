"""
SIR model, set version

@auth:  Yu-Hsiang Fu
@date:  2014/10/02
@update: 2018/03/22
"""
# --------------------------------------------------------------------------------
# 1.Import modular
# --------------------------------------------------------------------------------
# import packages
import copy as c
import random as r


# --------------------------------------------------------------------------------
# 2.Define functions
# --------------------------------------------------------------------------------
def convert_susceptible_to_infected(g, susceptible_set, infected_set, rate_infection=0.1):
    current_infected = set()

    for ni in infected_set:
        # for nb in r.shuffle(g.neighbors(ni)):
        for nb in g.neighbors(ni):
            if (r.random() < rate_infection) and (nb in susceptible_set):
                current_infected.add(nb)

    return current_infected


def convert_infected_to_recovered(infected_set, rate_recovery=1):
    if rate_recovery == 1:
        # Case 1: if rate_recovery == 1, then move all I nodes to R state
        return infected_set
    else:
        # Case 2: if move I nodes to R state by rate_recovery
        current_recovered = set()

        for ni in infected_set:
            if r.random() < rate_recovery:
                current_recovered.add(ni)

        return current_recovered


def spreading(g, initial_node, num_time_step=50, rate_infection=0.1, rate_recovery=1):
    # SIR model sets
    S = set(g.nodes())
    I = set()
    R = set()

    # network-spreading simulation
    num_node = c.copy(g.number_of_nodes())
    spreading_result = {}

    for t in range(0, num_time_step + 1):
        if t == 0:
            # Case 1: t == 0, initial nodes to I state
            I = I | set(initial_node)  # I = I + I(t=0)
            S = S - I                  # S = S - I(t=0)
        else:
            # Case 2: t > 0, infect neighbors of I nodes
            # I(t), infected neighbor nodes
            I_t = convert_susceptible_to_infected(g, S, I, rate_infection)

            # R(t), nodes from I state to R state
            R_t = convert_infected_to_recovered(I, rate_recovery)

            # update sets
            R = R | R_t  # R = R + R(t)
            I = I | I_t  # I = I + I(t)
            I = I - R_t  # I = I - R(t)
            S = S - I_t  # S = S - I(t)

        # record current result: p(t) = R(t)/|V| or p(t) = 1 - S(t)/|V|
        # spreading_result[t] = len(R) / num_node
        spreading_result[t] = (1 - (len(S) / num_node))

    return spreading_result
