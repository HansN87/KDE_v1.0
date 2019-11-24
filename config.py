# -*- coding: utf-8 -*-

from functions import (
    pl_weighting,
    conv_weighting,
    conv_pl_weighting,
    plotter_wkde_weighting
)

CFG = {
    'debugging': {
        'log_format': ('%(asctime)s %(processName)s %(name)s %(levelname)s: '
            '%(message)s')  # The default log format.
    },
    'paths': {
        'meerkat_root': '/home/ge56lag/Software/Meerkat/inc',
        'meerkat_lib': '/home/ge56lag/Software/Meerkat/lib/libMeerkat.so',
        #'IC_mc': '/home/ge56lag/Data/diffuse_mc_wBDT.npy',
        'IC_mc': '/home/ge56lag/Data/dataset_8yr_fit_IC86_2012_16_MC_2017_09_29_more_fields.npy'
    },
    'project': {
        'NCPU': 4,
        'n_splits': 5,  # Number of folds for cross validation.
        'random_state': 0,  # Seed used by the random number generator.
        'working_directory': '/home/ge56lag/Software/KDE'
    },
    'MC_keys': {
        'ow': 'generator_ow',
        'trueE': 'true_energy',  # Used in code.
        'conv': 'conv',  # Used in code.
        'astro': 'astro',
        #'logEr': 'loge_muex',
        'logE': 'log_e',
        'sigma': 'lgb_sigma_psimu',
        'trueDec': 'true_dec',  # Used in code.
        'sigmaOK': 'sigmaok',  # Used in code.
        'psi': 'psi_mu'
    },
    'weighting_dict': {
        'pl': pl_weighting,
        'conv': conv_weighting,
        'conv+pl': conv_pl_weighting,
        'plotter_wkde': plotter_wkde_weighting
    }
}

CFG_HMN_LOCAL = {
    'debugging': {
        'log_format': ('%(asctime)s %(processName)s %(name)s %(levelname)s: '
            '%(message)s')  # The default log format.
    },
    'paths': {
        'meerkat_root': '/home/hans/software/Meerkat/Meerkat/inc',
        'meerkat_lib': '/home/hans/software/Meerkat/Meerkat/lib/libMeerkat.so', 
        'IC_mc': '/home/hans/icecube/projects/ps_llh/datasets/diffuse_northern_tracks/version-001-p00/dataset_8yr_fit_IC86_2012_16_MC_append.npy'
    },
    'project': {
        'NCPU': 4,
        'n_splits': 5,  # Number of folds for cross validation.
        'random_state': 0,  # Seed used by the random number generator.
        'working_directory': '/home/hans/icecube/projects/ps_llh/kde_new/hans_dev/seed_traditional'
    },
    'MC_keys': {
        'ow': 'orig_OW',
        'trueE': 'trueE',  # Used in code.
        'conv': 'conv',  # Used in code.
        'astro': 'astro',
        #'logEr': 'loge_muex',
        'log_e': 'log_e',
        'sigma': 'log_sigma_pull_corrected',
        'trueDec': 'trueDec',  # Used in code.
        'sigmaOK': 'sigmaOK',  # Used in code.
        'log_psi': 'log_psi'
    },
    'weighting_dict': {
        'pl': pl_weighting,
        'conv': conv_weighting,
        'conv+pl': conv_pl_weighting,
        'plotter_wkde': plotter_wkde_weighting
    }
}

