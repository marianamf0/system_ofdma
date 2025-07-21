import numpy as np

def db2pow(value_db):
    return 10 ** (np.array(value_db) / 10)

def lin2db(value_linear): 
    return 10*np.log10(value_linear)

def simulation_monte_carlo(function, number_simulation, *args, **kwargs): 
    result = [function(*args, **kwargs) for _ in range(number_simulation)] 
    return result