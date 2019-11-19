"""
New version of evolution.py, which now evolves separate populations rather than one main.

Been thinking a bit about what selection etc actually means. In our implementation, there basically is no selection at
all, since we are using a generational model with a comma strategy. There is an equal number of offspring produced
to the amount of parents, which are all replaced (some offspring are left unmutated, but this is still technically
generational). Thus, no parent selection or survivor selection is enforced in the populations. Selection does come
into play for currently playing genes/phenes, but this is not technically evolutionary selection. The structure
could be changed to have survivor selection, for instance by producing a multitude of offspring and cutting a few
based on selection.

There's a bunch of redundancy in cloning offspring etc and the program works exactly the same without doing this (just
mutating the pop directly). I left it in because maybe in the future, it could be more interesting to generate more
offspring.

todo's
- could look a bit more at evolution strategy. Maybe adjust the parameters of .mutPolynomialBounded so a mutrate of
  1 guarantees mutation? This would be a bit more logical and enable more control.
- Update the evolution strategy to actually use survivor selection! The populations now are completely replaced by
  a similar amount of offspring. Over-producing offspring could generate more 'favourable' combinations prior to
  currently playing-selection.

- COULD experiment with 'demes', DEAP's preferred way of implementing multiple populations... but not required.
"""

from deap import base
from deap import creator
from deap import tools
from genetics import *
from presets import *
from fitness import *
import fitness as fit
import pandas as pd
import time
import json
import glob as glob
from itertools import repeat

'''
def evalOneMax(individual):
    x = sum(individual)
    return x,
'''
def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    contents = []
    df = load_genepool(filename)
    for genome in df.values:
        contents.append(list(genome))
    return pcls(ind_init(c) for c in contents)


def evaluation(population, optimum):

    # subset of cols to evaluate
    # calc distance based on subset
    # then score every individual in pop
    subset = ['order']

    opt = optimum.loc[:,subset].values
    pop = population.loc[:,subset].values
    print(opt)

    #opt = [[3]]
    fitnesses = map(toolbox.evaluate, pop, repeat(opt))
    #print(list(fitnesses))
    return fitnesses


# DEAP stuff
creator.create("FitnessMax", base.Fitness, weights=(1.00,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", initIndividual, creator.Individual)
toolbox.register("population", initPopulation, list, toolbox.individual)

toolbox.register("evaluate", distance)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=.9, low=0., up=1., indpb=0.9)
#toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.1, indpb=0.05)
#toolbox.register("select", tools.selNSGA2)
toolbox.register("select", tools.selWorst)



def main():

    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    playing_path = preset_path + 'current/playing.csv'
    phen_cols = [x for x in load_genepool(playing_path).columns]# if x not in ['nature', 'pitch']]
    gen_cols = [x for x in load_genepool(playing_path).columns if x not in ['nature', 'pitch']]

    # Initializing the populations
    files = glob.glob(preset_path + 'current/*.csv')
    try:
        files.remove(f'{preset_path}current/playing.csv')
    except:
        pass

    pops = [toolbox.population(file) for file in files]

    g = 0  # generation counter

    done = False
    while not done:

        g += 1

        mutpb = preset_config['mut_rate']

        next_play = pd.DataFrame(columns=phen_cols)

        print("-- Generation %i --" % g)

        # if pop == ...: # using an if statement, different rules can be programmed for different instruments
        # Optimum is the mean of the phenotype
        optimum = compute_optimum(load_genepool(f'{preset_path}current/playing.csv'), phen_cols)

        for i, pop in enumerate(pops):

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))

            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            for mutant in offspring:
                if random.random() < mutpb[i]:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # fitness assignment for each population // reworked
            offspring_fit = pd.DataFrame(offspring, columns=gen_cols)
            offspring_dict = offspring_fit.to_dict(orient="records")

            pop_offspring = []

            for child in offspring_dict:
                pop_offspring.append(make_phenotype(child, i))

            pop_phenotypes = pd.DataFrame(pop_offspring, columns=phen_cols)

            fitnesses = evaluation(pop_phenotypes, optimum)

            # for some stupid reason, not printing here will mean the code doesn't work (WTF? python 3 issue i think)
            print(list(zip(offspring, fitnesses)))

            for ind, fit in zip(offspring, list(fitnesses)):
                ind.fitness.values = fit

            pop[:] = offspring

            # save new populations to respective csvs
            pop_genes = pd.DataFrame(pop, columns=gen_cols)
            pop_genes.to_csv(files[i])

            # selection for next_play using NSGA2
            best_genes = toolbox.select(pop, preset_config['instr_count'][i])
            best_genes = pd.DataFrame(best_genes, columns=gen_cols)

            # convert next play to phenotype and save as play.csv
            best_phenotypes = gen2phen(best_genes, phen_cols, i)
            next_play = pd.concat([next_play, best_phenotypes])

        # not the prettiest code but it works. Maps playing genes back to a pd.df of phenes
        next_play.to_csv(f'{preset_path}current/playing.csv')

        # updating configs
        preset_path = read_preset_path()
        preset_config = load_config(preset_path)

        time.sleep(preset_config['gen_length'])


if __name__ == '__main__':
    main()
