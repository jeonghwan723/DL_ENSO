
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


## You can download Data set through the link below

   -  https://drive.google.com/open?id=1cbeA3pGF9Ls-U805uFIwa21DhzMRD2eK
   
   The data set consists of the following:
     -  Training set: [CMIP5.input.36mon.1861_2001.nc], [CMIP5.label.12mon.1863_2003.nc]
     -  Training set for transfer learning: [SODA.input.36mon.1871_1970.nc], [SODA.label.12mon.1873_1972.nc]
     -  validation set: [GODAS.input.36mon.1980_2015.nc], [GODAS.label.12mon.1982_2017.nc]


## Requirement (python packages)

   -  Tensowflow (https://www.tensorflow.org/install/)
   -  netCDF4
   
## You can find tutorials basic codes at here: https://www.tensorflow.org/tutorials/
