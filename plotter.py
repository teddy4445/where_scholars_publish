# library imports
import os
import matplotlib.pyplot as plt
from data_analytical_fit import DataAnalyticalFit

# project imports
from consts import *
from fit_functions import *


class Plotter:
    """
    A class responsible to generate plots from data
    """

    # CONSTS #

    # END - CONSTS #

    def __init__(self):
        pass

    @staticmethod
    def hist(data: list,
             x_label: str,
             y_label: str,
             save_path: str,
             normalize: bool = False):
        plt.hist(x=data,
                 density=normalize,
                 color="blue")
        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()

    @staticmethod
    def bar(x: list,
            y: list,
            x_label: str,
            y_label: str,
            save_path: str,
            ylim: tuple = None):
        plt.bar(x=x,
                height=y,
                width=0.8,
                color="blue")
        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        if isinstance(ylim, tuple) and len(ylim) == 2:
            plt.ylim(ylim[0], ylim[1])
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()

    @staticmethod
    def author_journal(x: list,
                       y: list,
                       x_label: str,
                       y_label: str,
                       save_path: str,
                       x_names: list = None,
                       ylim: tuple = None,
                       xlim: tuple = None):
        plt.plot(x,
                 y,
                 "-o",
                 color="blue",
                 label="Data")

        # add the fitting
        best_func, params, best_r2 = DataAnalyticalFit.fit_data(data=y)
        plt.plot(x,
                 fit_funcs[best_func](x, *params),
                 "--",
                 color="black",
                 label="$y = {} | R^2={:.3f}$".format(fit_string_funcs[best_func].format(*params), best_r2))

        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        if isinstance(x_names, list) and len(x_names) == len(x):
            plt.xticks(x, x_names, fontsize=10, rotation=45)
        if isinstance(ylim, tuple) and len(ylim) == 2:
            plt.ylim(ylim[0], ylim[1])
        if isinstance(xlim, tuple) and len(xlim) == 2:
            plt.xlim(xlim[0], xlim[1])
        plt.grid(alpha=0.25,
                 color="black")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
