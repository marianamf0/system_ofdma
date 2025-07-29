import numpy as np
from network import Network
from settings import Settings
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

def graphic_network(network:Network): 
    """
    Plot the network layout.

    Args:
        network (Network): The network object containing cell and UE information.
    """
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
    """
    Plot a Cumulative Distribution Function (CDF) of the given values.

    Args:
        value (list): Values to compute and plot the CDF.
        title_xlabel (str): Label for the X-axis.
        xscale (str, optional): Scale for the X-axis ("linear" or "log"). Defaults to "linear".
        name (str, optional): If provided, saves the figure as a PNG in the 'image/' directory. Defaults to None.
    """
    
    fig, graf = plt.subplots(figsize = (6, 4), constrained_layout=True) 
    graf.plot(sorted(value), np.linspace(0, 1, len(value)))
    graf.grid(True, which='major', linestyle='-', linewidth=0.75)
    graf.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    graf.set_xscale(xscale)
    graf.set_xlabel(title_xlabel, fontweight='bold')
    graf.set_ylabel("CDF", fontweight='bold')
        
    if name != None: 
        fig.savefig(f"image/{name}.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        plt.show()
        
def graphic_cdf_per_scheduler2(output:dict, title_xlabel:str, title_parameters:str, name:str = None): 
    """
    Plot CDF graphs for total and per-user capacity under different scheduling strategies and power allocation methods.

    Args:
        output (dict): Dictionary containing simulation results. Keys follow the format "<Scheduler> (<Power Strategy>)".
            Each value is another dict with:
                - "total" (list): Total cell capacity values for all simulations.
                - "individual" (list): Per-user capacity values for all simulations.
        title_xlabel (str): Label for the x-axis (e.g., "Capacity (Mbps)").
        title_parameters (str): String containing parameters of the scenario to display in the subplot titles.
        xscale (str, optional): X-axis scale (e.g., "linear" or "log"). Defaults to "linear".
        name (str, optional): If provided, saves the figure as a PNG in the 'image/' directory. Defaults to None.
    """
    cmap = plt.get_cmap("tab10")
    line_styles = {"Round-Robin": "-", "Max-SINR": "--"}
    fig, graf = plt.subplots(2, 2, figsize = (12, 8), constrained_layout=True) 
    
    legend_linestyle = [Line2D([0], [0], color='black', linestyle=linestyle, label=label) 
                        for label, linestyle in line_styles.items()]
    
    for index, strategy in enumerate(["Uniform Power", "Inverse Pathloss Power"]): 
        style_legend = []
        for index_subcarriers, subcarriers in enumerate(list(output.keys())): 
            for scheduler, linestyle_scheduler in line_styles.items(): 
                output_subcarriers = output[subcarriers][scheduler][strategy]
                
                value = output_subcarriers["total"]
                graf[index, 0].plot(sorted(value), np.linspace(0, 1, len(value)),
                                    color=cmap(index_subcarriers), linestyle=linestyle_scheduler)
                
                value = output_subcarriers["individual"]
                graf[index, 1].plot(sorted(value), np.linspace(0, 1, len(value)), 
                                    color=cmap(index_subcarriers), linestyle=linestyle_scheduler)

            style_legend.append(
                Line2D([0], [0], color=cmap(index_subcarriers), linestyle='-', label=rf"$N$ = {subcarriers}")
            )
            
            for index_graf, title in enumerate(["Total Cell Capacity", "Per-UE Capacity"]): 
                graf[index, index_graf].grid(True, which='major', linestyle='-', linewidth=0.75)
                graf[index, index_graf].tick_params(axis='both', which='both', direction='in', top=True, right=True)
                graf[index, index_graf].set_xscale("linear")
                graf[index, index_graf].set_xlabel(title_xlabel, fontweight='bold')
                graf[index, index_graf].set_ylabel("CDF", fontweight='bold')
                graf[index, index_graf].set_title(f"{title} - {strategy} and {title_parameters}", fontweight='bold')
                
        
                legend1 = graf[index, index_graf].legend(handles=style_legend + legend_linestyle, loc="lower right")
                graf[index, index_graf].add_artist(legend1)
                        
    if name != None: 
        fig.savefig(f"image/{name}.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        plt.show()

        
def graphic_cdf_per_scheduler(output:dict, title_xlabel:str, title_parameters:str, name:str = None): 
    """
    Plot CDF graphs for total and per-user capacity under different scheduling strategies and power allocation methods.

    Args:
        output (dict): Dictionary containing simulation results. Keys follow the format "<Scheduler> (<Power Strategy>)".
            Each value is another dict with:
                - "total" (list): Total cell capacity values for all simulations.
                - "individual" (list): Per-user capacity values for all simulations.
        title_xlabel (str): Label for the x-axis (e.g., "Capacity (Mbps)").
        title_parameters (str): String containing parameters of the scenario to display in the subplot titles.
        xscale (str, optional): X-axis scale (e.g., "linear" or "log"). Defaults to "linear".
        name (str, optional): If provided, saves the figure as a PNG in the 'image/' directory. Defaults to None.
    """
    cmap = plt.get_cmap("tab10")
    base_colors = {"Round-Robin": 'blue', "Max-SINR": "red"}
    line_styles = {"Uniform Power": "-", "Inverse Pathloss Power": "--"}
    fig, graf = plt.subplots(2, 2, figsize = (12, 8), constrained_layout=True) 
    
    legend_linestyle = [Line2D([0], [0], color='black', linestyle=linestyle, label=label) 
                        for label, linestyle in line_styles.items()]
    for index, scheduler_name in enumerate(["Round-Robin", "Max-SINR"]): 
        style_legend = []
        for index_subcarriers, subcarriers in enumerate(list(output.keys())): 
            output_subcarriers = output[subcarriers][scheduler_name]
            
            for strategy, linestyle_strategy in line_styles.items(): 
                
                value = output_subcarriers[strategy]["total"]
                graf[index, 0].plot(sorted(value), np.linspace(0, 1, len(value)),
                                    color=cmap(index_subcarriers), linestyle=linestyle_strategy)
                
                value = output_subcarriers[strategy]["individual"]
                graf[index, 1].plot(sorted(value), np.linspace(0, 1, len(value)), 
                                    color=cmap(index_subcarriers), linestyle=linestyle_strategy)
            
            style_legend.append(
                Line2D([0], [0], color=cmap(index_subcarriers), linestyle='-', label=rf"$N$ = {subcarriers}")
            )
            
            for index_graf, title in enumerate(["Total Cell Capacity", "Per-UE Capacity"]): 
                graf[index, index_graf].grid(True, which='major', linestyle='-', linewidth=0.75)
                graf[index, index_graf].tick_params(axis='both', which='both', direction='in', top=True, right=True)
                graf[index, index_graf].set_xscale("linear")
                graf[index, index_graf].set_xlabel(title_xlabel, fontweight='bold')
                graf[index, index_graf].set_ylabel("CDF", fontweight='bold')
                graf[index, index_graf].set_title(f"{title} - {scheduler_name} Scheduler ({title_parameters})", fontweight='bold')

                legend1 = graf[index, index_graf].legend(handles=style_legend + legend_linestyle, loc="lower right")
                graf[index, index_graf].add_artist(legend1)
                        
    if name != None: 
        fig.savefig(f"image/{name}.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        plt.show()

if __name__ == "__main__":
    
    settings = Settings(number_subcarriers = 32, path_loss_exponent = 4, cell_radius = 1000)
    network = Network(settings=settings, number_ues=10)
    graphic_network(network)