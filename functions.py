# -*- coding: utf-8 -*-

import os
import importlib
import sys

def powerlaw(Et, phi0=1.01*1e-18, gamma=2.19):
    return phi0 * (Et / 1.e5) ** (-gamma)

def load_model(model_path):
    model_path = os.path.abspath(model_path)
    sys.path.append(os.path.dirname(model_path))
    mname = os.path.splitext(os.path.basename(model_path))[0]
    return importlib.import_module(mname), mname
