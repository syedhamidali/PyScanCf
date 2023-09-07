"""
Colormap created using https://syedha.com/colormaps
"""
# import numpy as np
# import matplotlib as mpl
# import os


# # Define colormap data
# data_dir = os.path.split(__file__)[0]
# syed_spectral_vals = np.genfromtxt(os.path.join(data_dir, 'SyedSpectral_RGB.txt'))
# cmap_data = {
#     'SyedSpectral': syed_spectral_vals,
# }

# # Register colormaps
# for cmap_name, rgb_colors in cmap_data.items():
#     # Normalize the RGB values to the range [0, 1]
#     c = rgb_colors / 255.0

#     # Create a ListedColormap
#     cmap = mpl.colors.ListedColormap(c)

#     # Register the colormap
#     mpl.colormaps.register(cmap=cmap, name=cmap_name, force=True)

# # Usage example:
# if __name__ == "__main__":
#     # Now you can use 'SyedSpectral' colormap in your plots
#     pass


import numpy as np
import matplotlib as mpl
import os


def register_colormap(data_dir):
    # Define colormap data
    # data_dir = os.path.split(__file__)[0]
    syed_spectral_vals = np.genfromtxt(os.path.join(data_dir, "SyedSpectral_RGB.txt"))
    cmap_data = {
        "SyedSpectral": syed_spectral_vals,
    }

    # Register colormaps
    for cmap_name, rgb_colors in cmap_data.items():
        # Normalize the RGB values to the range [0, 1]
        c = rgb_colors / 255.0

        # Create a ListedColormap
        cmap = mpl.colors.ListedColormap(c)

        # Register the colormap
        mpl.colormaps.register(cmap=cmap, name=cmap_name, force=True)


# data_dir = os.path.split(__file__)[0]
SyedSpectral = register_colormap(data_dir=os.path.split(__file__)[0])
