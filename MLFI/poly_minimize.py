import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def error_poly(C, data):
    err = np.sum((data[:, 1] - np.polyval(C, data[:, 0])) ** 2)
    return err


def fit_poly(data, error_func, degree=3):
    # Initial guess for polynomial model
    c_guess = np.poly1d(np.ones(degree + 1, dtype=np.float32))

    # Plot initial guess
    x = np.linspace(-5, 5, 21)
    plt.plot(x, np.polyval(c_guess, x), 'm--', linewidth=2.0, label='Initial guess')

    result = spo.minimize(error_func, c_guess, args=(data,), method='SLSQP', options={'disp': True})
    return np.poly1d(result.x)
