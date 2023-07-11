import numpy as np


# edited generateObjects for hw5
def generateObjects(count, center=0, width=10, massmult=100, vcenter=0, vwidth=10):
    '''Generate a `count` x 5 matrix of (x, y) coordinates corresponding
    to `count` the number of arbitrarly placed elements
    
    Args:
        count (int): the number of (x, y) pairs to generate
        center (float): the center of our distribution
        width (float): the width of our distribution
        massmult (float): mass multiplier
        vcenter (float): the center of our velocity distribution
        vwidth (float): the width of our velocity distribution

    Returns:
        a (`count`, 5) array/list of positions

        The return value should look like:
            [[x1, y1, mass1, velocityx1, velocityy1],
             [x2, y2, mass2, velocityx2, velocityy2],
             ...
            ]
    '''
    coords = np.random.normal(center,width,(count,2))
    mass_values = np.random.ranf(count)*massmult
    vel = np.random.normal(vcenter,vwidth,(count,2))
    return(np.column_stack((coords,mass_values,vel)))


def generateObjectsNormal(count, center=0, width=10, massmult=100):
    ''' Creating a 2-d bell curve of (x,y,mass) matrix '''
    return np.random.multivariate_normal([center, center, massmult],
                                         [[width/2, 0, 0],
                                          [0, width/2, 0],
                                          [0, 0, massmult*10]],
                                         count).tolist()
