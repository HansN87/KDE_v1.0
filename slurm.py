# -*- coding: utf-8 -*-

import numpy as np
import itertools
import os
import dill as pickle

from config import CFG
from dataset import load_and_prepare_data
from kde_classes import Model, KDE

from models.multi_gaussian import settings, grid

mc = np.load(CFG['paths']['mg_mc'])

model = Model(mc, settings, weighting=None)

kde = KDE(model)

kde_dump_file = open('kde_dump_file', 'wb')
pickle.dump(kde, kde_dump_file, pickle.HIGHEST_PROTOCOL)
kde_dump_file.close()

# slurm_draft = '#!/usr/bin/env bash \n\
# #SBATCH --time=2:30:00 \n\
# #SBATCH --mem=8000 \n\
# #SBATCH --partition=kta \n\
# #SBATCH --error={bpath}/slurm.err \n\
# #SBATCH --output={bpath}/slurm.out \n\
# bash ./env.sh {args}\n'

slurm_draft = """#!/usr/bin/env bash

python temp_python.py

cp "/var/tmp/dict_test_{bw_str}.txt" /home/ge56lag/Software/KDE/output
"""

python_draft = """# -*- coding: utf-8 -*-

import dill as pickle

kde_dump_file = open('kde_dump_file', 'r')
kde = pickle.load(kde_dump_file)
kde_dump_file.close()

result = kde.cross_validate({bandwidth}, {adaptive})

f = open("/var/tmp/dict_test_{bw_str}.txt","w")
f.write(str(result))
f.close()
"""

for bandwidth in itertools.product(*kde.model.bandwidths):
    temp_submit = 'temp_submit.sub'
    python_submit = 'temp_python.py'

    with open(temp_submit, "wc") as file:
        file.write(slurm_draft.format(bw_str=str(bandwidth)))

    adaptive = False
    with open(python_submit, "wc") as file:
        file.write(python_draft.format(bandwidth=bandwidth,
                                       adaptive=adaptive,
                                       bw_str=str(bandwidth)))

    os.system("sbatch {}".format(temp_submit))
