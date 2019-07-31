# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict

settings = OrderedDict([
    ('sigma_pull_corrected', {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': np.linspace(0.05, 0.25, 6), #[0.08]
        'nbins': 100,
        'range': None
        }),
    ('dec', {
        'values': "np.sin(mc['dec'])",
        'bandwidth': np.linspace(0.05, 0.6, 6), #[0.04]
        'nbins': 400,
        'range': [np.sin(np.radians(-5)), 1.0]
        }),
    ('log_e', {
        'values': "mc['log_e']",
        'bandwidth': np.linspace(0.05, 0.60, 6), #[0.17]
        'nbins': 100,
        'range': None
        })
])

grid = None
