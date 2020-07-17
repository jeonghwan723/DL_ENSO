
## Processes of the Nino3.4 prediction

   - Training with CMIP5 (csh/nino34.cmip.csh)
   
       (1) training (import from sample/nino34.train_cmip.sample)
       
       (2) validation (import from sample/nino34.valid.sample)
      
       (3) ensemble mean (import from sample/nino34.ensmean.sample)

   - Transfer learning with SODA (csh/nino34.transfer.csh)
   
       (1) training (import from sample/nino34.train_transfer.sample)
       
       (2) validation (import from sample/nino34.valid.sample)
       
       (3) ensemble mean (import from sample/nino34.ensmean.sample)

   - Heatmap analysis (csh/nino34.heatmap.csh)
          (import from sample/nino34.heatmap.sample)



## Processes of the El Nino type prediction

   - Training with CMIP5 (csh/nino_type.cmip.csh)
   
       (1) training (import from sample/nino_type.train_cmip.sample)
       
       (2) validation (import from sample/nino_type.valid.sample)
       
       (3) ensemble mean (import from sample/nino_type.ensmean.sample)

   - Heatmap analysis (csh/nino_type.heatmap.csh)
          (import from nino_type.heatmap.sample)


## Data set (netCDF4)

   -  you can download data set here: https://drive.google.com/file/d/1Ht6__G4bFWguZTJ3nKc3XuEY1KKLMIIN/view?usp=sharing
   
   -  The data set consists of the following:
   
       
       - Dataset for Nino3.4 forecast
   
          (1) Training set (CMIP5/): 
              Input: [CMIP5.input.36mn.1861_2001.nc]
              
              Label for 2-23month lead: [CMIP5.label.nino34.12mn_3mv.1863_2003.nc]
              
              Label for 1month lead: [CMIP5.label.nino34.12mn_2mv.1863_2003.nc]
       
          (2) Training set for transfer learning (SODA/)
              Input: [SODA.input.36mn.1871_1970.nc]
              Label for 2-23month lead: [SODA.label.nino34.12mn_3mv.1873_1972.nc]
              Label for 1month lead: [SODA.label.nino34.12mn_2mv.1873_1972.nc]
       
          (3) validation set (GODAS/)
              Input: [GODAS.input.36mn.1980_2015.nc]
              Label for 2-23month lead: [GODAS.label.12mn_3mv.1982_2017.nc]
              Label for 1month lead: [GODAS.label.12mn_2mv.1982_2017.nc]
          
          
        - Dataset for El Nino type forecast
        
          (1) Training set (CMIP5/)
              Input: [CMIP5.input.type.NDJ.1861_2001.nc]
              Label: [CMIP5.label.type.DJF.1863_2003.nc]
       
          (2) validation set (GODAS/)
              Input: [GODAS.input.36mn.1980_2015.nc]
              Label: [GODAS.label.type.DJF.1982_2017.nc]        
          
          
## Reference
Ham, Y. G., Kim, J. H. & Luo, J.-J. Deep learning for multi-year ENSO forecasts. Nature 573, https://doi.org/10.1029/2010JC006695 (2019).

## Requirement (python packages)

   -  Tensowflow (https://www.tensorflow.org/install/) 
      ( < version 2.0 )
   -  netCDF4
   
## Basic tutorial: https://www.tensorflow.org/tutorials/
