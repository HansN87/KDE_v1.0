# -*- coding: utf-8 -*-

import numpy as np
import itertools

from config import CFG
from dataset import load_and_prepare_data
from kde_classes import Model, KDE

#from models.example_new import settings, grid
from models.multi_gaussian import settings, grid

#mc = load_and_prepare_data(CFG['paths']['IC_mc'])

mc = np.load(CFG['paths']['mg_mc'])

model = Model(mc, settings)

kde = KDE(model, adaptive=False)

binned_kernel_density = kde.generate_binned_kernel_density()

print(kde.eval_point([0, 0]))


out_bins = []
for key in settings:
    out_bins.append(np.linspace(settings[key]['range'][0],
                                settings[key]['range'][1],
                                settings[key]['nbins']))

print(out_bins)

coords = np.array(list(itertools.product(*out_bins)))

print(coords)

nbins = 100

print('Evaluate KDEs:')
pdf_vals = np.asarray([kde.eval_point(coord) for coord in coords])
shape = np.ones(len(settings.keys()), dtype=int)*nbins
pdf_vals = pdf_vals.reshape(*shape)

print(pdf_vals)



from sklearn.model_selection import KFold
from scipy.interpolate import RegularGridInterpolator

def cross_validate(mc, model):
    kfold = KFold(n_splits=5, random_state=0, shuffle=True)
    lh_arr, zero_arr = [], []

    for train_index, val_index in kfold.split(mc):
        model.update_model(mc[train_index])
        kde = KDE(model, adaptive=False)

        #res_dict = create_KDE(args, mc=self.mc[train_index], bws=bw_dict)
        mc_val = mc[val_index]

        val_settings, grid = model.setup_KDE(mc_val)


        lh, zeros = do_validation(res_dict, val_settings, mc_val['cur_weight'])
        print('Number of zeros {}'.format(zeros))
        print('Likelihood Value {}'.format(lh))
        zero_arr.append(zeros)
        lh_arr.append(lh)
    fname = ''
    for i in range(len(args['bw'])):
        fname += '{}_{}_'.format(args['bw_key'][i], args['bw'][i])
    fname = fname[:-1] + '.npy'
    odict = {'zeros': zero_arr, 'lh': lh_arr}

def do_validation(res_dict, settings, weights):


    #old code:
    bins = [res_dict['bins'][i] for i in range(len(res_dict['bins']))]
    pdf = RegularGridInterpolator(bins, res_dict['pdf_vals'],
                                  method='linear',
                                  bounds_error=False, fill_value=0)
    weights = weights / np.sum(weights)
    mc_arr = [settings[key]['values'] for key in settings.keys()]
    likelihood = pdf(list(zip(*mc_arr)))
    inds = likelihood > 0.
    return np.sum(np.log(likelihood[inds]) * weights[inds]), len(likelihood) - len(inds)
