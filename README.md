# bokeh-dash
###### An Interactive Dashboard built using bokeh
###### Required Libraries:
```
numpy: pip install numpy
pandas: pip install pandas
geopandas: pip install geopandas
shapely: pip install shapely
bokeh: pip install bokeh
```
###### Intructions: Get inside the folder and execute the following command.
```
bokeh serve --show teal.py
```
###### Description
- The idea is to visualize the variation in number of **deeds** w.r.t time for Delhi region.
- Since bokeh cannot deal with shape files **.shp** directly, requires processing **.shp** files using **geopandas** and **shapely**.
