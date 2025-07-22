import numpy as np
from utils import lin2db

class Settings: 
    
    def __init__(self, number_subcarriers:int, path_loss_exponent:float, transmition_power:float = 1000, sigma_shadow_fading:float=6, bandwidth:float = 10e6, 
                 cell_center:complex = 0, cell_radius:float = 1000, noise_power_spectral_density:float = 1e-20):
        self.total_bandwidth = bandwidth  # em Hz
        self.cell_center = cell_center
        self.cell_radius = cell_radius # em m 
        self.max_transmition_power_mW = transmition_power # em mW
        self.number_subcarriers = number_subcarriers
        self.path_loss_exponent = path_loss_exponent
        self.sigma_shadow_fading = sigma_shadow_fading # em dB
        self.noise_power_spectral_density = noise_power_spectral_density # em W por Hz
        self.position_base_station_interference = self.calculate_position_base_station_interference()

    def calculate_distance(self, position:complex, index_bs_inteferente:float = None): 
        if index_bs_inteferente is None: 
            return abs(self.cell_center - position)

        return abs(self.position_base_station_interference[index_bs_inteferente] - position)
    
    def calculate_position_base_station_interference(self): 
        positions = []
        for index in range(6): 
            angle = 2 * np.pi * index / 6
            position = self.cell_center + 2*self.cell_radius*(np.cos(angle) + 1j*np.sin(angle)) 
            positions.append(position)
            
        return np.array(positions)
    
    
    def noise_power_dbm(self): 
        noise_power = self.noise_power_spectral_density*self.total_bandwidth/self.number_subcarriers
        return lin2db(noise_power) + 30
        