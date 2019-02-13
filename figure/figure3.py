#!/usr/bin/env python
from netCDF4 import Dataset
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, addcyclic
import numpy as np

deg = u'\xb0'

CH_list = ['C30H30', 'C30H50', 'C50H30', 'C50H50']

# Open CNN (1981-2017)
f = open('/home/jhkim/cnn/output/ver4f_18month_SODA/combination.gdat','r')
cnn = np.fromfile(f, dtype=np.float32)

# Open New SINTEX (1984-2017)
f = open('/home/jhkim/data/SINTEX_ensemble2/prediction_em/nino3.4/nino3.4.18month_12.gdat','r')
sin = np.fromfile(f, dtype=np.float32)

# Open observation (GODAS, 1981-2017)
f = Dataset('/home/jhkim/data/GODAS/godas.nino.1981_2017.nc','r')
obs = f.variables['pr'][:,0,0,0]

cnn = cnn/np.std(cnn)
sin = sin/np.std(sin)
obs = obs/np.std(obs)

# open SST & HC map
f = Dataset('/home/jhkim/data/GODAS/godas.sst_t300.1980_2017.144x73.nc','r')
osst = np.mean(f.variables['sst'][:,4:7,:,:],axis=1)
ot300 = np.mean(f.variables['t300'][:,4:7,:,:],axis=1)

chimera = np.zeros(osst.shape, dtype=np.float32)
for i in range(osst.shape[0]):
  chimera[i,:,:] = osst[i,:,:]
  chimera[i,28:45,48:113] = ot300[i,28:45,48:113]

# Compute correlation coefficient (1984-2017)
cor_cnn = np.round(np.corrcoef(obs[3:],cnn[3:])[0,1],2)
cor_sin = np.round(np.corrcoef(obs[3:],sin)[0,1],2)
 
# Open Heatmap of each case (1981-2016)
heat_each = np.zeros((4,36,18,6), dtype=np.float32)
for i in range(4):
  f = open('/home/jhkim/analysis/heatmap-ver4f_18month_SODA/each_case/'+CH_list[i]+'/heatmap.gdat','r')
  heat_each[i,:,:,:] = np.fromfile(f, dtype=np.float32).reshape(37,18,6)[1:37,:,:]

heat_each = np.swapaxes(heat_each,2,3)
heat_each_mean = np.mean(heat_each, axis=0)

# 0-360 -> 0-380
# chimera: 38x73x144 -> 38x73x152
ext_chimera = np.append(chimera,chimera[:,:,0:8],axis=2)

# heatmap: 36x6x18 -> 36x6x19
ext_heatmap = np.append(heat_each_mean,heat_each_mean[:,:,0:1],axis=2)

# standard deviation (36x6x19 -> 6x19)
std_heatmap = np.std(ext_heatmap,axis=0)

# mean heatmap (36x6x19 -> 6x19)
mean_heatmap = np.mean(ext_heatmap,axis=0)

# significant test
mask_heatmap = np.zeros((36,6,19),dtype=np.float32)
for i in range(36):
  for j in range(6):
    for k in range(19):
      level = abs(ext_heatmap[i,j,k]-mean_heatmap[j,k])/(std_heatmap[j,k]/np.sqrt(37))
      if level > 2.56:
        mask_heatmap[i,j,k] = ext_heatmap[i,j,k]


# Draw Figure
# Figure 3-(a)
plt.subplot(2,1,1)
x = np.arange(1,38)
y = np.arange(4,38)
lines = plt.plot(x, obs, 'black', x, cnn, 'orangered', y, sin, 'dodgerblue')
my_plot = plt.gca()
line0 = my_plot.lines[0]
line1 = my_plot.lines[1]
line2 = my_plot.lines[2]
plt.setp(line0,linewidth=2)
plt.setp(line1,linewidth=0.5, marker='o', markersize=2)
plt.setp(line2,linewidth=0.5, marker='v', markersize=2)
plt.legend(('Observation','CNN(Cor='+str(cor_cnn)+')', 'SINTEX-F(Cor='+str(cor_sin)+')'),loc='upper right', prop={'size':7}, ncol=3)
plt.xlim([0,37])
plt.ylim([-3,3.5])
plt.xticks(np.arange(2,39,2),np.arange(1982, 2019, 2), fontsize=6.5)
plt.tick_params(labelsize=6.,direction='in',length=2,width=0.3,color='black')

plt.yticks(np.arange(-3,3.51,1), fontsize=6.5)
plt.grid(linewidth=0.2, alpha=0.7)
plt.axhline(0,color='black',linewidth=0.5)
plt.title('(a) 18-month lead prediction for DJF Nino3.4', fontsize=8, x=0.268, y=0.967)
plt.xlabel('Year', fontsize=7)
plt.ylabel('DJF Nino3.4', fontsize=7)

# Figure 3-(b)
plt.subplot(2,1,2)

x, y  = np.meshgrid(np.arange(0,380,2.5), np.arange(-91.25,91.25,2.5))

# Contour
CS = plt.contour(x,y,ext_chimera[1996-1980,:,:],np.arange(0.5,1.501,0.5),colors='black',linewidths=0.6)
plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=False)
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]
zc = CS.collections[0]
plt.setp(zc, linewidth=0.6)
for line in CS.collections:
  if line.get_linestyle() == [(None, None)]:
    print("Solid Line")
  else:
    line.set_linestyle([(0, (5, 3))])

CS = plt.contour(x,y,ext_chimera[1996-1980,:,:],np.arange(-1.5,0,0.5),colors='black',linewidths=0.6)
plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=False)
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]
zc = CS.collections[0]
plt.setp(zc, linewidth=0.6)
for line in CS.collections:
  if line.get_linestyle() == [(None, None)]:
    print("Solid Line")
  else:
    line.set_linestyle([(0, (5, 3))])

# shade
cax = plt.imshow(mask_heatmap[1996-1981,:,:], cmap='RdBu_r',clim=[-20,20], extent=[0,380,60,-55],zorder=1)
plt.gca().invert_yaxis()
map = Basemap(projection='cyl', llcrnrlat=-55,urcrnrlat=59, resolution='c',
              llcrnrlon=20, urcrnrlon=380)
map.drawcoastlines(linewidth=0.2)
map.drawparallels(np.arange( -90., 90.,30.),labels=[1,0,0,0],fontsize=6.5,
                  color='grey', linewidth=0.2)
map.drawmeridians(np.arange(0.,380.,60.),labels=[0,0,0,1],fontsize=6.5,
                  color='grey', linewidth=0.2)
map.fillcontinents(color='silver', zorder=3)
space = '                                                               '
plt.title('(b) MJJ 1996 Heatmap'+space+'[97/98 El Niño Case]',fontsize=8, y=0.962,x=0.5)

x = [  120,   280,   280,   120,   120]
y = [  -16,   -16,    23,    23,   -16]
plt.plot(x,y,'black',zorder=4,linewidth=0.9)

cax = plt.axes([0.08, 0.073, 0.72, 0.013])
cbar = plt.colorbar(cax=cax, orientation='horizontal')
cbar.ax.tick_params(labelsize=6.5,direction='out',length=2,width=0.4,color='black')

plt.tight_layout(h_pad=0,w_pad=-0.6)
plt.subplots_adjust(bottom=0.10, top=0.9, left=0.08, right=0.8)
plt.savefig('/home/jhkim/analysis/fig/figure3.png', dpi=1000)
plt.close()







