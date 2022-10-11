from scipy import spatial
import numpy as np
# Specifically written scripts for this work
from analog_auto import analog_auto

def select_analogs(training_sample, test_sample, test_stats, n_analogs, n_star, params, **kwargs):
    """Selects a single Milky Way analog from the given catalogs.
 
    Given a set of Milky Way parameters (e.g. Teff, log(g),[Fe/H])
    will select a set of analog stars from a binary tree constructed
    from the parameters using the analog_auto() function.
    
    
    Args:
        training_sample (dataframe): A dataframe containing the parameters where analogs are
            being searched for. It can contain other columns outside of the 
            selection parameters.
        test_sample (dataframe): A dataframe that contains the selection parameters for
            for the sample of interest. It can contain other columns outside of the 
            selection parameters.
        test_stats (dataframe): A dataframe that contains the mean and standard deviation
            for each selection parameter. Each row is a parameter, column 1 the mean, labeled 
            "mean", and column 2 in the standard deviation, labeled "sigma"
        n_analogs (int): The number of analogs to obtain.
        params (array): An array of the parameters from which to select analogs.
        
    Returns:
        An array of indices of a sample of analog stars in the 
        parameter space.
    """
    search_space = np.zeros((training_sample[params].shape[0], training_sample[params].shape[1]))
    for j, i in enumerate(params):
        search_space[:, j] = (training_sample[params[j]].values - test_stats.at["mean", params[j]]) / test_stats.at["sigma", params[j]]
    tree = spatial.cKDTree(search_space)
    analog_idx = []
    dists = []
    while np.size(analog_idx) < n_analogs:
        realization = test_sample[params].copy(deep=True)
        realization.loc["point"] = [np.random.normal(loc=it[0], scale=it[1]) for it in (test_stats.T.values)]
        analog_idx_i, dist_i = analog_auto(tree, test_sample, test_stats, n_star, params, **kwargs)
        if np.isnan(analog_idx_i) == False:
            analog_idx.append(analog_idx_i)
            dists.append(dist_i)
    analog_idx = np.array(analog_idx)
    dists = np.array(dists)
    return analog_idx, #dists
