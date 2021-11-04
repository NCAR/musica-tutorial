import numpy as np

def SE_ZonalMeridional(Data,Area,input_coords,Regridding_res,**kwargs):  
    """
    This function will be used for calculating area-weighted Zonal/Meridional information
    
    Data: SE data 
    
    Area: Area with similar length as Data
    
    input_coords: Latitude or Longitude coordinates for zonal or meridional info, respectively
    
    Regridding_res: The regular grid resolution for calculating the output means
    
    **kwargs:
        Type: Default to Zonal. Should be changed to Meridional if desired
    
    """
    Type=kwargs.pop('Type','Zonal')
    
    
    # Calculating output_coords
    if Type=='Zonal':
        n = int(180/Regridding_res+1)
        x = np.linspace(-90,90,n)
    elif Type=='Meridional':
        n = int(360/Regridding_res+1)
        x = np.linspace(-180,180,n)    
    else:
        print('ZonalMeridional Error: Type is wrong')
    
      
    # Find the nearest indices for the coords
    output_idx=[]
    for tmp_l in input_coords:
        tmp_data=(x-tmp_l)**2    # distance
        idx=np.where(tmp_data==np.min(tmp_data))[0][0]  # find the index of nearest x
        output_idx.append(int(idx))
    output_idx=np.array(output_idx)    
    
    
    # Calculate the area-weighted means for the ZonalMeridional data
    data=[]
    for idx in range(len(x)):
        tmp=np.where(output_idx==idx)

        tmp_mean=np.nansum(Data[tmp]*Area[tmp])/np.nansum(Area[tmp])

        data.append(tmp_mean)
    data=np.array(data)
     
    return data,x
