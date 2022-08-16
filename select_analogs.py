def select_analogs(training_sample, test_sample, test_stats, n_analogs, n_star, params, **kwargs):
    search_space = np.zeros((training_sample[params].shape[0], training_sample[params].shape[1]))
    for j, i in enumerate(params):
        search_space[:, j] = (training_sample[params[j]].values - test_stats.at["mean", params[j]]) / test_stats.at["sigma", params[j]]
    tree = spatial.cKDTree(search_space)
    analog_idx = []
    dists = []
    while np.size(analog_idx) < n_analogs:
        realization = test_sample[params].copy(deep=True)
        realization.loc["point"] = [np.random.normal(loc=it[0], scale=it[1]) for it in (test_stats.T.values)]
        analog_idx_i, dist_i = analog_auto(tree, realization, test_stats, n_star, params, **kwargs)
        if np.isnan(analog_idx_i) == False:
            analog_idx.append(analog_idx_i)
            dists.append(dist_i)
    analog_idx = np.array(analog_idx)
    dists = np.array(dists)
    return analog_idx, #dists
