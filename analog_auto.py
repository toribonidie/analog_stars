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
   
    n_params = len(params)
    if not silent:
        print("You have {} parameter input.".format(n_params))

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
