# PUP-viusalize
Python3可视化雷达PUP数据产品(CINRAD-PUP)
* Coder: Lai Sheng @ College of Atmospheric Science, Chengdu University of Information Technology.
* E-mail: laish12@lzu.edu.cn

由于[PyCINRAD](https://github.com/CyanideCN/PyCINRAD)的`cinrad.io.PUP`目前有BUG，暂时无法正确生成数据的经纬度信息从而画图。<br>
所以我参考了[`metpy.io.Level3File`](https://unidata.github.io/MetPy/latest/examples/formats/NEXRAD_Level_3_File.html#sphx-glr-examples-formats-nexrad-level-3-file-py)雷达PUP数据接口的官方样例，编写了这个脚本。<br>
<p align="left">
    <img src="https://github.com/laishenggx/PUP-viusalize/raw/master/sample.png" alt="Sample"  width="700">
</p>

## 坐标变换
Metpy的官方样例中，将PUP产品文件读出后，做了如下变换，将极坐标投影到了平面直角X-Y坐标系中：
```
# Convert az,range to x,y
xlocs = rng * np.sin(np.deg2rad(az[:, np.newaxis]))
ylocs = rng * np.cos(np.deg2rad(az[:, np.newaxis]))
```
`xlocs`和`ylocs`是某点到雷达的经向和纬向距离<br>
这样根据雷达经纬度信息，还有经向和纬向距离，很容易就可以算图上每一点的距离经纬度：
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
绘图使用的是`basemap(1.2.0)`和`matplotlib(3.0.3)`<br>
投影选择`等距方位投影(Azimuthal Equidistant Projection)`，用这个投影时1个纬距和1个经距是相等的，不然等距离圈不是正圆形<br>
地图shp文件请移步气象家园搜索下载<br>

## 日后更新计划
我个人不做中尺度方向(被老板狠心抛弃QAQ)，这个程序是写给泽儿(我GF可爱多)的。<br>
目前仅做了基本反射率，基本速度还有就是将数据输出成网格的，她让我弄我再弄吧~<br>
