"""Demo app

Ref:
- https://docs.streamlit.io/en/stable/getting_started.html
- https://deckgl.readthedocs.io/en/latest/gallery/geojson_layer.html
"""

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import geopandas as gpd


st.title("My first app")

st.write("Here's our first attempt at using data to create a table:")
st.write(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)

df_trial = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

df_trial

# another way to display df
chart_data = df_trial

st.line_chart(chart_data)

# map
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)

st.map(map_data)

# checkbox
if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    chart_data

# selectbox
option = st.selectbox("Which number do you like best?", df_trial["first column"])

"You selected: ", option

# button
left_column, right_column = st.beta_columns(2)
pressed = left_column.button("Press me?")
if pressed:
    right_column.write("Woohoo!")

# expander
expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

# map geojson layer
# ref: https://deckgl.readthedocs.io/en/latest/gallery/geojson_layer.html
DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
LAND_COVER = [
    [[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]
]

INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=49.254, longitude=-123.13, zoom=11, max_zoom=16, pitch=45, bearing=0
)

polygon = pdk.Layer(
    "PolygonLayer",
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="-",
    get_fill_color=[0, 0, 0, 20],
)

geojson = pdk.Layer(
    "GeoJsonLayer",
    DATA_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.valuePerSqm / 20",
    get_fill_color="[255, 255, properties.growth * 255]",
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[polygon, geojson], initial_view_state=INITIAL_VIEW_STATE)
st.pydeck_chart(r)



########################################################################################################


YEAR = 2017
MONTH = 5
VARIABLE_TO_PREDICT = "Airbnb_Number"

url_geo = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_geo.json"

df_geo = gpd.read_file(url_geo)
df_geo.set_index("Tag", inplace=True)

url_data = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_{}_{:02d}.csv".format(YEAR, MONTH)

df = pd.read_csv(url_data)
df.set_index("Tag", inplace=True)

df_geo["Target"] = df[VARIABLE_TO_PREDICT]

df_geo