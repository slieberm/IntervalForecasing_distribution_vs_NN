import arch.data.sp500

from arch import arch_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from D_models.SkewStudent import SkewStudent
import config as cfg
import config_models as cfg_mod

horizon_ = cfg.prediction['horizon']
alpha_ = cfg.prediction['alpha']


def run_garch(data_set, m_storage):
    """
    Returns prediction intervals (at given confidence level)
     calculated with GARCH(1,1) with Hansen's skewed t distribution.
     Moreover the inputs which were used for parameter calibration
     and the true value of the predicted interval are returned.
     Parameters lambda and eta are returned.

    Parameters
    ----------
    data_set : DataFrame
        input data set for network training
    m_storage : dict
        dictionary with information of used model, defined in "config_models.py"-file

    Returns
    -------
    m_storage: dict
        intervals, inputs, labels, etas, lambdas added
    """
    length_ = cfg.d_pred['input_len']  # not validated yet

    intervals = np.empty((0, 2), float)
    labels = np.empty((0, 1), float)
    inputs = np.empty((0, cfg.d_pred['input_len'], 1), float)
    eta = list()
    lam = list()
    for i in range(len(data_set)-cfg.data['test_data_size']+cfg.nn_pred['input_len'], len(data_set)):
        train, true = _get_traindata(length_, data_set, i)
        am = arch_model(train, dist="skewt")
        res = am.fit(update_freq=0, disp='off')
        eta.append(res.params['nu'])
        lam.append(res.params['lambda'])
        intervals = np.append(intervals, _get_interval(true, res, print_results=False), axis=0)
        labels = np.append(labels, np.array(true).reshape(1, 1), axis=0)
        inputs = np.append(inputs, np.array(train).reshape(1, cfg.d_pred['input_len'], 1), axis=0)

    # Save in pickles
    # with open('../outputs/intervals/garch_intervals.pickle', 'wb') as f:
    #     pickle.dump([inputs, labels, intervals], f)
    m_storage['intervals'] = intervals
    m_storage['inputs'] = inputs
    m_storage['labels'] = labels
    m_storage['etas'] = eta
    m_storage['lams'] = lam
    return m_storage


def _get_traindata(length, data, true_idx):
    true_val = data[cfg.label][true_idx]
    train_data = data[cfg.label][true_idx-length:true_idx]
    return train_data, true_val


def _get_interval(true_val, fit_res, print_results=False):
    eta, lam = fit_res.params['nu'], fit_res.params['lambda']
    skewt_dist = SkewStudent(eta=eta, lam=lam)
    lb, ub = skewt_dist.ppf(alpha_ / 2), skewt_dist.ppf(1 - alpha_ / 2)
    fcast = fit_res.forecast(horizon=horizon_, reindex=False)
    std_dev = np.sqrt(fcast.variance['h.1'][0])
    interval = np.array([[std_dev * lb, std_dev * ub]])
    if print_results:
        print('True value: ', true_val)
        print(f'Parameter - dof={eta}; lambda={lam}')
        print(f'lower bound quantile = {lb}, upper bound quantile = {ub}')
        print('Standard deviation =', std_dev)
        print(f'Interval: {interval}, width=', interval[1] - interval[0])
    return interval


if __name__ == '__main__':
    # example dataset
    data = arch.data.sp500.load()
    market = pd.DataFrame(data, columns={"Adj Close"})
    market = market.rename(columns={'Adj Close': 'd_glo'})
    returns = market.diff(1).dropna()
    model = cfg_mod.model_garch
    model = run_garch(returns, model)
    # plt.plot(model['etas'])
    plt.plot(model['lams'])
    plt.show()
    print('Hello World')