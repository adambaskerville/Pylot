import matplotlib.patheffects as PathEffects
from shapely.geometry import multipolygon
from shapely.geometry import polygon
import matplotlib.pyplot as plt
import matplotlib
import geopandas

import numpy as np

from cartopy.io import shapereader
import cartopy.crs as ccrs
import cartopy


def draw(countries, values, resolution='50m', category='cultural', name='admin_0_countries'):
    # read the shapefile using geopandas
    df = geopandas.read_file(shapereader.natural_earth(resolution, category, name))

    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    ax.set_extent([-150, 60, -25, 60])

    # Add natural earth features and borders
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=1)
    ax.coastlines(resolution=resolution)

    # Normalise the lag times to between 0 and 1 to extract the colour
    lags_norm = (values - np.nanmin(values)) / (np.nanmax(values) - np.nanmin(values))

    # Choose your colourmap here
    cmap = matplotlib.cm.get_cmap('summer')

    for country, lag_norm, value in zip(countries, lags_norm, values):
        # read the borders of the country in this loop
        poly = df.loc[df['ADMIN'] == country]['geometry'].values[0]
        if isinstance(poly, polygon.Polygon):
            poly = multipolygon.MultiPolygon([poly])
        # get the color for this country
        rgba = cmap(lag_norm)
        # plot the country on a map
        centroid = max(poly, key=lambda x: x.area).centroid

        ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor=rgba, edgecolor='none', zorder=1)
        ax.text(centroid.x, centroid.y, f"{value}", color='white', size=25, ha='center',
                va='center', transform=ccrs.PlateCarree(),
                path_effects=[PathEffects.withStroke(linewidth=5, foreground="black", alpha=.9)])
