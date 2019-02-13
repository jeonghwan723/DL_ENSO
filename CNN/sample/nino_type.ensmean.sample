#!/usr/bin/env python
import numpy as np
from tempfile import TemporaryFile

ipth = 'home_directory/output/case/opfname/'

tot = np.zeros((TSTSIZ,numen), dtype=np.float32)
for i in range(numen):
  f = open(ipth+'EN'+str(i+1)+'/result.gdat','r')
  tot[:,i] = np.fromfile(f, dtype=np.float32)

sum_typ = np.zeros((TSTSIZ,3,numen), dtype=np.float32)
for i in range(TSTSIZ):
  for j in range(numen):
    if tot[i,j] == 0:
      sum_typ[i,0,j] = 1

    elif tot[i,j] == 1:
      sum_type[i,1,j] = 1

    else:
      sum_typ[i,2,j] = 1

mean_typ = np.mean(sum_typ, axis=2)

# save as ASCII
#np.savetxt(ipth+'/ensmean/result', tot2, delimiter=",")

# save as binary
mean_typ.astype('float32').tofile(ipth+'/ensmean/result.gdat')

ctl_EOF = open(ipth+'/ensmean/result.ctl','w')
ctl_EOF.write('dset ^result.gdat\n')
ctl_EOF.write('undef -9.99e+08\n')
ctl_EOF.write('xdef   1  linear  0.   5\n')
ctl_EOF.write('ydef   1  linear -55.  5\n')
ctl_EOF.write('zdef   3  linear  1 1\n')
ctl_EOF.write('tdef '+str(TSTSIZ)+'  linear jan0001 1yr\n')
ctl_EOF.write('vars   1\n')
ctl_EOF.write('pr    3   1  variable\n')
ctl_EOF.write('ENDVARS\n')

