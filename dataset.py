# -*- coding: utf-8 -*-

import numpy as np
from numpy.lib import recfunctions as np_rfn
import os.path

from config import CFG

def load_and_prepare_data(pathfilenames):
    """Loads the data file(s), renames fields and applies diffuse dataset cuts.

    Parameters
    ----------
    pathfilenames : str | sequence of str
        The file name(s), including path(s), of the monte-carlo data file(s).

    Returns
    -------
    data : numpy record ndarray
        Loaded and prepared monte-carlo data.
    """
    if isinstance(pathfilenames, basestring):
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

    # Apply diffuse dataset cuts.
    data = diffuse_cuts(data)

    return data

def diffuse_cuts(mc):
    """Applies diffuse dataset cuts on a given monte-carlo data.

    Parameters
    ----------
    mc : str | numpy record ndarray
        Monte-carlo data.

    Returns
    -------
    mc_dc : numpy record ndarray
        Monte-carlo data after diffuse dataset cuts.
    """
    log_true_e = np.log10(mc['true_energy'])
    mc_dc = mc[(mc['true_dec'] > np.radians(-5)) &
               (np.log10(mc['true_energy']) < 8.0) &
               (mc['sigmaok'] == 0)]
    return mc_dc

def assert_file_exists(pathfilename):
    """Checks if the given file exists.

    Parameters
    ----------
    pathfilenames : str
        The file name, including path.

    Raises
    ------
    RuntimeError
        If the file does not exist.
    """
    if(not os.path.isfile(pathfilename)):
        raise RuntimeError('The data file "%s" does not exist!'%(pathfilename))
