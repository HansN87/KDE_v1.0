# -*- coding: utf-8 -*-

CFG = {
    'paths': {
        'meerkat_root': '/home/ge56lag/Software/Meerkat/inc',
        'meerkat_lib': '/home/ge56lag/Software/Meerkat/lib/libMeerkat.so',
        #'IC_mc': '/home/ge56lag/Data/diffuse_mc_wBDT.npy',
        'IC_mc': '/home/ge56lag/Data/dataset_8yr_fit_IC86_2012_16_MC_2017_09_29_more_fields.npy',
        'mg_mc': 'data/multi_gaussian.npy'
    },
    'project': {
        # A working directory path to save created files.
        'wd': '.'
    },
    'MC_keys': {
        'ow': 'generator_ow',
        'trueE': 'true_energy', # Used in code.
        'conv': 'conv', # Used in code.
        'astro': 'astro',
        'logEr': 'loge_muex',
        'sigma': 'lgb_sigma_psimu',
        'trueDec': 'true_dec', # Used in code.
        'sigmaOK': 'sigmaok', # Used in code.
        'psi': 'psi_mu'
    }
}
