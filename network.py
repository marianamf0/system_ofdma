import numpy as np
from settings import Settings
from utils import lin2db, db2pow
from user_equipments import UserEquipments

class Network: 
    
    def __init__(self, settings: Settings, number_ues:int): 
        self.settings = settings
        self.shadow_coefficient = self.generate_shadow_coefficient(number_ues=number_ues)
        self.transmition_power_dbm = self.calculate_transmition_power(number_ues=number_ues)
        self.user_equipaments = UserEquipments(number_ues=number_ues, cell_radius=settings.cell_radius, cell_center=settings.cell_center)

    def calculate_transmition_power(self, number_ues:int):
        return lin2db(self.settings.max_transmition_power_mW/number_ues)*np.ones(number_ues)
        
    def generate_shadow_coefficient(self, number_ues:int): 
        return np.random.normal(0, self.settings.sigma_shadow_fading, size=number_ues)
        
    def path_loss_per_ue(self, index_ue:int, index_bs_inteferente:float=None): 
        distance = self.settings.calculate_distance(
            position=self.user_equipaments.positions[index_ue], index_bs_inteferente=index_bs_inteferente)
        return 130 + 10*self.settings.path_loss_exponent*np.log10(distance/1000) + self.shadow_coefficient[index_ue]
    
    def received_power_per_ue(self, index_ue:int, index_bs_inteferente:float=None): 
        path_loss_per_ue = self.path_loss_per_ue(index_ue=index_ue, index_bs_inteferente=index_bs_inteferente)
        if index_bs_inteferente is None: 
            return self.transmition_power_dbm[index_ue] - path_loss_per_ue
        else:
            return lin2db(self.settings.max_transmition_power_mW) - path_loss_per_ue
    
    def interferente_power_per_ue(self, index_ue:int): 
        interferente_power = 0
        for index_interferente in range(6): 
            interferente_power += db2pow(self.received_power_per_ue(index_ue=index_ue, index_bs_inteferente=index_interferente))
        return interferente_power
    
    def calculate_sinr_per_ue(self, index_ue:int): 
        received_power_mw = db2pow(self.received_power_per_ue(index_ue))         
        interferente_power_mw = self.interferente_power_per_ue(index_ue) 
        noise_power_mw = self.settings.noise_power_mW()                  
        return received_power_mw / (interferente_power_mw + noise_power_mw)

    def calculate_capacity_per_ue(self, index_ue:int, number_subcarriers_per_ue:int=1): 
        sinr = self.calculate_sinr_per_ue(index_ue)
        return number_subcarriers_per_ue*(self.settings.total_bandwidth*np.log2(1+sinr)/self.settings.number_subcarriers)
    
    def calculate_sinr(self):
        value_sinr = [self.calculate_sinr_per_ue(index_ue=index_ue) 
                      for index_ue in range(self.user_equipaments.number_ues)]
        return value_sinr
    
    def calculate_capacity(self, allocation_subcarriers:list=None):
        if allocation_subcarriers is None: 
            allocation_subcarriers = np.ones(self.user_equipaments.number_ues)
        
        value_capacity = []
        for index_ue in range(self.user_equipaments.number_ues): 
            capacity_per_ue = self.calculate_capacity_per_ue(index_ue=index_ue, number_subcarriers_per_ue=allocation_subcarriers[index_ue])
            value_capacity.append(capacity_per_ue)
        
        return value_capacity