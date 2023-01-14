# library imports
import numpy as np

def exp(x,
        a,
        b,
        c):
    return a * np.exp(b * x) + c


def linear(x,
           a,
           b):
    return a * b*x


def log(x,
        a,
        b,
        c):
    return a * np.log(b * x) + c


def inv(x,
        a,
        b,
        c):
    return a + b/(x + c)

# functions
fit_funcs = {"exp": exp, "linear": linear, "log": log, "inv": inv}
fit_string_funcs = {"exp": "{:.3f} * exp({:.3f}x) + {:.3f}",
                    "linear": "{:.3f} + {:.3f}x",
                    "log": "{:.3f} * log(x{:.3f}x) + {:.3f}",
                    "inv": "{:.3f} + {:.3f}/(x + {:.3f})"}
