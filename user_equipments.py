import numpy as np 

class UserEquipments:
    """
    Represents a set of User Equipments (UEs) within a cellular network.
    Generates and stores random UE positions within a circular cell.
    """ 
    
    def __init__(self, number_ues:int, cell_radius:float, cell_center:complex):
        """
        Initialize the UserEquipments class.

        Args:
            number_ues (int): Number of user equipments in the cell.
            cell_radius (float): Cell radius in meters.
            cell_center (complex): Position of the cell center.
        """
        self.number_ues = number_ues
        self.positions = self.generate_position(cell_radius, cell_center)

    def generate_position(self, cell_radius:float, cell_center:complex): 
        """
        Generate random UE positions within the cell area.
        Ensures a minimum distance of 150 meters from the base station.

        Args:
            cell_radius (float): Cell radius in meters.
            cell_center (complex): Position of the cell center.

        Returns:
            np.ndarray: Array of positions for each UE.
        """
        positions = []
        while len(positions) < self.number_ues:
            ray = cell_radius * np.sqrt(np.random.rand())  # raiz para uniformidade na área
            if ray < 150:
                continue
    
            angle = 2*np.pi*np.random.rand() 
            position = cell_center + ray * np.exp(1j * angle)
            positions.append(position)

        return np.array(positions)

