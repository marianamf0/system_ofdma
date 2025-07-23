import numpy as np 
from network import Network
from settings import Settings

def round_robin_allocation(number_ues:int, number_subcarriers:int):
    """
    Allocate subcarriers equally among UEs using a Round-Robin strategy.

    Args:
        number_ues (int):  Number of UEs in the cell.
        number_subcarriers (int): Total number of subcarriers to allocate.

    Returns:
        list: Number of subcarriers allocated to each UE.
    """
    subcarriers_per_ue = number_subcarriers // number_ues
    subcarriers_allocation = [subcarriers_per_ue] * number_ues
    
    remaining = number_subcarriers % number_ues
    for i in range(remaining):
        subcarriers_allocation[i] += 1
    
    return subcarriers_allocation

def max_sinr_allocation(value_sinr:list, number_subcarriers:int):
    """
    Allocate subcarriers proportionally to the SINR of each UE.
    UEs with higher SINR get more subcarriers.

    Args:
        value_sinr (list): SINR values (linear scale) for each UE
        number_subcarriers (int): Total number of subcarriers to allocate.

    Returns:
        list: Number of subcarriers allocated to each UE.
    """
    subcarriers_allocation = [0]*len(value_sinr)
    sorted_index_ue = np.argsort(-np.array(value_sinr))
    for index_ue in sorted_index_ue:
        subcarriers_per_ue = int((value_sinr[index_ue]/sum(value_sinr))*number_subcarriers)
        if sum(subcarriers_allocation) + subcarriers_per_ue <= number_subcarriers: 
            subcarriers_allocation[index_ue] += subcarriers_per_ue
        else: 
            subcarriers_allocation[index_ue] += number_subcarriers - sum(subcarriers_allocation)
            break
        
    remaining = number_subcarriers - sum(subcarriers_allocation)
    for i in range(remaining):
        index_ue = sorted_index_ue[i % len(sorted_index_ue)]
        subcarriers_allocation[index_ue] += 1
    
    return subcarriers_allocation

