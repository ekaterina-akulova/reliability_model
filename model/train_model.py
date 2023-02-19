import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def polynomial(df, num_of_predictions):
    X = np.array(df.temp, dtype=float)
    y = np.array(df.temp_mtbf, dtype=float)
    Z = [50, 57, 60,  70]
    coefs = poly.polyfit(X, y, 4)
    X_new = np.linspace(X[0], X[-1] + num_of_predictions, num=len(X) + num_of_predictions)
    ffit = poly.polyval(X_new, coefs)
    pred = poly.polyval(Z, coefs)
    predictions = pd.DataFrame(Z, pred)
    print(predictions)
    plt.plot(X, y, 'ro', label="Original data")
    plt.plot(X_new, ffit, label="Fitted data")
    plt.legend(loc='upper left')
    plt.show()

