import random
import numpy as np
from network import Network
from settings import Settings
from graphic import graphic_cdf
from utils import simulation_monte_carlo
from scheduler import round_robin_allocation, max_sinr_allocation

def analysis_scheduler(settings: Settings, type_allocation:str="round-robin"): 
    """
    Perform a single network simulation to calculate UE capacities.

    Args:
        settings (Settings): Network and system configuration.
        type_allocation (str, optional): Resource allocation method ("round-robin" or "sinr"). Defaults to "round-robin".

    Returns:
        list: List of capacities (in bps) for each UE in the simulation.
    """
    number_ues = random.choice([10, 20, 40, 80])
    network = Network(settings=settings, number_ues=number_ues)
    if type_allocation.lower() == "round-robin": 
        subcarriers_allocation = round_robin_allocation(number_ues=number_ues, number_subcarriers=settings.number_subcarriers)
    else:
        value_sinr = network.calculate_sinr()
        subcarriers_allocation = max_sinr_allocation(value_sinr=value_sinr, number_subcarriers=settings.number_subcarriers)

    return network.calculate_capacity(subcarriers_allocation)

def analysis_per_scheduler(number_subcarriers:int, path_loss_exponent:int, cell_radius:int, verbose:bool=False):
    """
    Run Monte Carlo simulations to analyze capacity performance under different 
    scheduling and power allocation strategies.

    Args:
        number_subcarriers (int): Total number of subcarriers in the system.
        path_loss_exponent (int): Path loss exponent (e.g., 4 for normal, 5 for urban).
        cell_radius (int): Cell radius in meters. Defaults to 1000.
        verbose (bool, optional): If True, prints percentiles (10th, 50th, 90th) for 
            per-UE and total capacity. Defaults to False.

    Returns:
         dict: A nested dictionary with simulation results for each combination of 
              scheduling and power allocation strategies.
              Structure:
                  {
                      "<Scheduler> (<Power Strategy>)": {
                          "total": [list of total capacity values in Mbps],
                          "individual": [list of per-UE capacity values in Mbps]
                      },
                      ...
                  }
                  
    Notes:
        - Schedulers analyzed: Round-Robin and Max-SINR.
        - Power allocation strategies analyzed: Uniform Power and Inverse Pathloss Power.
        - Each simulation runs 1e3 Monte Carlo samples by default.
    """
    output = {}
    schedulers = {"Round-Robin": "round-robin", "Max-SINR": "sinr"}
    power_allocation_strategies: list = {"Uniform Power": "uniform", "Inverse Pathloss Power": "inverse_pathloss"}
    
    for power_strategy_name, power_strategy in power_allocation_strategies.items():
        settings = Settings(number_subcarriers=number_subcarriers, path_loss_exponent=path_loss_exponent,
                            cell_radius=cell_radius, power_allocation_strategy=power_strategy)
    
        for name, sched_type in schedulers.items():
            capacity = simulation_monte_carlo(
                function=analysis_scheduler,
                number_simulation=int(1e3),
                **{'settings': settings, 'type_allocation': sched_type}
            )
            capacity_total = [sum(sublist)/1e6 for sublist in capacity]
            capacity_individual = [item/1e6 for sublist in capacity for item in sublist]
            
            # Save results using key = "Scheduler - PowerStrategy"
            key_name = f"{name} ({power_strategy_name})"
            output[key_name] = {"total": capacity_total, "individual": capacity_individual}

            if verbose:
                print(f"\n=== {name} Scheduler ({power_strategy_name}) ===")
                print(f"Per-UE Capacity (Mbps): 10th={np.percentile(capacity_individual, 10):.2f}, "
                      f"50th={np.percentile(capacity_individual, 50):.2f}, "
                      f"90th={np.percentile(capacity_individual, 90):.2f}")
                print(f"Total Cell Capacity (Mbps): 10th={np.percentile(capacity_total, 10):.2f}, "
                      f"50th={np.percentile(capacity_total, 50):.2f}, "
                      f"90th={np.percentile(capacity_total, 90):.2f}")
    
    return output
        

if __name__ == "__main__":
    
    capacity_round_robin = simulation_monte_carlo(
        function=analysis_scheduler,
        number_simulation=int(1e4),
        **{
            'settings': Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000),
            'type_allocation': "round-robin"
        }
    )
    
    capacity_total_round_robin = [sum(sublist)/1e6 for sublist in capacity_round_robin]
    graphic_cdf(value=capacity_total_round_robin, title_xlabel="Capacity (Mbps)")

    capacity_individual_round_robin = [item/1e6 for sublist in capacity_round_robin for item in sublist]
    graphic_cdf(value=capacity_individual_round_robin, title_xlabel="Capacity (Mbps)")

    capacity_max_sinr = simulation_monte_carlo(
        function=analysis_scheduler,
        number_simulation=int(1e4),
        **{
            'settings': Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000),
            'type_allocation': "sinr"
        }
    )

    capacity_total_max_sinr = [sum(sublist)/1e6 for sublist in capacity_max_sinr]
    graphic_cdf(value=capacity_total_max_sinr, title_xlabel="Capacity (Mbps)")

    capacity_individual_max_sinr = [item/1e6 for sublist in capacity_max_sinr for item in sublist]
    graphic_cdf(value=capacity_individual_max_sinr, title_xlabel="Capacity (Mbps)")