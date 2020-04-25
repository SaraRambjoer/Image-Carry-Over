import scipy.sparse
import numpy
def generate_adjacency_matrix(density, min_val, max_val, width, height):
    """
    :param connectivity: % of nodes a node should be connected to
    :param min_val: minimum connection strength if there is a connection
    :param max_val: maximum connection strength if there is a connection
    :param width: width of transition matrix
    :param height: height of transition matrix
    :return: a randomly generated transition matrix
    """

    # Shamelessly adapted from https://github.com/scipy/scipy/issues/9699
    rng1 = numpy.random.RandomState()
    rng2 = numpy.random.RandomState()

    nnz = int(width * height * width * height * density)

    row = rng1.randint(width * height, size=nnz)
    cols = rng2.randint(width * height, size=nnz)
    data = rng1.rand(nnz)

    return scipy.sparse.coo_matrix((data, (row, cols)), shape=(width * height, width * height)) # sparse matrices are neccesary for computational efficiency


