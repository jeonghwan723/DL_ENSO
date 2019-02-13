#!/usr/bin/env python
import numpy as np
from tempfile import TemporaryFile

ipth = 'home_directory/output/case/opfname/'

tot = np.zeros((TSTSIZ,numen), dtype=np.float32)
for i in range(numen):
  f = open(ipth+'EN'+str(i+1)+'/result.gdat','r')
  tot[:,i] = np.fromfile(f, dtype=np.float32)

ens_mean = np.mean(tot,axis=1)

# save as ASCII
#np.savetxt(ipth+'/ensmean/result', tot2, delimiter=",")

# save as binary
ens_mean.astype('float32').tofile(ipth+'/ensmean/result.gdat')

