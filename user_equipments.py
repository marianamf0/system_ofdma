import numpy as np 

class UserEquipments: 
    
    def __init__(self, number_ues:int, cell_radius:float, cell_center:complex):
        self.number_ues = number_ues
        self.positions = self.generate_position(cell_radius, cell_center)

    def generate_position(self, cell_radius:float, cell_center:float): 
        positions = []
        while len(positions) < self.number_ues:
            ray = cell_radius * np.sqrt(np.random.rand())  # raiz para uniformidade na área
            if ray < 150:
                continue
    
            angle = 2 * np.pi * np.random.rand()
            position = ray * np.cos(angle) + cell_center.real + 1j*(ray * np.sin(angle) + cell_center.imag)

            positions.append(position)

        return np.array(positions)

