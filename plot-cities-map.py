#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# PROGRAM: plot_cities_map.py
#------------------------------------------------------------------------------
# Version 0.1
# 1 September, 2023
# Michael Taylor
# https://patternizer.github.io
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------

# Numeric/Data libraries:    
import numpy as np
import pandas as pd
#import pickle
#from datetime import datetime
#import nc_time_axis
#import cftime

# Plotting libraries:
import matplotlib    
# matplotlib.use('agg')
# %matplotlib inline # for Jupyter Notebooks
import matplotlib.pyplot as plt; plt.close('all')
import matplotlib.ticker as mticker   # for gridlines
import matplotlib.cm as cm            # for cmap
import matplotlib.patches as mpatches # for polygons
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import rcParams
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Seaborn libraries
#import seaborn as sns; sns.set()

# Mapping libraries
import cartopy
import cartopy.crs as ccrs
from cartopy.io import shapereader
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

fontsize = 16
resolution = '10m' # 110, 50 or 10km
dpi = 600 # 144,300,600

#city, location_lat, location_lon = 'London', 51.5, -0.1
#city, location_lat, location_lon = 'Rennes', 48.1, -1.7
#city, location_lat, location_lon = 'Kisumu', -0.1, 34.8
#city, location_lat, location_lon = 'Nairobi', -1.3, 36.8
#city, location_lat, location_lon = 'Homa', -0.5, 34.5
#city, location_lat, location_lon = 'Beijing', 39.9, 116.4
#city, location_lat, location_lon = 'Ningbo', 29.9, 121.6

lats = np.array([51.5, 48.1, -0.1, -1.3, -0.5, 39.9, 29.9])
lons = np.array([-0.1, -1.7, 34.8, 36.8, 34.5, 116.4, 121.6])
cities = ['London', 'Rennes', 'Kisumu', 'Nairobi', 'Homa', 'Beijing', 'Ningbo']

# CARTOPY:

projection = 'robinson'

if projection == 'equalearth': p = ccrs.EqualEarth(central_longitude=0)
if projection == 'europp': p = ccrs.EuroPP()
if projection == 'geostationary': p = ccrs.Geostationary(central_longitude=0)
if projection == 'goodehomolosine': p = ccrs.InterruptedGoodeHomolosine(central_longitude=0)
if projection == 'lambertconformal': p = ccrs.LambertConformal(central_longitude=0)
if projection == 'mollweide': p = ccrs.Mollweide(central_longitude=0)
if projection == 'northpolarstereo': p = ccrs.NorthPolarStereo()
if projection == 'orthographic': p = ccrs.Orthographic(0,0)
if projection == 'platecarree': p = ccrs.PlateCarree(central_longitude=0)
if projection == 'robinson': p = ccrs.Robinson(central_longitude=0)
if projection == 'southpolarstereo': p = ccrs.SouthPolarStereo()    

'''
use_dark_theme = False
if use_dark_theme == True:
    default_color = 'white'
else:    
    default_color = 'black'    	

# Calculate current time

now = datetime.now()
currentdy = str(now.day).zfill(2)
currentmn = str(now.month).zfill(2)
currentyr = str(now.year)
titletime = str(currentdy) + '/' + currentmn + '/' + currentyr  

#-----------------------------------------------------------------------------
# METHODS:
#-----------------------------------------------------------------------------

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#-----------------------------------------------------------------------------
# MAKE COLOR SAFE PALETTE & CMAP
#-----------------------------------------------------------------------------

#plt.style.use('tableau-colorblind10')
#plt.style.library['tableau-colorblind10']

# GREYSCALE

# 'black'
# '#595959'   # dark grey
# '#898989'   # slate grey
# '#ABABAB'   # grey
# '#CFCFCF'   # light grey
# 'white'

# DIVERGING

# '#006BA4'   # dark steel blue
# '#5F9ED1'   # steel blue
# '#A2C8EC'   # light steel blue
# '#FFBC79'   # light salmon
# '#FF800E'   # orange
# '#C85200'   # chocolate

grey_dark = tuple( hex_to_rgb("#595959")[i]/255.0 for i in range(3) )
grey_slate = tuple( hex_to_rgb("#898989")[i]/255.0 for i in range(3) )
grey_mid = tuple( hex_to_rgb("#ABABAB")[i]/255.0 for i in range(3) )
grey_light = tuple( hex_to_rgb("#CFCFCF")[i]/255.0 for i in range(3) )

blue_dark = tuple( hex_to_rgb("#006BA4")[i]/255.0 for i in range(3) )
blue_mid = tuple( hex_to_rgb("#5F9ED1")[i]/255.0 for i in range(3) )
blue_light = tuple( hex_to_rgb("#A2C8EC")[i]/255.0 for i in range(3) )
orange_light = tuple( hex_to_rgb("#FFBC79")[i]/255.0 for i in range(3) )
orange_mid = tuple( hex_to_rgb("#FF800E")[i]/255.0 for i in range(3) )
orange_dark = tuple( hex_to_rgb("#C85200")[i]/255.0 for i in range(3) )

colorlist_greyscale = [ 'black', grey_dark, grey_mid, grey_light, 'white' ]
colorlist_diverging = [ blue_dark, blue_mid, blue_light, orange_light, orange_mid, orange_dark ]
colorlist_mixed = [ grey_dark, blue_dark, blue_light, grey_light, 'White', orange_light, orange_mid, orange_dark ]

cmap_greyscale = LinearSegmentedColormap.from_list('testCmap', colors=colorlist_greyscale, N=5)
cmap_diverging = LinearSegmentedColormap.from_list('testCmap', colors=colorlist_diverging, N=6)
cmap_mixed = LinearSegmentedColormap.from_list('testCmap', colors=colorlist_mixed, N=8)

colors = 'Colorsafe'

if colors == 'Viridis':    
    colors = px.colors.sequential.Viridis_r
elif colors == 'Cividis':    
    colors = px.colors.sequential.Cividis_r
elif colors == 'Plotly3':
    colors = px.colors.sequential.Plotly3_r
elif colors == 'Magma':
    colors = px.colors.sequential.Magma_r
elif colors == 'Shikari_lite':
    colors = ['#d8d7d5','#a1dcfc','#fdee03','#75b82b','#a84190','#0169b3']
elif colors == 'Shikari_dark':
    colors = ['#2f2f2f','#a1dcfc','#fdee03','#75b82b','#a84190','#0169b3']     
elif colors == 'Colorsafe':
    colors = colors=colorlist_mixed

#----------------------------------------------------------------------------
# DARK THEME
#----------------------------------------------------------------------------

if use_dark_theme == True:
    
    matplotlib.rcParams['text.usetex'] = False
    rcParams['font.family'] = ['Lato']
#    rcParams['font.family'] = 'sans-serif'
#    rcParams['font.sans-serif'] = ['Avant Garde', 'Lucida Grande', 'Verdana', 'DejaVu Sans' ]    
    plt.rc('text',color='white')
    plt.rc('lines',color='white')
    plt.rc('patch',edgecolor='white')
    plt.rc('grid',color='lightgray')
    plt.rc('xtick',color='white')
    plt.rc('ytick',color='white')
    plt.rc('axes',labelcolor='white')
    plt.rc('axes',facecolor='black')
    plt.rc('axes',edgecolor='lightgray')
    plt.rc('figure',facecolor='black')
    plt.rc('figure',edgecolor='black')
    plt.rc('savefig',edgecolor='black')
    plt.rc('savefig',facecolor='black')
    
else:

#    print('Using Seaborn graphics ...')

    matplotlib.rcParams['text.usetex'] = True
    rcParams['font.family'] = ['Lato']
#    rcParams['font.family'] = 'sans-serif'
#    rcParams['font.sans-serif'] = ['Avant Garde', 'Lucida Grande', 'Verdana', 'DejaVu Sans' ]    
    plt.rc('savefig',facecolor='white')
    plt.rc('axes',edgecolor='black')
    plt.rc('xtick',color='black')
    plt.rc('ytick',color='black')
    plt.rc('axes',labelcolor='black')
    plt.rc('axes',facecolor='white')
       
'''    
                
#------------------------------------------------------------------------------
# PLOT
#------------------------------------------------------------------------------
    
use_projection = 'robinson' # see projection list below

# SET: projection
    
if use_projection == 'equalearth': p = ccrs.EqualEarth(central_longitude=0)
if use_projection == 'europp': p = ccrs.EuroPP()
if use_projection == 'geostationary': p = ccrs.Geostationary(central_longitude=0)
if use_projection == 'goodehomolosine': p = ccrs.InterruptedGoodeHomolosine(central_longitude=0)
if use_projection == 'lambertconformal': p = ccrs.LambertConformal(central_longitude=0)
if use_projection == 'mollweide': p = ccrs.Mollweide(central_longitude=0)
if use_projection == 'northpolarstereo': p = ccrs.NorthPolarStereo()
if use_projection == 'orthographic': p = ccrs.Orthographic(0,0)
if use_projection == 'platecarree': p = ccrs.PlateCarree(central_longitude=0)
if use_projection == 'robinson': p = ccrs.Robinson(central_longitude=0)
if use_projection == 'southpolarstereo': p = ccrs.SouthPolarStereo()    
    
print('plotting city locations ...')
        
figstr = 'cities-map.png'
     
fig, ax = plt.subplots(figsize=(13.33,7.5), subplot_kw=dict(projection=p))    
# PowerPoint:            fontsize = 18; fig = plt.figure(figsize=(13.33,7.5), dpi=144); plt.savefig('figure.png', bbox_inches='tight')
# Posters  (vectorized): fontsize = 18; fig = plt.figure(figsize=(13.33,7.5), dpi=600); plt.savefig('my_figure.svg', bbox_inches='tight')                          
# Journals (vectorized): fontsize = 18; fig = plt.figure(figsize=(3.54,3.54), dpi=300); plt.savefig('my_figure.svg', bbox_inches='tight')     

borders = cf.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land', scale=resolution, facecolor='none', alpha=1)
land = cf.NaturalEarthFeature('physical', 'land', scale=resolution, edgecolor='k', facecolor=cf.COLORS['land'])
ocean = cf.NaturalEarthFeature('physical', 'ocean', scale=resolution, edgecolor='none', facecolor=cf.COLORS['water'])
#lakes = cf.NaturalEarthFeature('physical', 'lakes', scale=resolution, edgecolor='b', facecolor=cf.COLORS['water'])
#rivers = cf.NaturalEarthFeature('physical', 'rivers_lake_centerlines', scale=resolution, edgecolor='b', facecolor='none')
         
ax.set_global()  
ax.add_feature(land, facecolor='grey', linestyle='-', linewidth=0.1, edgecolor='k', alpha=1, zorder=1)
ax.add_feature(ocean, facecolor='lightgrey', alpha=1, zorder=2)
#ax.add_feature(lakes)
#ax.add_feature(rivers, linewidth=0.5)
# ax.add_feature(borders, linestyle='-', linewidth=0.1, edgecolor='k', alpha=1, zorder=2)         
# ax.coastlines(resolution=resolution, color='k', linestyle='-', linewidth=0.2, edgecolor='k', alpha=1, zorder=10)                                                                                  

#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=0.1, color='purple', alpha=1, linestyle='-', zorder=10)
#gl.top_labels = False; gl.bottom_labels = False; gl.left_ylabels = False; gl.right_ylabels = False
#gl.xlines = True; gl.ylines = True
#gl.xlocator = mticker.FixedLocator(np.linspace(-180,180,73)) # every 5 degrees
#gl.ylocator = mticker.FixedLocator(np.linspace(-90,90,37))   # every 5 degrees
#gl.xformatter = LONGITUDE_FORMATTER; gl.yformatter = LATITUDE_FORMATTER

plt.scatter(x=lons, y=lats, color="white", s=20, marker='o', edgecolor='k', lw=0.1, alpha=1, transform=ccrs.PlateCarree() )        
ax.coastlines(resolution=resolution, color='k', linestyle='-', linewidth=0.2, edgecolor='k', alpha=1, zorder=1000)                                                                                  
ax.add_feature(borders, linestyle='-', linewidth=0.1, edgecolor='k', alpha=1, zorder=2000)         
fig.tight_layout()
plt.savefig( figstr, dpi=dpi, bbox_inches='tight')
#plt.savefig( figstr, dpi=dpi)
#plt.clf()
#plt.cla()
plt.close()

#------------------------------------------------------------------------------
print('** END')

