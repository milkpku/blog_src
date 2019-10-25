import plotly
import plotly.graph_objects as go
import numpy as np

def plot():

  x = np.arange(0, 4, 0.1)

  margin_cost = x + 0.1
  margin_prof = 4 - x
  dis_margin_prof = margin_prof / 4

  data = [
    go.Scatter(x=x, y=margin_cost, name='边际成本曲线'),
    go.Scatter(x=x, y=dis_margin_prof, name="大锅饭边际收益曲线"),
    go.Scatter(x=x, y=margin_prof, name="正常边际收益曲线"),
  ]

  annotations = [
    go.layout.Annotation(
      x=1.95, y=2.05, text="正常平衡点", 
      showarrow=True, arrowhead=7, ax=0, ay=-40),
    go.layout.Annotation(
      x=0.72, y=0.82, text="大锅饭平衡点", 
      showarrow=True, arrowhead=7, ax=0, ay=-40),
  ]

  layout = go.Layout(
    title='农民生产均衡图',
    xaxis=dict(title='劳动投入'),
    yaxis=dict(title='效用'),
    annotations=annotations
  )

  fig = go.Figure(
    data=data,
    layout=layout,
  )

  div_block=plotly.offline.plot(fig, filename='equilibrium.html', include_plotlyjs=False)
  plotly.offline.plot(fig, filename='file.html')


if __name__=="__main__":
  plot()