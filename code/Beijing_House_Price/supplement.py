import plotly
import plotly.graph_objects as go
import numpy as np

year = [2011,2012,2013,2014,2015,2016,2017,2018]
new_house   = [2596.4,1627.5,1736.5,1304,1199.2,1209.3,1226.7,1233.6]
built_house = [1316.1,1522.7,1692,1804.3,1378.2,1275.2,604,731.2]
sold_house  = [1035,1483.4,1363.7,1141.3,1127.3,993.5,612.8,526.8]

building_house = [1280.3,1385.1,1429.6,929.3,750.3,684.4,1307.1,1809.5]
selling_house =[281.1,320.4,648.7,1311.7,1562.6,1844.3,1835.5,2039.9]

def plot_bar():

  data = [
    go.Bar(x=year, y=new_house, name="新开工"),
    go.Bar(x=year, y=built_house, name="竣工"),
    go.Bar(x=year, y=sold_house, name="售出"),
    go.Scatter(x=year, y=building_house, name="估算在建"),
    go.Scatter(x=year, y=selling_house, name="估算待售"),
    ]

  layout = go.Layout(
    title='2011-2018北京住房供给',
    yaxis=dict(
      title='建筑面积（万平米）')
    )

  fig = go.Figure(
    data=data,
    layout=layout,
  )

  fig.update_layout(legend_orientation="h")
  
  plotly.offline.plot(fig, filename='supplement.html', include_plotlyjs=False)
  plotly.offline.plot(fig, filename='file.html')

if __name__=="__main__":
  plot_bar()


