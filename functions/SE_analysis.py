'''
SE_analysis.py
this code is designed for supplying some code for post-processing of SE(-RR) output
(1) get_scrip_slice: For regional history file from SE(-RR) output
(2) get_site_index: To get model index with taking into account grid boundaries

MODIFICATION HISTORY:
    Duseong Jo, 19, AUG, 2021: VERSION 1.00
    - Initial version
'''

### Module import ###
import numpy as np
import xarray as xr



def get_scrip_slice( lon_region, lat_region, scrip_file='' ):
    '''
    NAME:
           get_scrip_slice

    PURPOSE:
           calculate slice of scrip to use regional SE(-RR) output files

    INPUTS:
           lon_region: longitude array in degrees from regional output
           lat_region: latitude array in degrees from regional output
           scrip_file: scrip filename for grid information 
                       or can be xarray Dataset (global grid)
           index: if provided, return indices to extract 
                  regional lon/lat values from global lon/lat values
    '''

    if type(scrip_file) == xr.core.dataset.Dataset:
        ds_scrip = scrip_file
    elif type(scrip_file) == str:
        ds_scrip = xr.open_dataset( scrip_file )  
    elif scrip_file == '':
        raise ValueError( 'scrip_file must be provided!' )        
    else:
        raise ValueError( 'Check scrip_file keyword!' )
    
    
    lon_global = ds_scrip['grid_center_lon'].values
    lat_global = ds_scrip['grid_center_lat'].values

    
    lonlat_index = np.zeros( len(lon_region) ).astype('i')

    for i in np.arange( len(lon_region) ):
        lonlat_index[i] = np.argmin( np.abs( lon_region[i] - lon_global ) )

    print( 'Check SUM - longitudes: ', np.sum( np.abs(lon_global[ lonlat_index ] - lon_region) ), 
                        'latitudes: ', np.sum( np.abs(lat_global[ lonlat_index ] - lat_region) ) )

    return ds_scrip.isel( grid_size=lonlat_index ), lonlat_index



def get_site_index( site_lon, site_lat, scrip_file='' ):
    '''
    NAME:
           get_site_index

    PURPOSE:
           calculate site index for unstructured (SE) grids

    INPUTS:
           site_lon: site longitude in degrees
           site_lat: site latitude in degrees
           scrip_file: scrip filename for grid information
    '''
    
    if type(scrip_file) == xr.core.dataset.Dataset:
        ds_scrip = scrip_file
    elif type(scrip_file) == str:
        ds_scrip = xr.open_dataset( scrip_file )  
    elif scrip_file == '':
        raise ValueError( 'scrip_file must be provided!' )        
    else:
        raise ValueError( 'Check scrip_file keyword!' )

        
    candidates = ( np.abs( site_lat - ds_scrip['grid_center_lat'].values ) + \
                   np.abs( site_lon - ds_scrip['grid_center_lon'].values ) ).argsort()[0:10]
    
    for index_c in candidates:
        for jj in np.arange( len(ds_scrip.grid_corners) ):

            lat_checks = np.sort( [ds_scrip['grid_center_lat'][index_c], 
                                   ds_scrip['grid_corner_lat'][index_c,jj] ] )
            lon_checks = np.sort( [ds_scrip['grid_center_lon'][index_c], 
                                   ds_scrip['grid_corner_lon'][index_c,jj] ] )

            if ( (site_lat <= lat_checks[1]) & (site_lat >= lat_checks[0]) ) & \
               ( (site_lon <= lon_checks[1]) & (site_lon >= lon_checks[0]) ):
                index_site = index_c
                return index_site

    