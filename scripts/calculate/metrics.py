import numpy as np
from scipy.stats import spearmanr

def cosine_sim(M0, M1):
    """Calculates the cosine similarity between two matrices

    Args:
        M0 (matrix): original matrix on which the NMF was performed
        M1 (matrix): resulting matrix obtained from the multiplication of the NMF matrices
    """
    M0c = np.concatenate(np.array(M0))
    M1c = np.concatenate(np.array(M1))
    return M1c.dot(M0c) / np.sqrt(M1c.dot(M1c) * M0c.dot(M0c))

def get_evar(M0, M1):
    """Calculates the explained variance metric between two matrices"""
    return 1 - ( np.sum((np.array(M0)-np.array(M1))**2) / np.sum(np.array(M0)**2))

def rss_calc(M0, M1):
    """Calculates the rss metric between two matrices
    """
    return np.sum((np.array(M0)-np.array(M1))**2)

def l2norm_calc(M0, M1):
    """Calculates the l2 norm metric between two matrices
    """
    return np.sqrt(np.sum((np.array(M0) - np.array(M1))**2))

def bray_curtis_calc(x, y):
    """
    Calculate Bray-Curtis dissimilarity
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    denominator = np.sum(x + y)

    if denominator == 0:
        return 0.0

    min_val = []
    for i in range(len(x)):
        min_val.append(min(x[i], y[i]))

    numerator = 2* np.sum(min_val)

    return 1 - (numerator / denominator)

def spearman_corr(x, y):
    """
    Calculate Spearman rank correlation
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    rho, p_value = spearmanr(x, y)
    return rho, p_value
