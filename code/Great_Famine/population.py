import plotly
import plotly.graph_objects as go
import numpy as np

year = list(reversed(range(1950, 1971)))
population = [82992,80671,78534,76368,74542,72538,70499,69172,67296,65859,66207,67207,65994,64653,62828,61465,60266,58796,57482,56300,55196]
birth_rate = [33.59,34.25,35.75,34.12,35.21,38.00,39.34,43.60,37.22,18.13,20.86,24.78,29.22,34.03,31.90,32.60,37.97,37.00,37.00,37.80,37.00]
death_rate = [7.64,8.06,8.25,8.47,8.87,9.50,11.56,10.10,10.08,14.33,25.43,14.59,11.98,10.80,11.40,12.28,13.18,14.00,17.00,17.80,18.00]
food_production = [23995.50,21097.30,20906.00,21782.30,21400.90,19452.50,18088.70,16574.10,15441.40,13650.90,14385.70,16969.20,19766.30,19504.50,19275.60,18394.60,16952.80,16684.10,16392.50,14368.90,13212.90]
avg_food = np.array(food_production) / np.array(population)

def plot_bar():

  base=50000
  population_plot = np.array(population) - base
  data = [go.Bar(x=year, y=population_plot, base=50000, marker_color='indianred')]

  layout = go.Layout(
    title='1950-1970年中国人口数',
    yaxis=dict(
      title='人口数（万）')
    )

  fig = go.Figure(
    data=data,
    layout=layout,
  )

  plotly.offline.plot(fig, filename='population.html', include_plotlyjs=False)
  plotly.offline.plot(fig, filename='file.html')

if __name__=="__main__":
  plot_bar()


