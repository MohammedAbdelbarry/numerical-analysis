import numpy


class Output:
    """
    A data holder class that contains the output of the root finding methods.
    Fields:
    -------
    dataframes: a list of pandas.DataFrame
    roots: a numpy.array of floats
    errors: a numpy.array of floats
    error_bound: a float value
    title: the name of the method used
    function: the function
    boundary_function: the boundary function
    exection_time: a float representing the execution time
    """

    def __init__(self):
        self.dataframes = []
        self.roots = numpy.empty(0, dtype=numpy.float64)
        self.errors = numpy.empty(0, dtype=numpy.float64)
        self.error_bound = 0
        self.title = None
        self.function = None
        self.boundary_function = None
        self.execution_time = 0
