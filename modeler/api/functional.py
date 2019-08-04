import numpy as numpy


def scaling(scale):
    """ Get a scaling matrix for an object

    Parameters
    ----------
    scale : list(int, int, int) 
        Factors to scale x, y, and z dims respectively

    Returns
    -------
    scale_matrix : np.ndarray
       Matrix used to scale an object 
    """
    scale_matrix = np.identity(4)
    scale_matrix[0, 0] = scale[0]
    scale_matrix[1, 1] = scale[1]
    scale_matrix[2, 2] = scale[2]
    scale_matrix[3, 3] = 1 
    return scale_matrix