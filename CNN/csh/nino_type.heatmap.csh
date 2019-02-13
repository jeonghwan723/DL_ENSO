#!/bin/csh
# c-shell script for the heatmap analysis.

setenv CCC 'nino_type'              # case name (experiment name)
setenv HHH '/home/jhkim/cnn/'       # Main directory

foreach conf ( 30 50 )      # Number of conv. features
foreach hidf ( 30 50 )      # Number of hidden neurons

setenv GGG 3                       # GPU number
setenv ENN 10                      # Ensemble number

setenv EVD 'data/GODAS/godas.sst_t300.type.1980_2017.NDJ.nc'         # Input data file

setenv SEV 0                       # Start point of the data
setenv TEV 13                      # End point of the data

setenv XXX 72                       # X dimension
setenv YYY 24                       # Y dimension
setenv ZZZ  6                       # Z dimension

setenv opname 'C'$conf'H'$hidf

echo $opname

cd $HHH/output/$CCC/src
mkdir -p $HHH/output/$CCC/heatmap
mkdir -p $HHH/output/$CCC/heatmap/$opname
cp -f $HHH/sample/nino_type.heatmap.sample .

# make layer
sed "s/convfilter/$conf/g"   nino_type.heatmap.sample > tmp1
sed "s/hiddfilter/$hidf/g"                       tmp1 > tmp2
sed "s#samfile#$EVD#g"                           tmp2 > tmp1
sed "s/opfname/$opname/g"                        tmp1 > tmp2
sed "s/case/$CCC/g"                              tmp2 > tmp1
sed "s/xxx/$XXX/g"                               tmp1 > tmp2
sed "s/yyy/$YYY/g"                               tmp2 > tmp1
sed "s/zzz/$ZZZ/g"                               tmp1 > tmp2
sed "s/numberensemble/$ENN/g"                    tmp2 > tmp1
sed "s/st_size/$SEV/g"                           tmp1 > tmp2
sed "s#home_directory#$HHH#g"                    tmp2 > tmp1
sed "s/nd_size/$TEV/g"                           tmp1 > nino_type.heatmap.py

python nino_type.heatmap.py

end
end


