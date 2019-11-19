from genetics import *
from autopilot import *
import json
import os
import glob
import numpy as np

PRESETS_DIR_PATH = 'data/presets/'
MASTER_CONFIG_PATH = 'data/master_'
DEFAULT_CONFIG_DIR_PATH = PRESETS_DIR_PATH + 'default/'


def read_preset_path(master_config_path=MASTER_CONFIG_PATH):
    master_config = load_config(master_config_path)
    return master_config["preset_path"]


def read_scaling_factor(master_config_path=MASTER_CONFIG_PATH):
    master_config = load_config(master_config_path)
    return master_config["scaling_factor"]


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error creating directory: ' + directory)


def create_preset(preset_name, config_path=DEFAULT_CONFIG_DIR_PATH):
    preset_path = 'data/presets/' + preset_name + '/'
    config = load_config(config_path)
    create_data_structure(preset_path, config)
    save_config(preset_path, config)


def load_config(config_path=MASTER_CONFIG_PATH):  # loads .json config file for a preset

    with open(config_path + 'config.json') as f:
        config = json.load(f)

    return config


def save_config(path, config):
    with open(path + 'config.json', 'w') as fp:
        json.dump(config, fp)


def create_data_structure(preset_path, config):
    create_folder(preset_path)
    create_folder(preset_path + 'initial')
    for nature in config['natures']:
        create_initial_genes(preset_path + 'initial/', config, nature)
    create_folder(preset_path + 'current')


def create_initial_genes(preset_path, config, name):
    df = make_genepool(config['pop_size'])  # pull size from config here if needed
    df.to_csv(preset_path + name + '.csv')


def initialize_current(preset_path):
    create_folder(f'{preset_path}current')

    for file in glob.glob(f'{preset_path}initial/*'):
        data = load_genepool(file)
        name = file.split('/')[-1]
        save_genepool(data, f'{preset_path}current/{name}')


def create_random_indices(instr_counts):

    # get configs
    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    result = []

    for count in instr_counts:
        choice = np.random.choice(preset_config['pop_size'], count, replace=False)
        result.append(choice.tolist())

    return result



def select_genes(preset_path, indices=[[0],[0],[0],[0]]):

    phenotypes = []

    files = glob.glob(f'{preset_path}current/*.csv')
    try:
        files.remove(f'{preset_path}current/playing.csv')
    except:
        print()

    for i, index in enumerate(indices):
        if index == []:
            continue
        file = files[i]
        data = load_genepool(file)
        for j in index:
            gene = data.iloc[j,]
            phenotype = make_phenotype(gene, i)
            phenotypes.append(phenotype)

    current_phenotypes = pd.DataFrame(phenotypes)
    current_phenotypes.to_csv(f'{preset_path}current/playing.csv')


def create_preset_from_config_file(config_dict, name):
    '''
    Create complete preset folder from config dict object

    :param config: dictionary containing all config keys and values
    :param name: name for the preset
    :return: preset folder with /initial, initialized /current and config.json
    '''

    new_preset_path = f'{PRESETS_DIR_PATH}{name}/'
    create_folder(new_preset_path)

    # place config.json in folder
    save_config(new_preset_path, config)

    # now create initial folder
    create_folder(f'{new_preset_path}initial')

    natures = ["bass", "high_perc", "low_perc", "synth"]

    for nature in natures:
        # create initial gene pools
        create_initial_genes(f'{new_preset_path}initial/', config_dict, f'{nature}')

    initialize_current(new_preset_path)

    indices = create_random_indices(config_dict['instr_count'])
    select_genes(new_preset_path, indices)



#config ={"mut_rate": [0.5, 0.5, 0.5, 0.5], "pop_size": 100, "gen_length": 1, "bpm_base": 10, "refresh_rate": 8, "instr_count": [1, 1, 1, 1]}
#print(config)
#create_preset_from_config_file(config, "default_100")