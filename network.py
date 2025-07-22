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
        power = [self.settings.max_transmition_power_mW/number_ues]*np.ones(number_ues)
        return lin2db(power)
        
    def generate_shadow_coefficient(self, number_ues:int): 
        return np.random.normal(0, self.settings.sigma_shadow_fading, size=number_ues)
        
    def path_loss_per_ue(self, index_ue:int, index_bs_inteferente:float=None): 
        distance = self.settings.calculate_distance(
            position=self.user_equipaments.positions[index_ue], index_bs_inteferente=index_bs_inteferente)
        return 130 + 10*self.settings.path_loss_exponent*np.log10(distance) + self.shadow_coefficient[index_ue]
    
    def received_power_per_ue(self, index_ue:int, index_bs_inteferente:float=None): 
        return self.transmition_power_dbm[index_ue] - self.path_loss_per_ue(index_ue=index_ue, index_bs_inteferente=index_bs_inteferente)
    
    def interferente_power_per_ue(self, index_ue:int): 
        interferente_power = 0
        for index_interferente in range(6): 
            interference = lin2db(self.settings.max_transmition_power_mW) - self.path_loss_per_ue(index_ue=index_ue, index_bs_inteferente=index_interferente)
            interferente_power += db2pow(interference) #db2pow(self.received_power_per_ue(index_ue=index_ue, index_bs_inteferente=index_interferente))
        return lin2db(interferente_power)
    
    def calculate_sinr_per_ue(self, index_ue:int): 
        received_power = self.received_power_per_ue(index_ue)
        interferente_power = self.interferente_power_per_ue(index_ue)
        return received_power - (interferente_power + self.settings.noise_power_dbm())
    
    def calculate_capacity_per_ue(self, index_ue:int, number_subcarriers_per_ue:int=1): 
        sinr = db2pow(self.calculate_sinr_per_ue(index_ue))
        return number_subcarriers_per_ue*(self.settings.total_bandwidth*np.log2(1+sinr)/self.settings.number_subcarriers)
    
    def calculate_sinr(self):
        value_sinr  = []
        for index_ue in range(self.user_equipaments.number_ues): 
            sinr = self.calculate_sinr_per_ue(index_ue=index_ue)
            value_sinr.append(db2pow(sinr))
            
        return value_sinr
    
    def calculate_capacity(self, allocation_subcarriers:list=None):
        if allocation_subcarriers is None: 
            allocation_subcarriers = np.ones(self.user_equipaments.number_ues)
        
        value_capacity = []
        for index_ue in range(self.user_equipaments.number_ues): 
            capacity_per_ue = self.calculate_capacity_per_ue(index_ue=index_ue, number_subcarriers_per_ue=allocation_subcarriers[index_ue])
            value_capacity.append(capacity_per_ue)
        
        return value_capacity