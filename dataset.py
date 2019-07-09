# -*- coding: utf-8 -*-

from config import CFG
import numpy as np
from numpy.lib import recfunctions as np_rfn
import os.path
import sys

def load_and_prepare_data(pathfilenames):
    """Loads the data and renames fields.
    """
    pathfilenames = [pathfilenames]
    pathfilename = pathfilenames[0]
    assert_file_exists(pathfilename)
    data = np.load(pathfilename)
    for i in range(1, len(pathfilenames)):
        pathfilename = pathfilenames[i]
        assert_file_exists(pathfilename)
        data = np.append(data, np.load(pathfilename))

    # Rename fields based on MC_keys dictionary.
    data = np_rfn.rename_fields(data, CFG['MC_keys'])

    # Apply diffuse dataset cut.
    data = diffuse_cuts(data)

    return data

def diffuse_cuts(mc):
    log_true_e = np.log10(mc['true_energy'])
    return mc[(mc['true_dec'] > np.radians(-5)) &
              (np.log10(mc['true_energy']) < 8.0) &
              (mc['sigmaok'] == 0)]

def assert_file_exists(pathfilename):
    """Checks if the given file exists and raises a RuntimeError if it does
    not exist.
    """
    if(not os.path.isfile(pathfilename)):
        raise RuntimeError('The data file "%s" does not exist!'%(pathfilename))
