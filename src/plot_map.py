import plotly.graph_objects as go
import json

with open("route_data.json") as f:
    hops = json.load(f)

lats, lons, texts = [], [], []

for hop in hops:
    if hop["lat"] is not None and hop["lon"] is not None:
        lats.append(hop["lat"])
        lons.append(hop["lon"])
        texts.append(f"{hop['ip']}<br>{hop['city']}, {hop['region']}, {hop['country']}")

fig = go.Figure(go.Scattergeo(
    lon = lons,
    lat = lats,
    text = texts,
    mode = 'lines+markers',
    line = dict(width = 2, color = 'blue'),
    marker = dict(size = 6, color = 'red')
))

fig.update_layout(
    title = 'Traceroute Path',
    geo = dict(
        projection_type = 'natural earth',
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "rgb(200, 200, 200)",
    ),
)

fig.show()

