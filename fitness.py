"""
File that contains functions to be used in evolution2.py.

For computing the optimum, there are a few approaches to consider:
1. a single optimum generated by computing the mean of playing.csv
2. Preserve all playing.csv info, and compute distance to nearest active phene
3. several optima, one for each instrument nature

So far I only implemented option 1. Option 3 is somewhat appealing.

Distance metric options:
1. Euclidian distance seems most obvious, the norm of the difference vector (sqrt sum of squares)
2. Chebyshev distance might be cool to explore. Distance of vecs is defined as largest distance along any dimension
3. Taxicab is an option, but probably not that clever.

NOTE:
    changes to the gene structure would require a check on the indices in distance(), since I drop based on indices.

    It might be necessary to look at giving an ID to individual genes - it would certainly make it easier to track
    the age of stuff that is playing, and would make debugging and testing a lot more practical to begin with.

todo's:
- clean up redundant stuff (test files, unused imports, unused variables, unused functions)
- sharpen fitness calculation by removing unimportant variables (color, etc.)
- distance metric is very basic, variables are not scaled or weighed in any way.s
"""

from math import *
import numpy as np
from presets import *

preset_path = read_preset_path()
preset_config = load_config(preset_path)


def distance(a, b, method="euclidian"):
    """distance fitness function
    Inputs: two matching numpy arrays
    Output: a fitness value"""

    #a = a.select([:10])
    #b = b.select([:10])

    if method == 'euclidian':
        return sqrt(np.sum((a - b)**2))
    elif method == 'chebyshev':
        return np.max(abs(a - b))
    elif method == 'taxicab':
        return np.sum((a - b))


def compute_optimum(playing, phen_cols, method="mean"):
    """
    Input: a dataframe of playing.csv containing phenes(vars) as rows(cols)
    Output: an optimum of the same dimensionality

    This function should be placed in a loop later to reinitialize the optimum.
    """

    # clean out the variables not used in optimisation (index & instrument nature)
    natures = playing.loc[:, 'nature']  # save the instrument types for the instr_optima method

    # playing.iloc[:,  0] = 0
    playing.loc[:, ['nature','pitch']] = 0
    #playing.loc[:, ['nature']] = 0

    # convert pd to np
    if isinstance(playing, pd.DataFrame):
        playing = playing.values

    # compute a mean value for these that functions as an optimum
    if method == "mean":
        current_optimum = np.mean(playing, axis=0)

    elif method == "bounding_box":
        raise NotImplementedError()

    elif method == "instr_optima":
        raise NotImplementedError()


    df = pd.DataFrame([current_optimum.tolist()], columns=phen_cols)
    return df


def age_check(playing, pops):
    """Function returns either 1 or 0 for each individual in each population, depending on whether it is present in
    the 'playing' dataframe"""
    raise NotImplementedError()
    return ages


def symmetry(playing, pops):
    '''
    symmetry against what is currently playing
    could be implemented using the modulo operator
    '''
    raise NotImplementedError()
    return symmetry

def proportion(playing, pops):
    '''
    proportion of specific subset (i.e. order) to what is currently playing.
    could also be seen as symmetry of this proportion

    '''
    raise NotImplementedError()
    return proportion



