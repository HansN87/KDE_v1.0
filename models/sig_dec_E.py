# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict

settings = OrderedDict([
    ('sigma_pull_corrected', {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': np.linspace(0.05, 0.25, 6),
        'nbins': 100,
        'range': "[np.min(np.log10(mc['sigma_pull_corrected']))-0.5, \
                   np.max(np.log10(mc['sigma_pull_corrected']))+0.5]"
        }),
    ('true_dec', {
        'values': "np.sin(mc['true_dec'])",
        'bandwidth': np.linspace(0.10, 0.60, 6),
        'nbins': 400,
        'range': [np.sin(np.radians(-5)), 1.0]
        }),
    ('log_e', {
        'values': "mc['log_e']",
        'bandwidth': np.linspace(0.10, 0.60, 6),
        'nbins': 100,
        'range': "[np.min(mc['log_e'])-0.5, np.max(mc['log_e'])+0.5]"
        })
])

grid = None
