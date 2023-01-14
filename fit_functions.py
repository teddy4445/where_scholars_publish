# library imports
import numpy as np


def exp(x,
        a,
        b,
        c):
    return a * np.exp(-1*b * x) + c


def linear(x,
           a,
           b):
    return a + b*x


def inv(x,
        a,
        b,
        c):
    return a + b/(x + c)


def empty(x,
          a):
    return [-1 for _ in range(len(x))]

# functions
fit_funcs = {"exp": exp, "linear": linear, "inv": inv, "": empty}
fit_string_funcs = {"exp": "{:.3f} * exp(-{:.3f}x) + {:.3f}",
                    "linear": "{:.3f} + {:.3f}x",
                    "inv": "{:.3f} + {:.3f}/(x + {:.3f})",
                    "": "error"}
