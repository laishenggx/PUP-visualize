# PUP-viusalize
Python3可视化雷达PUP数据产品(CINRAD-PUP)
* Coder: Lai Sheng @ College of Atmospheric Science, Chengdu University of Information Technology.
* E-mail: laish12@lzu.edu.cn

由于PyCINRAD的`cinrad.io.PUP`目前有BUG，暂时无法正确读取数据的经纬度信息从而画图。<br>
所以参考了[`metpy.io.Level3File`](https://unidata.github.io/MetPy/latest/examples/formats/NEXRAD_Level_3_File.html#sphx-glr-examples-formats-nexrad-level-3-file-py)雷达PUP数据接口的官方样例，编写了这个脚本。<br>

我个人不做中尺度方向，这个程序是写给我家泽儿的，其他详细的东西等我拍拖回来了再写。<br>
样例数据来自我的老东家，仅作学习使用，请勿用作其他用途。<br>
<p align="left">
    <img src="https://github.com/laishenggx/PUP-viusalize/raw/master/sample.png" alt="Sample"  width="700">
</p>
