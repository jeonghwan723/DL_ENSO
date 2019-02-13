#!/bin/csh
# c-shell script for heatmap analysis.

setenv TRM 'nino34_18month_Transfer_20'         # model name
setenv CCC 'nino34_18month_Transfer_20'         # output name
setenv HHH '/home/jhkim/cnn/'                   # Main directory

foreach conf ( 30 50 )      # Number of conv. features
foreach hidf ( 30 50 )      # Number of hidden neurons

setenv GGG 3                       # GPU number
setenv ENN 10                      # Ensemble number

setenv EVD 'data/GODAS/godas.sst_t300.1980_2015.36mon.nc'   # Input data file

setenv SEV 0                       # Start point of the data
setenv TEV 36                      # End point of the data

setenv XXX 72                       # X dimension
setenv YYY 24                       # Y dimension
setenv ZZZ  6                       # Z dimension

setenv opname 'C'$conf'H'$hidf

echo $opname

cd $HHH/output/$CCC/src
mkdir -p $HHH/output/$CCC/heatmap
mkdir -p $HHH/output/$CCC/heatmap/$opname
cp -f $HHH/sample/nino34.heatmap.sample .

# make layer
sed "s/convfilter/$conf/g"      nino34.heatmap.sample > tmp1
sed "s/hiddfilter/$hidf/g"                       tmp1 > tmp2
sed "s#samfile#$EVD#g"                           tmp2 > tmp1
sed "s/opfname/$opname/g"                        tmp1 > tmp2
sed "s/case/$CCC/g"                              tmp2 > tmp1
sed "s/xxx/$XXX/g"                               tmp1 > tmp2
sed "s/yyy/$YYY/g"                               tmp2 > tmp1
sed "s/zzz/$ZZZ/g"                               tmp1 > tmp2
sed "s/numberensemble/$ENN/g"                    tmp2 > tmp1
sed "s/st_size/$SEV/g"                           tmp1 > tmp2
sed "s/model_name/$TRM/g"                        tmp2 > tmp1
sed "s#home_directory#$HHH#g"                    tmp1 > tmp2
sed "s/nd_size/$TEV/g"                           tmp2 > nino34.heatmap.py


python nino34.heatmap.py

end
end

