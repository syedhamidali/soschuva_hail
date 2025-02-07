#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netCDF4 import Dataset
import numpy as np
from osgeo import osr
from osgeo import gdal
import time as t

# Define KM_PER_DEGREE
KM_PER_DEGREE = 111.32

# GOES-16 Spatial Reference System
sourcePrj = osr.SpatialReference()
# Non-Operational
sourcePrj.ImportFromProj4('+proj=geos +h=35786023.0 +a=6378137.0 +b=6356752.31414 +f=0.00335281068119356027489803406172 +lat_0=0.0 +lon_0=-89.5 +sweep=x +no_defs')
# Operational
# sourcePrj.ImportFromProj4('+proj=geos +h=35786000 +a=6378140 +b=6356750 +lon_0=-75 +sweep=x')

# Lat/lon WSG84 Spatial Reference System
targetPrj = osr.SpatialReference()
#targetPrj.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
targetPrj.ImportFromProj4('+proj=latlong +datum=WGS84')

def exportImage(image,path):
    driver = gdal.GetDriverByName('netCDF')
    return driver.CreateCopy(path,image,0)

def getGeoT(extent, nlines, ncols):
    # Compute resolution based on data dimension
    resx = (extent[2] - extent[0]) / ncols
    resy = (extent[3] - extent[1]) / nlines
    return [extent[0], resx, 0, extent[3] , 0, -resy]

def getScaleOffset(path):
    nc = Dataset(path, mode='r')
    scale = nc.variables['CMI'].scale_factor
    offset = nc.variables['CMI'].add_offset
    nc.close()
    return scale, offset

def remap(path, extent, resolution, x1, y1, x2, y2):

    # GOES-16 Extent (satellite projection) [llx, lly, urx, ury]
    GOES16_EXTENT = [x1, y1, x2, y2]

    # Setup NetCDF driver
    gdal.SetConfigOption('GDAL_NETCDF_BOTTOMUP', 'NO')

    # Read scale/offset from file
    scale, offset = getScaleOffset(path)

    try:
        connectionInfo = 'NETCDF:\"' + path + '\":CMI'
        # Open NetCDF file (GOES-16 data)
        raw = gdal.Open(connectionInfo)
    except:
        connectionInfo = 'HDF5:\"' + path + '\"://CMI'
        # Open NetCDF file (GOES-16 data)
        raw = gdal.Open(connectionInfo)

    # Setup projection and geo-transformation
    raw.SetProjection(sourcePrj.ExportToWkt())
    #raw.SetGeoTransform(getGeoT(GOES16_EXTENT, raw.RasterYSize, raw.RasterXSize))
    raw.SetGeoTransform(getGeoT(GOES16_EXTENT, raw.RasterYSize, raw.RasterXSize))

    #print (KM_PER_DEGREE)
    # Compute grid dimension
    sizex = int(((extent[2] - extent[0]) * KM_PER_DEGREE) / resolution)
    sizey = int(((extent[3] - extent[1]) * KM_PER_DEGREE) / resolution)

    # Get memory driver
    memDriver = gdal.GetDriverByName('MEM')

    # Create grid
    grid = memDriver.Create('grid', sizex, sizey, 1, gdal.GDT_Float32)

    # Setup projection and geo-transformation
    grid.SetProjection(targetPrj.ExportToWkt())
    grid.SetGeoTransform(getGeoT(extent, grid.RasterYSize, grid.RasterXSize))

    # Perform the projection/resampling

    print('Remapping ' + path)

    start = t.time()

    gdal.ReprojectImage(raw, grid, sourcePrj.ExportToWkt(), targetPrj.ExportToWkt(), gdal.GRA_NearestNeighbour, options=['NUM_THREADS=ALL_CPUS'])

    print('- finished! Time: ' + str(t.time() - start) + ' seconds')

    # Close file
    raw = None

    # Read grid data
    array = grid.ReadAsArray()

    # Mask fill values (i.e. invalid values)
    np.ma.masked_where(array, array == -1, False)

    # Apply scale and offset
    array = array * scale + offset

    #grid.GetRasterBand(1).SetNoDataValue(-1)
    grid.GetRasterBand(1).WriteArray(array)

    return grid
