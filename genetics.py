import random
import pandas as pd

DATA_PATH = 'data/'

'''
# instruments
synths = ['blade', 'mod_pulse', 'mod_sine', 'pretty_bell']
#synths = ['saw', 'sine', 'pluck']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
#snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
snares = ['drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']

instruments = [synths, low_percs, snares, high_percs, synths, synths, high_percs, synths, bass, bass]
'''



def random_genome():
    """creates a pseudo-random genome"""

    genes = dict(rootnote=random.random(),
                 rootoctave=random.random(),
                 order=random.random(),
                 number=random.random(),
                 bpm=random.random(),
                 total_offset=random.random(),
                 initial_offset=random.random(),
                 red=random.random(), green=random.random(), blue=random.random(),
                 #nature=random.random(),
                 instrument=random.random(),
                 amp=random.random(),
                 cutoff=random.random(),
                 pan=random.random(),
                 attack=random.random(),
                 release=random.random(),
                 mod_range=random.random(),
                 mod_phase=random.random(),
                 mix_reverb=random.random(),
                 mix_echo=random.random()
                 #pitch=random.random()
                 )

    return genes


def make_phenotype(genes, nature):
    """
    Function that maps a genepool to a pool of phenotypes.
    Input: indexed pandas table of genes
    Output: indexed pandas table of phenes
    """
    natures = ['bass', 'high_perc', 'low_perc', 'synth']

    phenotype = dict(rootnote=int(genes['rootnote'] * 12 + 24),
                 rootoctave=int(genes['rootoctave'] * 3 + 3),
                 order=int(genes['order'] * 9 + 3),
                 number=int(genes['number'] * 3 + 1),
                 bpm=int(15*2**int(genes['bpm']*3)),
                 total_offset=(1/8) * int(genes['total_offset'] * 8) * 0.5**int(genes['bpm']*3),
                 initial_offset=(1/8) * int(genes['initial_offset'] * 8) * 1**int(genes['bpm']*3),
                 red=int(genes['red'] * 155 + 100), green=int(genes['green'] * 155 + 100),
                 blue=int(genes['blue'] * 155 + 100),
                 #nature=genes['nature'],#nature=int(genes['nature']*4),
                 instrument=int(genes['instrument']*4),
                 # this is all relevant for a synth
                 amp=round(genes['amp'] * 0.5 + 0.5, 2),
                 cutoff=int(genes['cutoff'] * 30 + 70),
                 pan=round(genes['pan'] - 0.5, 2),
                 attack=round(genes['attack'] / 2, 2),
                 release=round(genes['release'], 2),
                 mod_range=int(genes['mod_range'] * 10 + 2),
                 mod_phase=round(genes['mod_phase'] * .7 + .1, 2),
                 #effect stuff
                 mix_reverb=round(genes['mix_reverb'] * .7 + .3, 2),
                 mix_echo=round(genes['mix_echo'] * .6, 2),
                 # Now the sample related stuff
                 #pitch_change=int(genes['pitch'] * 24 - 12)
                 pitch=int(genes['rootnote'] * 12),
                 nature=natures[nature]
                 )

    return phenotype

def gen2phen(genotypes, phen_cols, i):

    geno_dict = genotypes.to_dict(orient="records")

    phenotypes = []

    for child in geno_dict:
        phenotypes.append(make_phenotype(child, i))

    phenotypes_df = pd.DataFrame(phenotypes, columns=phen_cols)
    return phenotypes_df


def add_genes(df, genes):
    """add genes to genome"""

    df.append(genes, ignore_index=True)

    return df


def make_genepool(size=3, crispr=[dict()]):
    """Create a pool of random genomes"""

    genepool = []

    for i in range(size):
        gen = random_genome()
        genepool.append(gen)

    df = pd.DataFrame(genepool)

    return df


def load_genepool(filename):
    """Load a genepool from a given file"""

    df = pd.read_csv(filename, index_col=0)

    return df


def save_genepool(df, filename='genepool.csv'):
    """save a genepool to a given csv file"""

    df.to_csv(filename)

    return

