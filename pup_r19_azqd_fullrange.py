import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from metpy.io.nexrad import Level3File
import matplotlib.colors as cmx
import datetime

def r_color_PUP():
    import matplotlib.colors as colors
    cdict = [(0/ 255, 172 / 255, 164/ 255), (192 / 255, 192 / 255, 255 / 255), (122 / 255, 114 / 255, 238 / 255)
        , (30 / 255, 38 / 255, 208 / 255), (166 / 255, 252 / 255, 168 / 255), (0 / 255, 234 / 255,0 / 255)
             , (16 / 255, 146 / 255,26/ 255), (252/ 255, 254 / 255,100 / 255), (200 / 255, 200 / 255,2/ 255)
             , (140 / 255, 140 / 255,0 / 255), (254 / 255, 172 / 255,172 / 255), (255 / 255, 100 / 255,92 / 255)
             , (238 / 255, 2 / 255,48 / 255), (212 / 255, 142 / 255,255 / 255),(170 / 255, 36 / 255, 250 / 255)]
    r_cmap = colors.ListedColormap(cdict, 'indexed')
    return r_cmap,cmx.Normalize(-5, 70)

# Open the file
f = Level3File('C:\\pyproj\\cinrad\\pupdata\\R\\19\\20170330.084822.02.19.778')

datadict = f.sym_block[0][0]
data = np.ma.array(datadict['data'])
data[data == 0] = np.ma.masked
data = np.ma.masked_invalid(f.map_data(data))

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
lon_leftup=106.3;lat_leftup=25.35
lon_rightdown=107.7;lat_rightdown=24.35
# m = Basemap(projection='cyl', llcrnrlat=lat_rightdown, urcrnrlat=lat_leftup, llcrnrlon=lon_leftup, urcrnrlon=lon_rightdown, resolution='l')
width = 2800000; lon_0 = sta_lon; lat_0 = sta_lat
m = Basemap(width=width,height=width,projection='aeqd',
            lat_0=lat_0,lon_0=lon_0)
m.readshapefile('C:\\dt\\county_2004', 'sf', color='w',linewidth=0.6)
m.readshapefile('C:\\dt\\dijishi_2004', 'aa', drawbounds=False)
for info, shape in zip(m.aa_info, m.aa):
    if info['LEVEL2_ID'] == 274:
        x, y = zip(*shape)
        m.plot(x, y, marker=None, color='red', linewidth=0.8)

r_cmap,r_norm=r_color_PUP()
lons,lats=m(lon,lat)
cf1=m.pcolormesh(lons, lats, data,cmap=r_cmap,norm=r_norm)

for cir in [50,100,150,200,230]:#画等距离圈
    cir_lon=lon[:,np.where(rng==cir)].flatten()
    cir_lat = lat[:, np.where(rng == cir)].flatten()
    cir_lon,cir_lat=m(cir_lon,cir_lat)
    m.plot(cir_lon,cir_lat,'w',linewidth=0.8)

for az_line in np.arange(30,360+30,30):
    az_lon=[sta_lon,lon[np.where(np.ceil(az)==az_line),-1]]
    az_lat=[sta_lat,lat[np.where(np.ceil(az)==az_line),-1]]
    az_lon,az_lat=m(az_lon,az_lat)
    m.plot(az_lon, az_lat, 'w', linewidth=0.8)

vt=f.metadata['vol_time']+datetime.timedelta(hours=8)

ax.text(1, 1.05,'基本反射率(R 19)\n仰角:%3.1f$^o$ MAX:%2ddBz'%(f.metadata['el_angle'],f.metadata['max']),
        transform=ax.transAxes, fontdict={'family':'SimHei','size':13,'color':'r'},horizontalalignment='right')
ax.text(1, 1.015,'%4d年%02d月%02d日 %02d:%02d:%02d(BJT)'%(vt.year,vt.month,vt.day,vt.hour,vt.minute,vt.second),
        transform=ax.transAxes, fontdict={'family':'SimHei','size':13,'color':'blue'},horizontalalignment='right')
ax.text(1.07, 0.91,'dBz', transform=ax.transAxes,fontsize=12)
ax.text(0.005, 1.015, '站点:河池(Z9778)\n雷达：CINRAD/SB(%6.2f$^o$E/%5.2f$^o$N,1047.7m)\n分辨率:1$^o$x1km 数据范围:230km\n扫描模式:VCP21-Precipitation'
        %(sta_lon,sta_lat), transform=ax.transAxes,fontdict={'family':'SimHei','size':13,'color':'k'})

cb=fig.colorbar(cf1,ax=ax,pad=0.02,shrink=0.7,aspect=20)
cb.ax.tick_params(labelsize=10, direction='in',labelcolor='k', length=0)
cb.set_ticks(np.arange(-5,70,5))
ax.set_facecolor('k')
lon1,lat1=m(np.min(lon),np.min(lat))
lon2,lat2=m(np.max(lon),np.max(lat))
ax.set_ylim([lat1,lat2])
ax.set_xlim([lon1,lon2])

# plt.show()
plt.savefig('111.png',dpi=300,bbox_inches='tight')