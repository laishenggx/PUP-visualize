import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from metpy.io.nexrad import Level3File
import datetime
import matplotlib as mpl

def v_color_PUP():
    import matplotlib.colors as colors
    cdict = [(126/ 255, 224 / 255, 255/ 255), (0 / 255, 224 / 255, 255 / 255), (0,176 / 255, 176 / 255)
          , (0 / 255, 255 / 255, 0 / 255), (0 / 255, 196 / 255, 0 / 255), (0 / 255, 128 / 255,0 / 255)
             , (255 / 255, 255 / 255,255/ 255), (255/ 255, 255 / 255,255 / 255), (255 / 255, 0 / 255,0/ 255)
             , (255 / 255,88 / 255,88/ 255), (255 / 255, 176 / 255,176 / 255), (255 / 255, 124/ 255,0 / 255)
             , (255 / 255, 210 / 255,0 / 255), (255 / 255, 255 / 255,0 / 255),(124 / 255, 0 / 255, 124 / 255)]#
    v_cmap = colors.ListedColormap(cdict, 'indexed')
    return v_cmap,mpl.colors.BoundaryNorm([-60,-27,-20,-15,-10,-5,-1,0,1,5,10,15,20,27,40,45], v_cmap.N)

# Open the file
f = Level3File('C:\\pyproj\\cinrad\\pupdata\\V\\26\\20170330.093021.02.26.778')
knots2ms=True

datadict = f.sym_block[0][0]
data1 = np.ma.array(datadict['data'])
data1[data1 == 0] = np.ma.masked
if knots2ms:
    data2=f.map_data(data1)*0.53
else:
    data2 = f.map_data(data1)
data = np.ma.masked_invalid(data2)
data_rf=data1+30

az = np.array(datadict['start_az'] + [datadict['end_az'][-1]])
rng = np.linspace(0, f.max_range, data.shape[-1] + 1)

xlocs = rng * np.sin(np.deg2rad(az[:, np.newaxis]))  #第一维是方位角，第二维是极径
ylocs = rng * np.cos(np.deg2rad(az[:, np.newaxis]))

sta_lon=f.lon  #站点经纬度
sta_lat=f.lat
a=6.371e3
dy=2*a*np.pi/360.0
lon=np.zeros(xlocs.shape)
lat=np.zeros(xlocs.shape)
for i in range(xlocs.shape[0]):
     for j in range(xlocs.shape[1]): #先算纬度，然后再确定经度
         lat[i,j]=sta_lat+ylocs[i][j]/dy
         dx=np.cos(np.deg2rad(lat[i][j]))*dy
         lon[i,j]=sta_lon+xlocs[i][j]/dx

fig, ax = plt.subplots(figsize=(10, 10))

width = 2800; lon_0 = sta_lon; lat_0 = sta_lat
m = Basemap(width=width,height=width,projection='aeqd',
            lat_0=lat_0,lon_0=lon_0)

m.readshapefile('C:\\dt\\county_2004', 'sf', color='w',linewidth=0.6)
m.readshapefile('C:\\dt\\dijishi_2004', 'aa', drawbounds=False)
for info, shape in zip(m.aa_info, m.aa):
    if info['LEVEL2_ID'] == 274:
        x, y = zip(*shape)
        m.plot(x, y, marker=None, color='red', linewidth=0.8)

v_cmap,v_norm=v_color_PUP()
lons,lats=m(lon,lat)
m.pcolormesh(lons, lats, data_rf,cmap=v_cmap,norm=v_norm) #画距离折叠
cf1=m.pcolormesh(lons, lats, data,cmap=v_cmap,norm=v_norm) #画速度

for cir in [25,50,75,100,115]:#画等距离圈
    cir_lon=lon[:,np.where(rng==cir)].flatten()
    cir_lat = lat[:, np.where(rng == cir)].flatten()
    cir_lon,cir_lat=m(cir_lon,cir_lat)
    m.plot(cir_lon,cir_lat,color=(1,161/255,123/255),linewidth=0.5)

for az_line in np.arange(30,360+30,30):
    az_lon=[sta_lon,lon[np.where(np.rint(az)==az_line),-1][0,0]]
    az_lat=[sta_lat,lat[np.where(np.rint(az)==az_line),-1][0,0]]
    az_lon,az_lat=m(az_lon,az_lat)
    m.plot(az_lon, az_lat, color=(1,161/255,123/255), linewidth=0.5)


vt=f.metadata['vol_time']+datetime.timedelta(hours=8)

ax.text(1, 1.05,'基本速度(V 26) 仰角:%3.1f$^o$\nMAX:%2dm/s MIN:%2dm/s'%(f.metadata['el_angle'],round(f.metadata['max']*0.514),round(f.metadata['min']*0.514)),
        transform=ax.transAxes, fontdict={'family':'SimHei','size':13,'color':'r'},horizontalalignment='right')
ax.text(1, 1.015,'%4d年%02d月%02d日 %02d:%02d:%02d(BJT)'%(vt.year,vt.month,vt.day,vt.hour,vt.minute,vt.second),
        transform=ax.transAxes, fontdict={'family':'SimHei','size':13,'color':'blue'},horizontalalignment='right')
ax.text(1.07, 0.85,'m/s', transform=ax.transAxes,fontsize=12)
ax.text(1.07, 0.90,'RF', transform=ax.transAxes,fontsize=12)
ax.text(0.005, 1.015, '站点:河池(Z9778)\n雷达：CINRAD/SB(%6.2f$^o$E/%5.2f$^o$N,1047.7m)\n分辨率:1$^o$x0.5km 数据范围:115km\n扫描模式:VCP21-Precipitation'
        %(sta_lon,sta_lat), transform=ax.transAxes,fontdict={'family':'SimHei','size':13,'color':'k'})

cb=fig.colorbar(cf1,ax=ax,pad=0.02,shrink=0.7,aspect=20)
cb.ax.tick_params(labelsize=10, direction='in',labelcolor='k', length=5)
cb.set_ticks([-27,-20,-15,-10,-5,-1,0,1,5,10,15,20,27])
ax.set_facecolor('k')
lon1,lat1=m(np.min(lon),np.min(lat))
lon2,lat2=m(np.max(lon),np.max(lat))
ax.set_ylim([lat1,lat2])
ax.set_xlim([lon1,lon2])

plt.savefig('sample_V26.png',dpi=100,bbox_inches='tight')
plt.show()
