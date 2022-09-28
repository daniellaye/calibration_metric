import pytest
import pdb 
import numpy as np
np.random.seed(12)

from metric import MAEMetric, MeanErrorAbove, MeanErrorBelow

def test_mse_metric_zero_mae():
    # make top preds evenly spaced probs between 0 and 1
    top_preds = np.linspace(0, 1, 10000)
    is_correct = []
    # produce corrects based on probability at that index
    for i in range(top_preds.shape[0]): 
        p_correct = top_preds[i]
        is_correct.append(np.random.choice([0, 1], p=[1-p_correct, p_correct]))
    is_correct = np.array(is_correct)

    metric = MAEMetric(n_bins=30)
    mae = metric(top_preds, is_correct)
    # should be sufficiently small 
    assert mae < 0.1

def test_mse_metric_high_mae():
    # make top preds evenly spaced probs between 0 and 1
    top_preds = np.linspace(0, 1, 10000)
    is_correct = []
    # produce corrects based on probability at that index
    for i in range(top_preds.shape[0]): 
        p_correct = top_preds[i]
        # make inversely proportional to probability, so MSE should be high
        is_correct.append(np.random.choice([0, 1], p=[p_correct, 1-p_correct]))
    is_correct = np.array(is_correct)

    metric = MAEMetric(n_bins=20)
    mae = metric(top_preds, is_correct)
    # should be sufficiently large
    assert mae > 0.2

def test_mse_metric_above_high_mae():
    # make top preds evenly spaced probs between 0 and 1
    top_preds = np.linspace(0, 1, 10000)
    is_correct = []
    # produce corrects based on probability at that index
    for i in range(top_preds.shape[0]): 
        # make predictions consistently overconfident by dividing probability by 2
        p_correct = top_preds[i] / 2
        is_correct.append(np.random.choice([0, 1], p=[1-p_correct, p_correct]))
    is_correct = np.array(is_correct)

    metric = MeanErrorAbove(n_bins=20)
    me_below = metric(top_preds, is_correct)
    # should be sufficiently small 
    assert me_below > 0.2

def test_mse_metric_below_high_mae():
    # make top preds evenly spaced probs between 0 and 1
    top_preds = np.linspace(0, 1, 10000)
    is_correct = []
    # produce corrects based on probability at that index
    for i in range(top_preds.shape[0]): 
        # make predictions consistently underconfident by inverting probability
        p_correct = 1-top_preds[i] 
        is_correct.append(np.random.choice([0, 1], p=[1-p_correct, p_correct]))
    is_correct = np.array(is_correct)

    metric = MeanErrorAbove(n_bins=20)
    me_below = metric(top_preds, is_correct)
    pdb.set_trace()
    # should be sufficiently small 
    assert me_below > 0.2