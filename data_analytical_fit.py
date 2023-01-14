# library imports
import os
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# project imports
from consts import *
from fit_functions import *


class DataAnalyticalFit:
    """
    A class responsible to fit data with a pre-set of distributions
    """

    # CONSTS #

    # END - CONSTS #

    def __init__(self):
        pass

    @staticmethod
    def fit_data(data):
        """
        fit data using dists and return answer
        """
        x = list(range(1, 1+len(data)))
        best_r2 = 0
        best_func = ""
        params = None
        for name, func in fit_funcs.items():
            try:
                popt, pcov = curve_fit(func, x, data)
                y_pred = func(x, *popt)
                r2 = r2_score(data, y_pred)
                if r2 > best_r2:
                    best_r2 = r2
                    best_func = name
                    params = popt
            except:
                pass
        return best_func, params, best_r2

