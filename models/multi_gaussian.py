# -*- coding: utf-8 -*-

import numpy as np

settings = {
    'x': {
        'values': "mc['x']",
        'bandwidth': np.linspace(0.1, 1, 10),
        'nbins': 100,
        'range': [-5, 5]
        },
    'y': {
        'values': "mc['y']",
        'bandwidth': [0.3, 0.4, 0.5, 0.6],
        'nbins': 100,
        'range': [-5, 5]
        }
}

#grid = np.linspace(0, 1, 1000)
grid = None
