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


def translation(displacement):
    """ Get a translation matrix for an object

    Parameters
    ----------
    displacement : list(int, int, int)
        Factors to displace the x, y, and z dims respectively
    """
    translation_matrix = np.identity(4)
    translation_matrix[0, 3] = displacement[0]
    translation_matrix[1, 3] = displacement[1]
    translation_matrix[2, 3] = displacement[2]
    return translation_matrix