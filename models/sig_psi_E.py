# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict

settings = OrderedDict([
    ('sigma_pull_corrected', {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': np.linspace(0.05, 0.25, 6), #[0.06]
        'nbins': 100,
        'range': None
        }),
    ('psi_mu', {
        'values': "np.log10(mc['psi_mu'])",
        'bandwidth': np.linspace(0.10, 0.30, 6), #[0.16]
        'nbins': 400,
        'range': None
        }),
    ('log_e', {
        'values': "mc['log_e']",
        'bandwidth': np.linspace(0.10, 0.30, 6), #[0.12]
        'nbins': 100,
        'range': None
        })
])

grid = None
