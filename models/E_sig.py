# -*- coding: utf-8 -*-

import numpy as np

settings = {
    'logSigma': {
        'values': "np.log10(mc['sigma_pull_corrected'])",
        'bandwidth': [0.08],
        'nbins': 100,
        'range': [0.0, 1.0]
        },
    'logEr': {
        'values': "mc['logE']",
        'bandwidth': [0.15, 0.20],
        'nbins': 100,
        'range': [0, 10]
        }
}

#grid = np.linspace(0, 1, 1000)
grid = None
