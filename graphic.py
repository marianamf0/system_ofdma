import numpy as np
from network import Network
from settings import Settings
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def graphic_network(network:Network): 
    fig, graf = plt.subplots(figsize = (6, 4), constrained_layout=True)
    circle = Circle((np.real(network.settings.cell_center), np.imag(network.settings.cell_center)), radius=network.settings.cell_radius, fill=False)
    graf.add_patch(circle)
    
    for index in range(6):
        position = network.settings.position_base_station_interference[index]
        circle = Circle((np.real(position), np.imag(position)), radius=network.settings.cell_radius, fill=False)
        graf.add_patch(circle)
    
    ue_positions = network.user_equipaments.positions
    graf.scatter(np.real(ue_positions), np.imag(ue_positions), marker='o', s=60, facecolors='white', edgecolors='red')
    
    graf.set_aspect('equal')
    graf.grid(True)
    plt.show()
    

def graphic_cdf(value:list, title_xlabel:str, xscale: str = "linear", name:str = None): 
    
    fig, graf = plt.subplots(figsize = (6, 4), constrained_layout=True) 
    graf.plot(sorted(value), np.linspace(0, 1, len(value)))
    graf.grid(True, which='major', linestyle='-', linewidth=0.75)
    graf.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    graf.set_xscale(xscale)
    graf.set_xlabel(title_xlabel, fontweight='bold')
    graf.set_ylabel("CDF", fontweight='bold')
    plt.show()
        
    if name != None: 
        fig.savefig(f"image/{name}.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        plt.show()

if __name__ == "__main__":
    
    settings = Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000)

    network = Network(settings=settings, number_ues=10)

    graphic_network(network)