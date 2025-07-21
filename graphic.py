import numpy as np
import matplotlib.pyplot as plt

# TODO: Fazer uma função que mostrar a representação da rede, com as células e os usuários 

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