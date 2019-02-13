#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, addcyclic
import numpy as np

yr_list = [[[1986, 1997],[1994, 2014],[1997, 1986],[2009, 2014],[2009, 1994]],
           [[2014, 2004],[2004, 2002],[1994, 2004],[2014, 2002],[1994, 2009]]]

yr_list = np.array(yr_list)

sea_list = [10, 1, 4, 7]

tit_list = ['(b) NDJ (12-mon. before)', '(f) NDJ (12-mon. before)',
            '(c) FMA (9-mon. before) ', '(g) FMA (9-mon. before) ',
            '(d) MJJ (6-mon. before) ', '(h) MJJ (6-mon. before) ',
            '(e) ASO (3-mon. before) ', '(i) ASO (3-mon. before) ']

txt_list = [' Best EP', ' Best CP']

s_xdim2 = [ 8, 24, 24, 32, 56]
e_xdim2 = [25, 53, 57, 61, 73]
s_ydim2 = [ 4, 16,  8,  0,  8]
e_ydim2 = [17, 25, 17,  9, 17]

acc_list = [66.67, 40.00, 58.33, 50.00, 41.67, 41.67, 41.67, 33.33, 33.33, 25.00] 
model_list = ['CNN', 'MMM', 'CanCM4', 'CCSM3', 'CanCM3', 'GFDL-\nFLOR-A06', 
              'GFDL-\nFLOR-B01', 'GFDL-\naer04', 'SINTEX-F', 'CCSM4']

# Open input map
f = Dataset('/home/jhkim/data/ERSST.v5/ersst.map.1950_2017.12mon.72x24.nc','r')
sst = f.variables['sst'][1976-1950:,:,:,:].reshape(42,1,12,24,72)

f = Dataset('/home/jhkim/data/NCEP/ncep.map.1948_2017.12mon.72x24.nc','r')
t1000 = f.variables['t'][1976-1948:,:,:,:].reshape(42,1,12,24,72)
u925 = f.variables['u'][1976-1948:,:,:,:].reshape(42,1,12,24,72)
v925 = f.variables['v'][1976-1948:,:,:,:].reshape(42,1,12,24,72)

ncep = np.append(sst,u925,axis=1)
ncep = np.append(ncep,v925,axis=1)

# Seasonal mean
season = np.zeros((2,2,5,3,4,24,72),dtype=np.float32) # nino_type,case,year,var,season,ydim,xdim
for i in range(2):
  for l in range(2):
    for j in range(5):
      for k in range(4):
        if k == 0:
          season[i,l,j,:,k,:,:] = np.mean(np.append(ncep[int(yr_list[i,j,l]-1976-1),:,10:12,:,:],
                        ncep[int(yr_list[i,j,l]-1976),:,0,:,:].reshape(3,1,24,72),axis=1),axis=1)
  
        else:
          season[i,l,j,:,k,:,:] = np.mean(ncep[int(yr_list[i,j,l]-1976),:,
                                sea_list[k]:sea_list[k]+4,:,:],axis=1)

# 0-360 -> 0-380
ext_season = np.append(season,season[:,:,:,:,:,:,:4],axis=6)  #2,2,6,3,4,24,76

# mean highest 3 case
mean_ext_season = np.mean(ext_season[:,:,:,:,:,:,:],axis=1)   #2,2,3,4,24,76

# (type, var, season, ydim, xdim)
chimera = np.zeros((2,3,4,24,76),dtype=np.float32)
chimera[:,:,:,:,:] = np.nan

ep_area = [0]
cp_area = [0, 3, 4]
for j in range(2):

  if j == 0:
   for i in ep_area:
     chimera[j,:,:,s_ydim2[i]:e_ydim2[i],s_xdim2[i]:e_xdim2[i]] = mean_ext_season[j,
                 i,:,:,s_ydim2[i]:e_ydim2[i],s_xdim2[i]:e_xdim2[i]]

  if j == 1:
   for i in cp_area:
     chimera[j,:,:,s_ydim2[i]:e_ydim2[i],s_xdim2[i]:e_xdim2[i]] = mean_ext_season[j,
                 i,:,:,s_ydim2[i]:e_ydim2[i],s_xdim2[i]:e_xdim2[i]]

mask_u = chimera[:,1,:,:,:]
mask_v = chimera[:,2,:,:,:]

width = 0.5
col_list = ['orangered', 'black', 'navy', 'darkorange', 'forestgreen', 'gold', 'indianred', 'purple', 'dodgerblue', 'sienna']

# draw figure a
plt.subplot2grid((29,2),(0,0),colspan=2,rowspan=8)
for i in range(10):

   plt.bar(i, acc_list[i], width, color=col_list[i], zorder=4)

x2 = np.arange(-0.5, 10.5001,1)
conf1 = plt.fill_between(x2, 8.33, 58.33, facecolor='black', alpha=0.2, edgecolor=None)

plt.xticks(np.arange(0,10,1), model_list, fontsize=5)
plt.yticks(np.arange(0,81,10), fontsize=5)
plt.ylim([0,75])
plt.xlim([-0.5, 9.5])
plt.text(-0.5, 77, '(a) Hit rate of 12-month lead prediction of El Niño type (1984-2017)', fontsize=5.5)
plt.ylabel('Hit rate (%)', fontsize=5.5)
plt.tick_params(labelsize=4.5,direction='in',length=3,width=0.4,color='black')
for i in range(20,80,10):
  plt.axhline(i, color='black', linewidth=0.3, alpha=0.3)

cmap = plt.cm.get_cmap('RdBu_r')
clevs = np.arange(-1.2,1.201,0.1)

for i in range(4):
  for j in range(2):

   plt.subplot2grid((29,2),((i*5)+9,j),rowspan=5)

   x, y  = np.meshgrid(np.arange(0,380,5), np.arange(-57.5,62.5,5))
   x1, y1  = np.meshgrid(np.arange(40,120.01,5), np.arange(-37.5,22.51,5))
   x2, y2  = np.meshgrid(np.arange(160,300.01,5), np.arange(-57.5,-17.51,5))
   x3, y3  = np.meshgrid(np.arange(280,360.01,5), np.arange(-17.5,22.51,5))

   # vector
   skip = (slice(None,None,2), slice(None,None,1))
   r = plt.quiver(x1[skip], y1[skip],
         mask_u[j,i,s_ydim2[0]:e_ydim2[0],s_xdim2[0]:e_xdim2[0]][skip], 
         mask_v[j,i,s_ydim2[0]:e_ydim2[0],s_xdim2[0]:e_xdim2[0]][skip],
         scale=50, color='black', headaxislength=3.0, headlength=9.5, headwidth=8, width=0.0024,
         zorder=4, edgecolor='black')

   r = plt.quiver(x2[skip], y2[skip],
         mask_u[j,i,s_ydim2[3]:e_ydim2[3],s_xdim2[3]:e_xdim2[3]][skip], 
         mask_v[j,i,s_ydim2[3]:e_ydim2[3],s_xdim2[3]:e_xdim2[3]][skip],
         scale=50, color='black', headaxislength=3.0, headlength=9.5, headwidth=8, width=0.0024,
         zorder=4, edgecolor='black')

   if j == 1:
     r = plt.quiver(x3[skip], y3[skip],
           mask_u[j,i,s_ydim2[4]:e_ydim2[4],s_xdim2[4]:e_xdim2[4]][skip], 
           mask_v[j,i,s_ydim2[4]:e_ydim2[4],s_xdim2[4]:e_xdim2[4]][skip],
           scale=50, color='black', headaxislength=3.0, headlength=9.5, headwidth=8, width=0.0024,
           zorder=4, edgecolor='black')

   # Shading
   cax = plt.contourf(x,y,chimera[j,0,i,:,:],clevs,cmap=cmap,extend='both')
   plt.gca().invert_yaxis()
   map = Basemap(projection='cyl', llcrnrlat=-60,urcrnrlat=60, resolution='c',
                 llcrnrlon=20, urcrnrlon=380)
   map.drawparallels(np.arange( -30., 60.,30.),labels=[1,0,0,0],fontsize=5.2,
                     color='grey', linewidth=0.2, zorder=4)
   map.drawmeridians(np.arange(0.,380.,60.),labels=[0,0,0,1],fontsize=5.2,
                     color='grey', linewidth=0.2, zorder=4)
   map.fillcontinents(color='lightgrey')

   plt.text(20,65,tit_list[int(j+(i*2))],fontsize=5.5)
   plt.text(296,65,txt_list[j],fontsize=5.5)

   if i == 3 and j == 1:
     plt.quiverkey(r,0.85,-0.37,5,"5 m/s",labelpos='S', fontproperties={'size':'5'}, labelsep=0.05)

   if j == 0:
     plt.text(55,27.5,'86, 97',fontsize=5,zorder=4)

   if j == 1:
     plt.text(55,27.5,'14, 04',fontsize=5,zorder=4)
     plt.text(205,-14,'14, 02',fontsize=5,zorder=4)
     plt.text(295,27.5,'94, 09',fontsize=5,zorder=4)

   # IO
   x = [   40,   120,  120,   40,    40]
   y = [  -37.5,   -37.5,   22.5,   22.5,   -37.5]
   plt.plot(x,y,'black',zorder=4,linewidth=0.5)

   if j == 1:
     # SP
     x = [  160,   300,   300,   160,   160]
     y = [  -57.5,   -57.5,   -17.5,   -17.5,   -57.5]
     plt.plot(x,y,'black',zorder=4,linewidth=0.5)

     # EA
     x = [  280,   360,   360,   280,   280]
     y = [  -17.5,   -17.5,    22.5,    22.5,   -17.5]
     plt.plot(x,y,'black',zorder=4,linewidth=0.5)

     cax = plt.axes([0.12, 0.033, 0.42, 0.014])
     cbar = plt.colorbar(cax=cax, orientation='horizontal')
     cbar.ax.tick_params(labelsize=5,direction='out',length=2,width=0.4,color='black')

plt.tight_layout(h_pad=1,w_pad=2.4)
plt.subplots_adjust(bottom=0.08, top=0.95, left=0.1, right=0.63)
plt.savefig('/home/jhkim/analysis/fig/figure4.png', dpi=1000)
plt.close()




