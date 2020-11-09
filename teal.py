from bokeh.io import curdoc
from bokeh.plotting import figure
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, LinearColorMapper, Slider, Button, RadioButtonGroup
from bokeh.palettes import Blues
from bokeh.layouts import column,row
import pandas as pd
import geopandas as gpd
import numpy as np
import time

Blues[9] = list(Blues[9])
Blues[9].reverse()

'''
Add the location of the dataset and shapefiles. (Example given)
'''
dataset = r'doris_deeds.csv'
shapefile = r'delhi_districts/delhi_districts.shp'


def get(geom):    
     if type(geom) is Polygon:       
             return [list(geom.exterior.coords.xy[0]),list(geom.exterior.coords.xy[1])]
     elif type(geom) is MultiPolygon:        
             polygons = list(geom)
             X = list(polygons[0].exterior.coords.xy[0])
             X.append(np.nan)
             X.extend(list(polygons[1].exterior.coords.xy[0]))
             Y = list(polygons[0].exterior.coords.xy[1])
             Y.append(np.nan)
             Y.extend(list(polygons[1].exterior.coords.xy[1]))
             return [X,Y]
def center(geom,t):   
    if t=='x': return geom.centroid.x
    elif t=='y': return geom.centroid.y

def callback(): 
    initial = 0
    final = len(df_temp)-1
    while(initial <= final):    
        radio_button_group.active = initial
        time.sleep(4)
        initial = initial + 1

def call(attr,old,new): 
    if new==0:  
        count = [(dt[dt['district']==d]['reg_date']).sum() for d in dis]
        new_color_mapper = LinearColorMapper(low=min(count),high=max(count),palette=Blues[9][1:])
    else:   
        active = new
        year = int(df_temp['dates'].iloc[active])
        count = [dt[(dt['district']==d) & (dt['year']==year)]['reg_date'].sum() for d in dis]
        new_color_mapper = LinearColorMapper(low=min(count),high=max(count),palette=Blues[9][1:])
    p1.glyph.update(fill_color={'field':'RECORDS','transform':new_color_mapper})
    data.data = {'DISTRICT':dis,'RECORDS':count,'X':list(coords.apply(lambda x:x[0])),'Y':list(coords.apply(lambda x:x[1])),'CENTER_X':cen_x,'CENTER_Y':cen_y}


points = gpd.read_file(shapefile)
dt = pd.read_csv(dataset)[['district','reg_date']]
dt['year'] = pd.to_datetime(dt['reg_date']).dt.year
dt = dt.groupby(['district','year'],as_index=False).count()
dis = list(points['DIST_NM'])
count = [(dt[dt['district']==d]['reg_date']).sum() for d in dis]
coords = points['geometry'].apply(get)
cen_x = list(points.apply(lambda row:center(row['geometry'],'x'),axis=1))
cen_y = list(points.apply(lambda row:center(row['geometry'],'y'),axis=1))
dates = ['ALL']
temp = list(pd.unique(dt['year']).astype(str))
temp.sort()
dates.extend(temp)
df_temp = pd.DataFrame()
df_temp['dates'] = dates
hover_tool = HoverTool(tooltips=[
		('District','@DISTRICT'),
		('Number of Deeds','@RECORDS')
])
color_mapper = LinearColorMapper(low=min(count),high=max(count),palette=Blues[9][1:])
radio_button_group = RadioButtonGroup(labels=dates,active=0,margin=(0,0,0,10))
radio_button_group.on_change('active', call)
button_widget = Button(label='Play',margin=(0,0,0,120),width=100)
button_widget.on_click(callback)
data = ColumnDataSource(data={'DISTRICT':dis,'RECORDS':count,'X':list(coords.apply(lambda x:x[0])),'Y':list(coords.apply(lambda x:x[1])),'CENTER_X':cen_x,'CENTER_Y':cen_y})
labels = LabelSet(x='CENTER_X',y='CENTER_Y',source=data,text='DISTRICT', level='glyph',render_mode='canvas',text_align='center',text_font_style='bold',text_font_size='7.5pt',text_baseline='bottom',text_alpha=1.0,text_line_height=1.2)
plot = figure(title='Districts of Delhi',tools=[hover_tool],sizing_mode='scale_width',margin=(0,0,0,360))
p1=plot.patches('X','Y',source=data,line_color='black',line_width=0.2,fill_alpha=0.4,fill_color={'field':'RECORDS','transform':color_mapper})
p2=plot.circle('CENTER_X','CENTER_Y',source=data,size=2,alpha=0,color='black')
plot.add_layout(p1)
plot.add_layout(p2)
plot.add_layout(labels)
layout = column(row(button_widget,radio_button_group),plot)
curdoc().add_root(layout)
