import numpy as np
from utils import lin2db

class Settings: 
    """
    Holds configuration parameters for the OFDMA network simulation. Includes cell 
    parameters, bandwidth, noise, shadowing, and interference positions.
    """
    
    def __init__(self, number_subcarriers:int, path_loss_exponent:float, transmition_power:float = 1000, power_allocation_strategy:str = "uniform", 
                 sigma_shadow_fading:float=6, bandwidth:float = 10e6, cell_center:complex = 0, cell_radius:float = 1000, noise_power_spectral_density:float = 1e-20):
        """
        Initialize network settings.

        Args:
            number_subcarriers (int): Total number of subcarriers in the system.
            path_loss_exponent (float): Path loss exponent (e.g., 4 for normal, 5 for urban).
            transmition_power (float, optional): Maximum transmission power of the base station in mW. Defaults to 1000.
            power_allocation_strategy (str, optional): Power allocation method ("uniform" for equal distribution or "inverse_pathloss" 
                for allocation inversely proportional to path loss, giving more power to distant UEs). Defaults to "uniform".
            sigma_shadow_fading (float, optional): Shadowing standard deviation in dB. Defaults to 6.
            bandwidth (float, optional): Total system bandwidth in Hz. Defaults to 10e6.
            cell_center (complex, optional): Complex coordinate of the cell center. Defaults to 0.
            cell_radius (float, optional): Cell radius in meters. Defaults to 1000.
            noise_power_spectral_density (float, optional): Noise power spectral density in W/Hz. Defaults to 1e-20.
        """
        self.total_bandwidth = bandwidth
        self.cell_center = cell_center
        self.cell_radius = cell_radius
        self.max_transmition_power_mW = transmition_power
        self.number_subcarriers = number_subcarriers
        self.path_loss_exponent = path_loss_exponent
        self.sigma_shadow_fading = sigma_shadow_fading
        self.power_allocation_strategy = power_allocation_strategy
        self.noise_power_spectral_density = noise_power_spectral_density
        self.position_base_station_interference = self.calculate_position_base_station_interference()

    def calculate_distance(self, position:complex, index_bs_inteferente:float = None): 
        """
        Calculate the distance from a UE to the serving or interfering base station.

        Args:
            position (complex): Position of the UE.
            index_bs_inteferente (float, optional): Index of the interfering BS (0–5). If None, distance to serving BS. Defaults to None.

        Returns:
            float: Distance in meters.
        """
        if index_bs_inteferente is None: 
            return abs(self.cell_center - position)

        return abs(self.position_base_station_interference[index_bs_inteferente] - position)
    
    def calculate_position_base_station_interference(self): 
        """
        Calculate the positions of the first-tier interfering base stations (6 neighbors).

        Returns:
            np.ndarray: Position of the 6 interfering BSs.
        """
        positions = []
        for index in range(6): 
            angle = 2 * np.pi * index / 6
            position = self.cell_center + 2*self.cell_radius*(np.cos(angle) + 1j*np.sin(angle)) 
            positions.append(position)
            
        return np.array(positions)
    
    def noise_power_mW(self): 
        """
        Calculate the noise power per subcarrier in mW.

        Returns:
            float: Noise power in mW.
        """
        noise_power = self.noise_power_spectral_density*self.total_bandwidth/self.number_subcarriers
        return noise_power*1000
        