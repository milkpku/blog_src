import plotly
import plotly.graph_objects as go
import numpy as np

year_gdp = [2011,2012,2013,2014,2015,2016,2017,2018]
debt_gdp   = [27.875, 29.949, 33.477, 36.086, 39.390, 45.079, 49.350, 53.186]
year_income = [2012, 2013, 2014, 2015, 2016, 2017]
debt_income = [71.1, 77.9, 81.8, 86.4, 97.3, 107.2]

def plot_bar():

  data = [
    go.Bar(x=year_income, y=debt_income, name="家庭债务占可支配收入百分比"),
    go.Scatter(x=year_gdp, y=debt_gdp, name="家庭债务占GDP百分比"),
    ]

  layout = go.Layout(
    title='2011-2018中国家庭债务变化',
    yaxis=dict(
      title='%')
    )

  fig = go.Figure(
    data=data,
    layout=layout,
  )

  fig.update_layout(legend_orientation="h")
  
  plotly.offline.plot(fig, filename='debt.html', include_plotlyjs=False)
  plotly.offline.plot(fig, filename='file.html')

if __name__=="__main__":
  plot_bar()


