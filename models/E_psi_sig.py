# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict

settings = OrderedDict([
    ('sigma_pull_corrected', {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': [0.12],
        'nbins': 80,
        'range': None
        }),
    ('psi_mu', {
        'values': "np.log10(mc['psi_mu'])",
        'bandwidth': [0.228],
        'nbins': 400,
        'range': None
        }),
    ('log_e', {
        'values': "mc['log_e']",
        'bandwidth': [0.228],
        'nbins': 80,
        'range': None
        })
])

grid = None
