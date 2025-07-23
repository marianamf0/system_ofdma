import numpy as np

def db2pow(value_db):
    """
     Convert a value from dB to linear scale.

    Args:
        value_db (float or array-like): Value(s) in dB.

    Returns:
        float or np.ndarray: Value(s) in linear scale.
    """
    return 10 ** (np.array(value_db) / 10)

def lin2db(value_linear): 
    """
    Convert a value from linear scale (power) to dB.

    Args:
        value_linear (float or array-like): Value(s) in linear scale.

    Returns:
        float or np.ndarray: Value(s) in dB.
    """
    return 10*np.log10(value_linear)

def simulation_monte_carlo(function, number_simulation, *args, **kwargs): 
    """
    Perform Monte Carlo simulation by repeatedly executing a function.

    Args:
        function (callable): The function to execute in each simulation iteration.
        number_simulation (int): Number of iterations to run.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        list: List containing the results of each simulation run.
    """
    result = [function(*args, **kwargs) for _ in range(number_simulation)] 
    return result