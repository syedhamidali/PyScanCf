"""
@author: Hamid Ali Syed
@email: hamidsyed37[at]gmail[dot]com
"""

import os

import cartopy.crs as ccrs
import cartopy.feature as feat
import cmweather  ## noqa
import matplotlib.pyplot as plt
import numpy as np
import pyart  ##noqa
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from matplotlib.ticker import NullFormatter
from netCDF4 import num2date

# from . import register_colormap

# Cmaps config
CAPPI_CMAPS = {
    "REF": {
        "cmap": "SyedSpectral",
        "vmin": -20,
        "vmax": 70,
        "title": "Max-Z",
        "unit": "dBZ",
        "keywords": [
            "REF",
            "DBZH",
            "reflectivity",
            "DBZ",
            "ref",
            "DBZV",
            "DBZC",
            "refh",
            "Z",
        ],
    },
    "VEL": {
        "cmap": cmweather.cm.NWSVel,
        "vmin": -50,
        "vmax": 50,
        "title": "Max-V",
        "unit": "m/s",
        "keywords": [
            "VELH",
            "velocity",
            "VEL",
            "V",
            "radial_velocity",
            "VELOCITY",
            "VELV",
            "vel",
            "velh",
        ],
    },
    "WIDTH": {
        "cmap": cmweather.cm.NWS_SPW,
        "vmin": 0,
        "vmax": 4,
        "title": "Max-W",
        "unit": "m/s",
        "keywords": [
            "WIDTH",
            "WIDTHH",
            "SPW",
            "W",
            "spectrum_width",
            "width",
            "spectrum_width",
            "WIDTHV",
        ],
    },
}


def get_cmap_params(keyword):
    for k, v in CAPPI_CMAPS.items():
        if any([kw in keyword for kw in v["keywords"]]):
            v["name"] = k
            return v
    else:
        raise KeyError(f"'{keyword}' does not match the defined grid variable")


def plot_crosshair(ax_xy):
    background_color = ax_xy.get_facecolor()
    if sum(background_color[:3]) / 3 > 0.5:
        color = "k"
    else:
        color = "w"
    ax_xy.plot([0, 0], [-10e3, 10e3], color=color)
    ax_xy.plot([-10e3, 10e3], [0, 0], color=color)


def plot_cappi(
    grid,
    moment,
    cmap=None,
    vmin=None,
    vmax=None,
    title=None,
    colorbar=True,
    range_rings=True,
    crosshair=True,
    dpi=100,
    show_progress=True,
    savedir=None,
    show_figure=True,
    **kwargs,
):
    """Plots CAPPI
    grid: pyart grid object,
    moment(str): radar moment e.g., "REF", "VEL", "WIDTH"
    cmap: matplotlib colormap, optional
    vmin: minimum value for color scaling, optional
    vmax: maximum value for color scaling, optional
    title: plot title, optional
    colorbar: bool, plot colorbar or not, (default: True), optional
    range_rings: bool, (50 km interval), (default: True), optional
    crosshair: bool, (default: True), optional
    dpi: int, (default: 100), optional
    show_progress: bool, (default: True)
    savedir: string, path to save the plot, optional
    """

    try:
        param = get_cmap_params(keyword=moment)
        max_c = grid.fields[param["name"]]["data"].max(axis=0)
        max_x = grid.fields[param["name"]]["data"].max(axis=1)
        max_y = grid.fields[param["name"]]["data"].max(axis=2).T
    except KeyError:
        print(f"Error: '{moment}' does not match the defined moment")

    trgx = grid.x["data"]
    trgy = grid.y["data"]
    trgz = grid.z["data"]

    max_height = int(np.floor(grid.z["data"].max()) / 1e3)
    sideticks = np.arange(max_height / 4, max_height + 1, max_height / 4).astype(int)

    if cmap is None:
        cmap = param["cmap"]
        # cmap.set_under(color="none")
    if vmin is None:
        vmin = param["vmin"]
    if vmax is None:
        vmax = param["vmax"]
    if title is None:
        title = f"Max-{moment.upper()}"

    def plot_range_rings(ax_xy):
        background_color = ax_xy.get_facecolor()
        if sum(background_color[:3]) / 3 > 0.5:
            color = "k"
        else:
            color = "w"
        [
            ax_xy.plot(
                r * np.cos(np.arange(0, 360) * np.pi / 180),
                r * np.sin(np.arange(0, 360) * np.pi / 180),
                color=color,
                ls="-",
                linewidth=0.5,
                alpha=0.5,
            )
            for r in np.arange(5e4, np.floor(trgx.max()) + 1, 5e4)
        ]

    if show_progress:
        print("...............................")
        figtime = num2date(grid.time["data"], grid.time["units"])[0].strftime(
            "%Y%m%d%H%M%S"
        )
        print(f"Plotting {title} {figtime}")
        print("...............................\n")
    else:
        None

    lat_0 = grid.origin_latitude["data"][0]
    lon_0 = grid.origin_longitude["data"][0]
    proj = ccrs.LambertAzimuthalEqualArea(lon_0, lat_0)

    # FIG
    fig = plt.figure(figsize=[10.3, 10], tight_layout=True)
    left, bottom, width, height = 0.1, 0.1, 0.6, 0.2
    ax_xy = plt.axes((left, bottom, width, width), projection=proj)
    ax_x = plt.axes((left, bottom + width, width, height))
    ax_y = plt.axes((left + width, bottom, height, width))
    ax_cnr = plt.axes((left + width, bottom + width, left + left, height))
    if colorbar:
        ax_cb = plt.axes((left + width + height + 0.02, bottom, 0.02, width))

    # set axis label formatters
    ax_x.xaxis.set_major_formatter(NullFormatter())
    ax_y.yaxis.set_major_formatter(NullFormatter())
    ax_cnr.yaxis.set_major_formatter(NullFormatter())
    ax_cnr.xaxis.set_major_formatter(NullFormatter())
    ax_x.set_ylabel("Height AMSL (km)", size=13)
    ax_y.set_xlabel("Height AMSL (km)", size=13)

    # draw CAPPI
    plt.sca(ax_xy)
    xy = ax_xy.pcolormesh(trgx, trgy, max_c, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)

    def map_features(ax_xy):
        background_color = ax_xy.get_facecolor()
        if sum(background_color[:3]) / 3 > 0.5:
            color = "k"
        else:
            color = "w"
        gl = ax_xy.gridlines(
            crs=ccrs.PlateCarree(),
            linewidth=1,
            alpha=0.5,
            linestyle="--",
            draw_labels=True,
        )
        gl.xlabels_top = False
        gl.ylabels_left = True
        gl.ylabels_bottom = True
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {
            "color": color,
        }
        gl.ylabel_style = {
            "color": color,
        }

        # ax_xy.add_feature(shape_feature)
        ax_xy.add_feature(feat.COASTLINE, alpha=0.8, lw=1, ec=color)
        ax_xy.add_feature(feat.BORDERS, alpha=0.7, lw=0.7, ls="--", ec=color)
        ax_xy.add_feature(
            feat.STATES.with_scale("10m"), alpha=0.6, lw=0.5, ls=":", ec=color
        )

    map_features(ax_xy)

    if range_rings:
        plot_range_rings(ax_xy)

    ax_xy.set_xlim(trgx.min(), trgx.max())
    ax_xy.set_ylim(trgx.min(), trgx.max())

    # plot crosshair
    if crosshair:
        plot_crosshair(ax_xy)

    # draw colorbar
    if colorbar:
        cb = plt.colorbar(xy, cax=ax_cb)
        cb.set_label(param["unit"], size=15)

    plt.sca(ax_x)
    plt.pcolormesh(trgx / 1e3, trgz / 1e3, max_x, cmap=cmap, vmin=vmin, vmax=vmax)
    # plt.ylim(0,20)
    plt.yticks(sideticks)
    # plt.grid(axis='y')
    ax_x.set_xlim(trgx.min() / 1e3, trgx.max() / 1e3)

    plt.sca(ax_y)
    plt.pcolormesh(trgz / 1e3, trgy / 1e3, max_y, cmap=cmap, vmin=vmin, vmax=vmax)
    # plt.xlim(0,20)

    ax_y.set_xticks(sideticks)
    # plt.grid(axis='x')
    ax_y.set_ylim(trgx.min() / 1e3, trgx.max() / 1e3)

    plt.sca(ax_cnr)
    plt.tick_params(
        axis="both",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        left=False,
        right=False,
        labelbottom=False,
    )

    # labels along the bottom edge are off
    plt.text(0.32, 0.8, title, size=14, weight="bold")
    plt.text(0.09, 0.65, f"Max Range: {np.floor(trgx.max()/1e3)} km", size=12)
    plt.text(0.12, 0.5, f"Max Height: {np.floor(trgz.max()/1e3)} km", size=12)
    plt.text(
        0.15,
        0.3,
        num2date(grid.time["data"], grid.time["units"])[0].strftime("%H:%M:%S Z"),
        weight="bold",
        size=17,
    )
    plt.text(
        0.06,
        0.15,
        num2date(grid.time["data"], grid.time["units"])[0].strftime("%d %b, %Y UTC"),
        size=14,
    )

    ax_xy.set_aspect("auto")

    if savedir is not None:
        radar_name = grid.metadata["instrument_name"]
        figtime = num2date(grid.time["data"], grid.time["units"])[0].strftime(
            "%Y%m%d%H%M%S"
        )
        figname = f"{savedir}{os.sep}{title}_{radar_name}_{figtime}.png"
        plt.savefig(fname=figname, dpi=dpi, bbox_inches="tight")
        print(f"Figure(s) saved as {figname}")
    if show_figure:
        fig.show()
    else:
        plt.close()
