from network import Network
from settings import Settings
from graphic import graphic_cdf
from utils import simulation_monte_carlo
from scheduler import round_robin_allocation, max_sinr_allocation

def analysis(settings: Settings, number_ues:int, type_allocation:str="round-robin"): 
    network = Network(settings=settings, number_ues=number_ues)
    if type_allocation.lower() == "round-robin": 
        subcarriers_allocation = round_robin_allocation(number_ues=number_ues, number_subcarriers=settings.number_subcarriers)
    else:
        value_sinr = network.calculate_sinr()
        subcarriers_allocation = max_sinr_allocation(value_sinr=value_sinr, number_subcarriers=settings.number_subcarriers)

    return network.calculate_capacity(subcarriers_allocation)

capacity_round_robin = simulation_monte_carlo(
    function=analysis,
    number_simulation=int(1e6),
    **{
        'settings': Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000),
        'number_ues': 10,
        'type_allocation': "round-robin"
    }
)
capacity_round_robin = [item/1e6 for sublist in capacity_round_robin for item in sublist]
graphic_cdf(value=capacity_round_robin, title_xlabel="Capacity (Mbps)")

capacity_max_sinr = simulation_monte_carlo(
    function=analysis,
    number_simulation=int(1e4),
    **{
        'settings': Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000),
        'number_ues': 10,
        'type_allocation': "sinr"
    }
)

capacity_max_sinr = [item/1e6 for sublist in capacity_max_sinr for item in sublist]
graphic_cdf(value=capacity_max_sinr, title_xlabel="Capacity (Mbps)")