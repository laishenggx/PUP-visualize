# PUP-visualize
Python3可视化雷达PUP数据产品(CINRAD-PUP)
* Coder: Lai Sheng @ College of Atmospheric Science, Chengdu University of Information Technology.

参考[`metpy.io.Level3File`](https://unidata.github.io/MetPy/latest/examples/formats/NEXRAD_Level_3_File.html#sphx-glr-examples-formats-nexrad-level-3-file-py)雷达PUP数据接口的官方样例，编写了这个脚本。<br>
[PyCINRAD](https://github.com/CyanideCN/PyCINRAD)中的`cinrad.io.PUP`坐标映射的BUG已经修复。<br>

<p align="left">
    <img src="https://github.com/laishenggx/PUP-viusalize/raw/master/sample.png" alt="Sample"  width="700">
</p>
<p align="left">
    <img src="https://github.com/laishenggx/PUP-viusalize/raw/master/sample_V26.png" alt="Sample"  width="700">
</p>


## 雷达数据存储方式

请看PUP雷达文件格式说明。

## 坐标变换
Metpy的官方样例中，将PUP产品文件雷达体扫的方位角`az`和极径`rng`读出后，把极坐标投影到了平面直角X-Y坐标系中：<br>
```
# Convert az,range to x,y
xlocs = rng * np.sin(np.deg2rad(az[:, np.newaxis]))
ylocs = rng * np.cos(np.deg2rad(az[:, np.newaxis]))
```
`xlocs`和`ylocs`是某点到雷达的经向和纬向距离<br>
这样根据雷达经纬度信息，还有经向和纬向距离，很容易就可以算图上每一点的距离经纬度：<br>
```
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
```
## 绘图
绘图使用的是`basemap(1.2.0)`和`matplotlib(3.0.3)`，也可以改用`cartopy`<br>
### 等距离圈
画等距离圈是直接根据雷达文件读取出的极径`rng`确定的<br>
做法大致是用`np.where`确定相应等距离圈的下标位置，然后把`rng==距离`的所有点的坐标切片出来<br>
最后用`plot`将点连成线形成等距离圈<br>
```
for cir in [50,100,150,200,230]:#画等距离圈
    cir_lon=lon[:,np.where(rng==cir)].flatten()
    cir_lat = lat[:, np.where(rng == cir)].flatten()
    cir_lon,cir_lat=m(cir_lon,cir_lat)
    m.plot(cir_lon,cir_lat,'w',linewidth=0.8)
```
### 方位角线
画方位角线也是类似等距离圈的做法，但是画线只用了两个点<br>
一个是雷达站点的经纬度(可以从文件中读取)，另一个是径向上最远的一个点<br>
```
for az_line in np.arange(30,360+30,30):
    az_lon=[sta_lon,lon[np.where(np.ceil(az)==az_line),-1]]
    az_lat=[sta_lat,lat[np.where(np.ceil(az)==az_line),-1]]
    az_lon,az_lat=m(az_lon,az_lat)
    m.plot(az_lon, az_lat, 'w', linewidth=0.8)
```
### 投影
投影选择`等距方位投影(Azimuthal Equidistant Projection)`<br>
此时1个纬距和1个经距是相等的，否则等距离圈不是正圆形<br>
(下图是等经度投影cyl，原因自己体会思考吧，发现蛮多人都没发现到这个问题，直接等经纬度投影上边画圆)<br>
<p align="left">
    <img src="https://github.com/laishenggx/PUP-viusalize/raw/master/sample_cyl.png" alt="Sample"  width="700">
</p>
地图shp文件请移步气象家园搜索下载<br>
