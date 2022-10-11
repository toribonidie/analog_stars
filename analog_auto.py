import numpy as np
import sklearn
from sklearn import linear_model
import scipy
from scipy import spatial
import random

def analog_auto(
    tree,
    test_sample,
    test_stats,
    n_star,
    params,
    n_neighbors,
    max_sigma,
    silent=True,
    equal_weight=False,
    delta_cutoff=False,
    **kwargs
):
    """Selects a single analog from the given test_sample.
 
    Given the selection parameters from a star in the test sample, will return the
    single index value of an analogous star randomly selected from the N nearest 
    neighbors in a cKDTree of the given catalogs around a point drawn from 
    the sample's posterior probability distribution. 
  
    Args:
        tree (KDTree/binary tree): A tree created from catalogs being used to 
            find analogs in. Make sure these values are matched in RA and Dec, 
            and the data is scaled approiately. 
            Example:
                tree = spatial.cKDTree(search_space)
        test_sample (dataframe) : A dataframe that contains the selection parameters for
            for the sample of interest. It can contain other columns outside of the 
            selection parameters.
        n_neighbors (int): The number of neighbors to search
            for around the given point.
        max_sigma (int): The maximum number of sigma used to 
            calculate the upper bound distance for the query. Typically between
            5 and 7.
        silent (bool): Default is True, which makes the function not return 
            print functions. If set to False the print statements are output.
        equal_weight (bool): Default is False, so the weighting in the selection 
            of the analogs from the n nearest neighbors depends on how far the
            neighbor is from the search point. If set to True then the 
            weighting is equal/the default of numpy.random.choice()
    Returns:
        An int representing the index of a single test_sample-like star.
    Raises:
        ValueError: If there is only 1 parameter input. The minimum is 2.
    """
   
    n_params = len(params)
    if not silent:
        print("You have {} parameter input.".format(n_params))

    # Find nearest neighbors
    # First we must scale the data correctly
    base_point = np.zeros((n_params))
    columns = list(test_sample[params])
    
    for j, i in enumerate(columns):
        base_point[j] = (test_sample[n_star:n_star+1][params[j]] - test_stats.at["mean", params[j]]) / test_stats.at["sigma", params[j]]
  
    # Find the n_neighbors nearest neighbors
    dist, inds = tree.query(base_point, k=n_neighbors, distance_upper_bound=max_sigma)
    # Randomly select one of the neighbors
    if n_neighbors > 1:
        if equal_weight is False:
            weight = (np.exp(-dist ** 2 / 2)) / np.sum(np.exp(-dist ** 2 / 2))
        else:
            weight = None
        analog_idx = np.random.choice(inds, p=weight)
        wh_dist = np.where(inds == analog_idx)
        dist = dist[wh_dist]
    else:
        analog_idx = inds

    return analog_idx, dist
