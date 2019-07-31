# -*- coding: utf-8 -*-

import argparse
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
    parser.add_argument('--bw', nargs='*', type=float, defaul=None)
    args = parser.parse_args()
    return vars(args)

local_draft = """#!/usr/bin/env bash

mkdir -p {working_directory}/output/{model}/{parameters_dir}/pdf

python temp_python_{model}.py

cp /var/tmp/{model}.pkl {working_directory}/output/{model}/{parameters_dir}/pdf

rm /var/tmp/{model}.pkl
rm temp_python_{model}.py
rm temp_local_{model}.sh
"""

slurm_draft = """#!/usr/bin/env bash

#SBATCH --time=3:00:00
#SBATCH --mem=2000
#SBATCH --partition=kta
#SBATCH --error={working_directory}/output/slurm/slurm-%j.err
#SBATCH --output={working_directory}/output/slurm/slurm-%j.out

mkdir -p {working_directory}/output/{model}/{parameters_dir}/pdf

python temp_python_{model}.py

cp /var/tmp/{model}.pkl {working_directory}/output/{model}/{parameters_dir}/pdf

rm /var/tmp/{model}.pkl
rm temp_python_{model}.py
rm temp_slurm_{model}.sub
"""

python_draft = """# -*- coding: utf-8 -*-

import cPickle as pickle
import glob
import itertools
import numpy as np
import os.path

from kde_classes import Model, KDE

model = Model('{model}', mc=None, weighting='{weighting}',
              gamma={gamma}, phi0={phi0})
kde = KDE(model)

if {bw} is None:
    cv_files = glob.glob('output/{model}/{parameters_dir}/cv/cv_*.npy')
    cv_results_split = np.array([], dtype=kde.cv_result_dtype)

    for cv_file in cv_files:
        cv_result_split = np.load(cv_file)
        cv_results_split = np.append(cv_results_split, cv_result_split)

    # Gather splitted cv results by calculating average values.
    arr, unique_index = np.unique(cv_results_split['bandwidth'], return_index=True,
                                  axis=0)
    cv_results = cv_results_split[unique_index]
    for i, cv_result in enumerate(cv_results):
        matches = cv_results_split[np.all(
            cv_results_split['bandwidth'] == cv_result['bandwidth'], axis=1)]
        cv_results['LLH'][i] = np.average(matches['LLH'])
        cv_results['Zeros'][i] = np.average(matches['Zeros'])

    cv_results_max_LLH = cv_results[cv_results['LLH'] == np.max(cv_results['LLH'])]

    bandwidth = cv_results_max_LLH['bandwidth']
else:
    bandwidth = {bw}

if {adaptive}:
    kernel_density = kde.generate_adaptive_kd(bandwidth)
else:
    kernel_density = kde.generate_binned_kd(bandwidth)

pdf_values = kde.get_pdf_values(kernel_density)

result_dict = {{
    'vars': kde.model.vars,
    'bins': kde.model.out_bins,
    'coords': kde.model.coords,
    'pdf_vals': pdf_values,
    'bw': bandwidth
}}

with open(os.path.join('/var/tmp/{model}.pkl'), 'wb') as file:
            pickle.dump(result_dict, file)
"""

# Set model and parameters.
args = parseArguments()
model = args['model']
adaptive = args['adaptive']
weighting = args['weighting']
gamma = args['gamma']
phi0 = args['phi0']
local = args['local']
bw = args['bw']

working_directory = CFG['project']['working_directory']

parameters_dir_format = '{kd}_{weighting}_gamma_{gamma}_phi0_{phi0}'
parameters_dir = parameters_dir_format.format(kd='adaptive_kd' if adaptive else
    'binned_kd', weighting=weighting, gamma=gamma, phi0=phi0)

temp_python_ = 'temp_python_{model}.py'.format(model=model)

with open(temp_python_, "w") as file:
    file.write(python_draft.format(model=model,
                                   weighting=weighting,
                                   gamma=gamma,
                                   phi0=phi0,
                                   adaptive=adaptive,
                                   parameters_dir=parameters_dir
                                   bw=bw))
if local:
    temp_local = 'temp_local_{model}.sh'.format(model=model)
    with open(temp_local, "w") as file:
        file.write(local_draft.format(model=model,
                                      working_directory=working_directory,
                                      parameters_dir=parameters_dir))

    os.system("source ./{}".format(temp_local))
else:
    temp_slurm = 'temp_slurm_{model}.sub'.format(model=model)
    with open(temp_slurm, "w") as file:
        file.write(slurm_draft.format(model=model,
                                      working_directory=working_directory,
                                      parameters_dir=parameters_dir))

    os.system("sbatch {}".format(temp_slurm))
