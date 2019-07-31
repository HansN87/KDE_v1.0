# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict

settings = OrderedDict([
    ('sigma_pull_corrected', {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': np.linspace(0.07, 0.13, 7), #[0.1]
        'nbins': 100,
        'range': None
        }),
    ('log_e', {
        'values': "mc['log_e']",
        'bandwidth': np.linspace(0.14, 0.20, 7), #[0.17]
        'nbins': 100,
        'range': None
        })
])

grid = None
