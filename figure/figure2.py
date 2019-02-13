#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.axes as ax
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, addcyclic

import numpy as np

minorLocator = AutoMinorLocator()

deg = u'\xb0'

conf_level =  [0.00142586,  0.0013108,   0.00240254,  0.00472927,  0.00650972,  0.0067122,
               0.00688624,  0.0088501,   0.01059312,  0.01154113,  0.01227826,  0.01225191,
               0.01160514,  0.01276475,  0.0140228,   0.01330945,  0.01300398,  0.014542,
               0.01392549,  0.01294643,  0.01569229,  0.01362468,  0.01339665]

sin_sig = [0.00219253,  0.00215715,  0.00364602,  0.00764075,  0.01048163,  0.01112115,
           0.01117301,  0.01377985,  0.01689541,  0.01778051,  0.01971778,  0.01968366,
           0.01801804,  0.02020356,  0.02213454,  0.02159965,  0.02070482,  0.02220418,
           0.02168681,  0.01996531,  0.02439883,  0.02181871,  0.02171612]

cm4_sig = [ 0.00151429,  0.00132075,  0.00216883,  0.00346866,  0.00397897,  0.00543547,
            0.00783759,  0.01191416,  0.01500621,  0.01839906,  0.02145076,  0.02329749]

             
mon_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
mon_list_skip = ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23']
mon_name = ['JFM','FMA','MAM','AMJ','MJJ','JJA','JAS','ASO','SON','OND','NDJ','DJF']

cor_sintex = np.zeros((23,12))
cor_cnn = np.zeros((23,12))
cor_cm3 = np.zeros((12,12))
cor_cm4 = np.zeros((12,12))
cor_ccsm3 = np.zeros((12,12))
cor_ccsm4 = np.zeros((12,12))
cor_aer04 = np.zeros((12,12))
cor_flora = np.zeros((12,12))
cor_florb = np.zeros((12,12))

for i in range(0,23,1):
  for j in range(1,13,1):

    # Open label
    if i == 0 or i ==23:
      f = Dataset('/home/jhkim/data/GODAS/godas.nino.2mn_mov.1982_2017.nc','r')
      lab = f.variables['pr'][2:,int(j-1),0,0]
    else:
      f = Dataset('/home/jhkim/data/GODAS/godas.nino.1982_2017.LAG.nc','r')
      lab = f.variables['pr'][2:,int(j-1),0,0]

    # Open SINTEX output
    f = open('/home/jhkim/data/SINTEX_ensemble2/prediction_em/nino3.4/nino3.4.'+str(i+1)+'month_'+str(j)+'.gdat','r')
    sin = np.fromfile(f, dtype=np.float32)

    # Open CNN output (Transfer Learning)
    f = open('/home/jhkim/cnn/output/ver6a_'+str(i+1)+'month_'+str(j)+'_Transfer_20/combination.gdat','r')
    cnn = np.fromfile(f, dtype=np.float32)[2:]

    if i < 12:

      # open CMC1-CanCM3 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/CMC1-CanCM3/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      cm3 = np.fromfile(f, dtype=np.float32)

      # open CMC2-CanCM4 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/CMC2-CanCM4/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      cm4 = np.fromfile(f, dtype=np.float32)

      # open COLA-RSMAS-CCSM3 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/COLA-RSMAS-CCSM3/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      ccsm3 = np.fromfile(f, dtype=np.float32)

      # open COLA-RSMAS-CCSM4 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/COLA-RSMAS-CCSM4/nino34.'
                +str(i+1)+'month_'+str(j)+'.gdat','r')
      ccsm4 = np.fromfile(f, dtype=np.float32)

      # open GFDL-CM2p1-aer04 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/GFDL-CM2p1-aer04/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      aer04 = np.fromfile(f, dtype=np.float32)

      # open GFDL-CM2p5FLOR-A06 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/GFDL-CM2p5-FLOR-A06/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      flora = np.fromfile(f, dtype=np.float32)

      # open GFDL-CM2p5-FLOR-B01 result
      f = open('/home/jhkim/data/NMME_Phase1/prediction_2017/GFDL-CM2p5-FLOR-B01/nino34.'
               +str(i+1)+'month_'+str(j)+'.gdat','r')
      florb = np.fromfile(f, dtype=np.float32)

    # Compute correlation coefficient
    pick_cnn = np.zeros((34),dtype=np.float32)
    pick_sin = np.zeros((34),dtype=np.float32)
    pick_lab = np.zeros((34),dtype=np.float32)
    pick_cm3 = np.zeros((34),dtype=np.float32)
    pick_cm4 = np.zeros((34),dtype=np.float32)
    pick_ccsm3 = np.zeros((34),dtype=np.float32)
    pick_ccsm4 = np.zeros((34),dtype=np.float32)
    pick_aer04 = np.zeros((34),dtype=np.float32)
    pick_flora = np.zeros((34),dtype=np.float32)
    pick_florb = np.zeros((34),dtype=np.float32)
    num = 0
    for k in range(34):
      if sin[k] != -9.99e+08:
        pick_cnn[num] = cnn[k]
        pick_sin[num] = sin[k]
        pick_lab[num] = lab[k]
        if i < 12:
          pick_cm3[num] = cm3[k]
          pick_cm4[num] = cm4[k]
          pick_ccsm3[num] = ccsm3[k]
          pick_ccsm4[num] = ccsm4[k]
          pick_aer04[num] = aer04[k]
          pick_flora[num] = flora[k]
          pick_florb[num] = florb[k]
          
        num = num + 1

    cor_sintex[int(i),int(j-1)] = np.corrcoef(pick_lab[0:num],pick_sin[0:num])[0,1]
    cor_cnn[int(i),int(j-1)]    = np.corrcoef(pick_lab[0:num],pick_cnn[0:num])[0,1]
    if i < 12:
      cor_cm3[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_cm3[0:num])[0,1]
      cor_cm4[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_cm4[0:num])[0,1]
      cor_ccsm3[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_ccsm3[0:num])[0,1]
      cor_ccsm4[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_ccsm4[0:num])[0,1]
      cor_aer04[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_aer04[0:num])[0,1]
nt(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_flora[0:num])[0,1]
      cor_florb[int(i),int(j-1)]  = np.corrcoef(pick_lab[0:num],pick_florb[0:num])[0,1]


mean_cor_cnn =   np.mean(cor_cnn,axis=1)
mean_cor_sin =   np.mean(cor_sintex,axis=1)
mean_cor_cm3   = np.mean(cor_cm3,axis=1)
mean_cor_cm4   = np.mean(cor_cm4,axis=1)
mean_cor_ccsm3 = np.mean(cor_ccsm3,axis=1)
mean_cor_ccsm4 = np.mean(cor_ccsm4,axis=1)
mean_cor_aer04 = np.mean(cor_aer04,axis=1)
mean_cor_flora = np.mean(cor_flora,axis=1)
mean_cor_florb = np.mean(cor_florb,axis=1)

# set confidence interval
upper = np.zeros((23),dtype=np.float32)
lower = np.zeros((23),dtype=np.float32)
upper_sin = np.zeros((23),dtype=np.float32)
lower_sin = np.zeros((23),dtype=np.float32)
upper_cm4 = np.zeros((12))
lower_cm4 = np.zeros((12))
for i in range(23):
  upper[i] = mean_cor_cnn[i]+conf_level[i]
  lower[i] = mean_cor_cnn[i]-conf_level[i]
  upper_sin[i] = mean_cor_sin[i] + sin_sig[i]
  lower_sin[i] = mean_cor_sin[i] - sin_sig[i]
  if i <= 11:
    upper_cm4[i] = mean_cor_cm4[i] + cm4_sig[i]
    lower_cm4[i] = mean_cor_cm4[i] - cm4_sig[i]

cnn_map = np.swapaxes(cor_cnn,0,1)
sin_map = np.swapaxes(cor_sintex,0,1)

# Figure 2-(a)
plt.subplot2grid((2,2),(0,0),rowspan=1,colspan=2)
x = np.arange(0,23,1)
y = np.arange(0,12,1)
z = np.arange(0,9,1)
lines = plt.plot(x, mean_cor_cnn, 'orangered', x, mean_cor_sin, 'dodgerblue',
                 y, mean_cor_cm3, 'forestgreen', y, mean_cor_cm4, 'navy',
                 y, mean_cor_ccsm3, 'darkorange', y, mean_cor_ccsm4, 'sienna',
                 y, mean_cor_aer04, 'purple', y, mean_cor_flora, 'gold',
                 y, mean_cor_florb, 'indianred')

my_plot = plt.gca()
line0 = my_plot.lines[0]
line1 = my_plot.lines[1]

error = plt.fill_between(x,lower,upper,facecolor='orangered',alpha=0.3,edgecolor=None)
error = plt.fill_between(x,lower_sin,upper_sin,facecolor='dodgerblue',alpha=0.3,edgecolor=None)
error = plt.fill_between(y,lower_cm4,upper_cm4,facecolor='navy',alpha=0.3,edgecolor=None)
my_err = plt.gca()

plt.setp(lines,linewidth=1.2, marker='v', markersize=2)
plt.setp(line0,linewidth=1.4, marker='o', markersize=2)
plt.setp(line1,linewidth=1.4, marker='o', markersize=2)

model_list = ['CNN', 'SINTEX-F', 'CanCM3', 'CanCM4', 'CCSM3', 'CCSM4', 'GFDL-aer04', 'GFDL-FLOR-A06', 'GFDL-FLOR-B01']

plt.legend(model_list,loc='upper right', prop={'size':6}, ncol=5)
plt.xlabel('Forecast Lead (months)', fontsize=7)
plt.ylabel('Correlation Skill', fontsize=7)
plt.xticks(np.arange(0,23,1), np.arange(1,24,1), fontsize=6)
plt.yticks(np.arange(0.3,0.91,0.1), fontsize=6)
plt.ylim([0.25,1.0])
plt.grid(linewidth=0.1, alpha=0.7)
plt.axhline(0.5,color='black',linewidth=0.5)
plt.title('(a) All-season correlation skills for Nino3.4 (1984-2017)', fontsize=8, x=0.3, y=0.97)
plt.tick_params(labelsize=6,direction='in',length=3,width=0.4,color='black')
zm1 = np.ma.masked_less(cnn_map,0.5)
zm2 = np.ma.masked_less(sin_map,0.5)
x = np.arange(-0.5,22)
y = np.arange(-0.5,12)

# Figure 2-(b)
plt.subplot2grid((2,2),(1,0),rowspan=1,colspan=1)
plt.pcolor(x, y, zm1, hatch='/////', alpha=0.,zorder=4)
mpl.rcParams['hatch.linewidth'] = 0.45
plt.imshow(cnn_map,cmap='OrRd',clim=[0.0,1.0])
plt.gca().invert_yaxis()
plt.yticks(np.arange(0,12,1),mon_name,fontsize=5)
plt.xticks(np.arange(0,23,2),np.arange(1,24,2), fontsize=4)
plt.ylabel('Target season',fontsize=7)
ax=plt.gca()
ax.yaxis.set_label_coords(-0.11, 0.5)
ax.xaxis.set_label_coords(0.5, -0.11)
plt.xlabel('Forecast lead (months)',fontsize=7)
plt.title('(b) Correlation Skill - CNN', fontsize=8, x=0.29, y=0.96)
plt.tick_params(labelsize=6,direction='in',length=2,width=0.3,color='black',right=True)
cax = plt.axes([0.75, 0.42, 0.015, 0.28])
cbar = plt.colorbar(cax=cax,orientation='vertical')
cbar.ax.tick_params(labelsize=6,direction='out',length=2,width=0.4,color='black')

# Figure 2-(c)
plt.subplot2grid((2,2),(1,1),rowspan=1,colspan=1)
plt.pcolor(x, y, zm2, hatch='/////', alpha=0.,zorder=4)
plt.imshow(sin_map,cmap='OrRd',clim=[0.0,1.0])
plt.gca().invert_yaxis()
plt.yticks(np.arange(0,12,1),mon_name, fontsize=5)
plt.xticks(np.arange(0,23,2),np.arange(1,24,2), fontsize=4)
plt.xlabel('Forecast lead (months)',fontsize=7)
plt.title('(c) Correlation skill - SINTEX-F', fontsize=8, x=0.34, y=0.96)
plt.tick_params(labelsize=6,direction='in',length=2,width=0.3,color='black',right=True)
ax=plt.gca()
ax.xaxis.set_label_coords(0.5, -0.11)
cax = plt.axes([0.19, 0.1, 0.6, 0.015])
cbar = plt.colorbar(cax=cax,orientation='horizontal')
cbar.ax.tick_params(labelsize=5,direction='out',length=2,width=0.4,color='black')
plt.tight_layout(h_pad=0.5,w_pad=0.2)
plt.subplots_adjust(left=0.08, right=0.9, bottom=0.12, top=0.94)
plt.savefig('/home/jhkim/analysis/fig/Figure_2', dpi=1000)
plt.close()

