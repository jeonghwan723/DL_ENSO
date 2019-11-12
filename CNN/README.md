
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


## Data set

   -  you can download data set here: https://drive.google.com/open?id=1cbeA3pGF9Ls-U805uFIwa21DhzMRD2eK
   
   -  The data set consists of the following:
   
       (1) Training set: [CMIP5.input.36mon.1861_2001.nc], [CMIP5.label.12mon.1863_2003.nc]
       
       (2) Training set for transfer learning: [SODA.input.36mon.1871_1970.nc], [SODA.label.12mon.1873_1972.nc]
       
       (3) validation set: [GODAS.input.36mon.1980_2015.nc], [GODAS.label.12mon.1982_2017.nc]

## Reference
Ham, Y. G., Kim, J. H. & Luo, J.-J. Deep learning for multi-year ENSO forecasts. Nature 573, https://doi.org/10.1029/2010JC006695 (2019).

## Requirement (python packages)

   -  Tensowflow (https://www.tensorflow.org/install/)
   -  netCDF4
   
## Basic tutorial: https://www.tensorflow.org/tutorials/
