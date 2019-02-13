#!/bin/csh
# c-shell script for Nino type prediction based on the CNN.

setenv CCC 'nino_type_12month'              # Name of case
setenv HHH '/home/jhkim/cnn/'       # Main directory

foreach conf ( 30 50 )      # Number of conv. features
foreach hidf ( 30 50 )      # Number of hidden neurons

setenv GGG 0                       # GPU number (0~3)
setenv ENN 10                      # Ensemble number

setenv SMF 'CMIP5/historical/MME.map.type.NDJ.1861_2003.nc'               # Sample of training data
setenv LBF 'CMIP5/historical/MME.label.type.one_hot_w20.DJF.1862_2004.nc ' # Label of training data
setenv EVD 'GODAS/godas.sst_t300.type.1980_2016.NDJ.nc'         # Sample of evaluation data
setenv EBD 'GODAS/godas.type.one_hot.1981_2017.nc'              # Label of training data

setenv TTT 1178                     # Total data size of training set
setenv SSS 1178                     # Training data size of training set

setenv TEV 13                      # Total data size of evaluation set
setenv SEV 0                       # Starting point of evaluation set
setenv EEV 13                      # Evaluation size

setenv XXX 72                       # X dimension
setenv YYY 24                       # Y dimension
setenv ZZZ  6                       # Z dimension

setenv BBB 250                      # Batch size
setenv EEE 2600                      # Epoch
setenv CDD 0.9                        # drop rate at the convolutional layer
setenv HDD 0.9                        # drop rate at the hidden layer

setenv opname 'C'$conf'H'$hidf

# Number of ensemble
@ ens = 1
while ( $ens <= $ENN )

mkdir -p $HHH/output/$CCC
mkdir -p $HHH/output/$CCC/src
mkdir -p $HHH/output/$CCC/$opname
mkdir -p $HHH/output/$CCC/$opname/EN$ens
mkdir -p $HHH/output/$CCC/$opname/ensmean

cd $HHH/output/$CCC/src
cp -f $HHH/sample/nino_type.train_cmip.sample .
cp -f $HHH/sample/nino_type.valid.sample .
cp -f $HHH/sample/nino_type.ensmean.sample .

# Run Training
sed "s/convfilter/$conf/g"   nino_type.train_cmip.sample > tmp1
sed "s/hiddfilter/$hidf/g"                          tmp1 > tmp2
sed "s#samfile#$SMF#g"                              tmp2 > tmp1
sed "s#labfile#$LBF#g"                              tmp1 > tmp2
sed "s/opfname/$opname/g"                           tmp2 > tmp1
sed "s/case/$CCC/g"                                 tmp1 > tmp2
sed "s/batsiz/$BBB/g"                               tmp2 > tmp1
sed "s/xxx/$XXX/g"                                  tmp1 > tmp2
sed "s/yyy/$YYY/g"                                  tmp2 > tmp1
sed "s/epoch/$EEE/g"                                tmp1 > tmp2
sed "s/TOTSIZ/$TTT/g"                               tmp2 > tmp1
sed "s/SAMSIZ/$SSS/g"                               tmp1 > tmp2
sed "s/CDRP/$CDD/g"                                 tmp2 > tmp1
sed "s/HDRP/$HDD/g"                                 tmp1 > tmp2
sed "s/zzz/$ZZZ/g"                                  tmp2 > tmp1
sed "s/number_gpu/$GGG/g"                           tmp1 > tmp2
sed "s#home_directory#$HHH#g"                       tmp2 > tmp1
sed "s/member/$ens/g"                               tmp1 > nino_type.train_cmip.py

python nino_type.train_cmip.py

# Run Evaluation
sed "s/convfilter/$conf/g"       nino_type.valid.sample > tmp1
sed "s/hiddfilter/$hidf/g"                         tmp1 > tmp2
sed "s#samfile#$EVD#g"                             tmp2 > tmp1
sed "s/opfname/$opname/g"                          tmp1 > tmp2
sed "s/case/$CCC/g"                                tmp2 > tmp1
sed "s/xxx/$XXX/g"                                 tmp1 > tmp2
sed "s/yyy/$YYY/g"                                 tmp2 > tmp1
sed "s/TOTSIZ/$TEV/g"                              tmp1 > tmp2
sed "s/SAMSIZ/$SEV/g"                              tmp2 > tmp1
sed "s/TSTSIZ/$EEV/g"                              tmp1 > tmp2
sed "s/zzz/$ZZZ/g"                                 tmp2 > tmp1
sed "s/number_gpu/$GGG/g"                          tmp1 > tmp2
sed "s#home_directory#$HHH#g"                      tmp2 > tmp1
sed "s/member/$ens/g"                              tmp1 > nino_type.valid.py

python nino_type.valid.py

@ ens = $ens + 1
end

#compute ensemble mean
sed "s/opfname/$opname/g"    nino_type.ensmean.sample > tmp1
sed "s/case/$CCC/g"                              tmp1 > tmp2
sed "s/TSTSIZ/$EEV/g"                            tmp2 > tmp1
sed "s/convfilter/$conf/g"                       tmp1 > tmp2
sed "s#home_directory#$HHH#g"                    tmp2 > tmp1
sed "s/numen/$ENN/g"                             tmp1 > nino_type.ensmean.py

python nino_type.ensmean.py


end
end


