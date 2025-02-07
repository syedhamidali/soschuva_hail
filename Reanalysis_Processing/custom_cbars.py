# -*- coding: utf-8 -*-
"""
CREATE CUSTOM COLORBARS

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ColorConverter

from misc_functions import make_colormap

converter = ColorConverter().to_rgb

cmap = make_colormap([converter("#99CCFF"), 0.1,
                      converter("#99CCFF"), converter("#18A04C"), 0.35,
                      converter("#18A04C"), converter("#FFDF8E"), 0.55,
                      converter("#FFDF8E"), 0.6,
                      converter("#FFDF8E"), converter("#D64646"), 0.85,
                      converter("#D64646"), converter("#0F0D0D")], 'dbz')
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#20314C"), converter("#7AADFF"), 0.2,
                      converter("#7AADFF"), converter("#F9F9F9"), 0.33,
                      converter("#F9F9F9"), converter("#F48244"), 0.45,
                      converter("#F48244"), converter("#470219")], 'zdr')
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#224C25"), converter("#CAE894"), 0.35,
                      converter("#CAE894"), converter("#F9F9F9"), 0.4,
                      converter("#F9F9F9"), converter("#AF95E2"), 0.55,
                      converter("#AF95E2"), converter("#3E0B5E")], 'kdp')
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#FFF0E2"), converter("#DDA65D"), 0.5,
                      converter("#DDA65D"), converter("#B21152"), 0.75,
                      converter("#B21152"), converter("#442F42"), 0.89,
                      converter("#442F42"), converter("#CCB69B"), 0.9,
                      converter("#CCB69B")], 'rho')
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#F7FCFA"), converter("#CCFFE3"), 0.15,
                      converter("#CCFFE3"), converter("#57D6CB"), 0.35,
                      converter("#57D6CB"), converter("#9399C6"), 0.65,
                      converter("#9399C6"), converter("#60205B")], 'mass')
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#FFFFFF"), 0.2,
                      converter("#FFFFFF"), converter("#93E1D8"), 0.4,
                      converter("#93E1D8"), converter("#FFA69E"), 0.6,
                      converter("#FFA69E"), converter("#AA4465"), 0.8,
                      converter("#AA4465"), converter("#5B0E3B")], 'wind')
plt.register_cmap(name=cmap.name, cmap=cmap, lut=48)

cmap = make_colormap([converter("#FFFFFF"), converter("#ECFFB0"), 0.25,
                      converter("#ECFFB0"), converter("#9AA899"), 0.5,
                      converter("#9AA899"), converter("#4A7B9D"), 0.75,
                      converter("#4A7B9D"), converter("#3A3C59")], 'vorticity')
plt.register_cmap(name=cmap.name, cmap=cmap, lut=48)

cmap = make_colormap([converter("#FFFFFF"), 0.05,
                      converter("#DAFF47"), converter("#EDA200"), 0.25,
                      converter("#EDA200"), converter("#D24E71"), 0.5,
                      converter("#D24E71"), converter("#91008D"), 0.75,
                      converter("#91008D"), converter("#001889")], 'cape')
plt.register_cmap(name=cmap.name, cmap=cmap, lut=48)
