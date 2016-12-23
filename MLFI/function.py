import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def f(x):
    y = (x - 1.5) ** 2 + 5
    print 'X = {}, Y = {}'.format(x, y)
    return y
