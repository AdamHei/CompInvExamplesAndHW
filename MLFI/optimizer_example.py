import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def f(x):
    y = (x - 1.5) ** 2 + 5
    print 'X = {}, Y = {}'.format(x, y)
    return y


def test_run():
    x_guess = 2.0
    min_result = spo.minimize(f, x_guess, method='SLSQP', options={'disp': True})
    print '\nMinima found at:'
    print 'X = {}, Y = {}'.format(min_result.x, min_result.fun)

    x_plot = np.linspace(0.5, 2.5, 21)
    y_plot = f(x_plot)
    plt.plot(x_plot, y_plot)
    plt.plot(min_result.x, min_result.fun, 'ro')
    plt.title('Minima of an objective function')
    plt.show()


if __name__ == '__main__':
    test_run()
