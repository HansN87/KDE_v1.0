# -*- coding: utf-8 -*-

import argparse
import importlib
import itertools
import os

from config import CFG

def parseArguments():
    """Parse the command line arguments.

    Returns
    -------
    args : dict
        Dictionary containing the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "model", type=str)
    parser.add_argument(
        "--adaptive", action="store_true", default=False)
    parser.add_argument(
        "--weighting", type=str, default=None)
    parser.add_argument(
        "--gamma", type=float, default=2.0)
    parser.add_argument(
        "--phi0", type=float, default=1.01)
    parser.add_argument(
        "--local", action="store_true", default=False)
    args = parser.parse_args()
    return vars(args)

local_draft = """#!/usr/bin/env bash

mkdir -p {working_directory}/output/{model}/{parameters_dir}/cv

python temp_python_{model}_{i}_{n_split}.py

cp /var/tmp/cv_{i}_{n_split}.npy {working_directory}/output/{model}/{parameters_dir}/cv

rm /var/tmp/cv_{i}_{n_split}.npy
rm temp_python_{model}_{i}_{n_split}.py
rm temp_local_{model}_{i}_{n_split}.sh
"""

slurm_draft = """#!/usr/bin/env bash

#SBATCH --time=3:00:00
#SBATCH --mem=2000
#SBATCH --partition=kta
#SBATCH --error={working_directory}/output/slurm/slurm-%j.err
#SBATCH --output={working_directory}/output/slurm/slurm-%j.out

mkdir -p {working_directory}/output/{model}/{parameters_dir}/cv

python temp_python_{model}_{i}_{n_split}.py

cp /var/tmp/cv_{i}_{n_split}.npy {working_directory}/output/{model}/{parameters_dir}/cv

rm /var/tmp/cv_{i}_{n_split}.npy
rm temp_python_{model}_{i}_{n_split}.py
rm temp_slurm_{model}_{i}_{n_split}.sub
"""

python_draft = """# -*- coding: utf-8 -*-

import numpy as np

from kde_classes import Model, KDE

model = Model('{model}', mc=None, weighting='{weighting}',
              gamma={gamma}, phi0={phi0})
kde = KDE(model)

result = kde.cross_validate_split({bandwidth}, {n_split}, adaptive={adaptive})

np.save("/var/tmp/cv_{i}_{n_split}.npy", result)
"""

# Set model and parameters.
args = parseArguments()
model = args['model']
adaptive = args['adaptive']
weighting = args['weighting']
gamma = args['gamma']
phi0 = args['phi0']
local = args['local']

working_directory = CFG['project']['working_directory']

parameters_dir_format = '{kd}_{weighting}_gamma_{gamma}_phi0_{phi0}'
parameters_dir = parameters_dir_format.format(kd='adaptive_kd' if adaptive else
    'binned_kd', weighting=weighting, gamma=gamma, phi0=phi0)

settings = importlib.import_module('models.{}'.format(model)).settings
bandwidths = [settings[key]['bandwidth'] for key in settings]

for i, bandwidth in enumerate(itertools.product(*bandwidths)):
    for n_split in range(CFG['project']['n_splits']):
        python_submit = 'temp_python_{model}_{i}_{n_split}.py'.format(
            model=model, i=i, n_split=n_split)
        with open(python_submit, "w") as file:
            file.write(python_draft.format(model=model,
                                           weighting=weighting,
                                           gamma=gamma,
                                           phi0=phi0,
                                           bandwidth=bandwidth,
                                           adaptive=adaptive,
                                           i=i,
                                           n_split=n_split))

        if local:
            temp_local = 'temp_local_{model}_{i}_{n_split}.sh'.format(
                model=model, i=i, n_split=n_split)
            with open(temp_local, "w") as file:
                file.write(local_draft.format(model=model, i=i,
                                              working_directory=working_directory,
                                              parameters_dir=parameters_dir,
                                              n_split=n_split))

            os.system("source ./{}".format(temp_local))
        else:
            temp_slurm = 'temp_slurm_{model}_{i}_{n_split}.sub'.format(
                model=model, i=i, n_split=n_split)
            with open(temp_slurm, "w") as file:
                file.write(slurm_draft.format(model=model, i=i,
                                              working_directory=working_directory,
                                              parameters_dir=parameters_dir,
                                              n_split=n_split))

            os.system("sbatch {}".format(temp_slurm))
