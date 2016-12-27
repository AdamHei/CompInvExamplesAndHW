import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def error(line, data):
    """
    :param line: Tuple, list, array (C0, C1) where C0 is slope and C1 is y-intercept
    :param data: 2D array where each row is a point (x,y)
    :return: Error as a single real value
    """

    # Sum of squared Y-axis differences
    err = np.sum((data[:, 1] - (line[0] * data[:, 0] + line[1])) ** 2)
    return err


def fit_line(data, error_func):
    """ Fit a line to given data, using a supplied error function

    :param data: 2D array where each row is a point
    :param error_func: function that computes the error between a line and observed data
    :return: Line that minimizes the error function
    """

    l = np.float32([0, np.mean(data[:, 1])])

    x_ends = np.float32([-5, 5])
    plt.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth=2.0, label='Initial guess')

    result = spo.minimize(error_func, l, args=(data,), method='SLSQP', options={'disp': True})
    return result.x


def test_run():
    # Original line
    l_original = np.float32([4, 2])
    print 'Original line: C0: {}, C1 = {}\n'.format(l_original[0], l_original[1])
    x_original = np.linspace(0, 10, 21)
    y_original = l_original[0] * x_original + l_original[1]
    plt.plot(x_original, y_original, 'b', linewidth=2.0, label='Original line')

    # Generate noisy points???
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, y_original.shape)
    data = np.asarray([x_original, y_original + noise]).T
    plt.plot(data[:, 0], data[:, 1], 'go', label='Data points')

    # Try to fit a line to the data
    l_fit = fit_line(data, error)
    print '\nFitted line: C0 = {}, C1 = {}'.format(l_fit[0], l_fit[1])
    plt.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], 'r--', linewidth=2.0, label='Fitted line')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    test_run()
