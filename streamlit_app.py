"""Demo app

Ref:
- https://docs.streamlit.io/en/stable/getting_started.html
- https://deckgl.readthedocs.io/en/latest/gallery/geojson_layer.html
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
from __version__ import version

st.title("InsideAirBnB data for Barcelona")


# data
@st.cache(allow_output_mutation=True)
def get_data():
    """Load and merge data.

    Returns:
        dict: {"describe": pandas decribe() of the features,
               "geojson": geojson formatted dictionary}
    """

    import geopandas as gpd
    import json

    YEAR = 2017
    MONTH = 5
    URL_GEO = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_geo.json"
    URL_DATA = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_{}_{:02d}.csv".format(
        YEAR, MONTH
    )

    df_geo = gpd.read_file(URL_GEO)
    df_geo.set_index("Tag", inplace=True)

    df = pd.read_csv(URL_DATA)
    df.set_index("Tag", inplace=True)

    full_df = df_geo.merge(df, on="Tag")

    return {"describe": df.describe(), "geojson": json.loads(full_df.to_json())}


bcn_data = get_data()
bcngeojson = bcn_data["geojson"]
features = bcn_data["describe"].columns.values

# select features for elevation & color
option_elevation = st.selectbox(
    "Which feature do you like to visualize as elevation?", features
)
option_color = st.selectbox(
    "Which feature do you like to visualize as color?", features
)

# plot
BCN_INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=41.38879, longitude=2.15899, zoom=11, max_zoom=16, pitch=45, bearing=0
)

bcngeojson = pdk.Layer(
    "GeoJsonLayer",
    data=bcngeojson,
    # opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation=f"properties.{option_elevation}",
    elevation_scale=bcn_data["describe"].loc["max"].max()
    / bcn_data["describe"][option_elevation]["max"],
    get_fill_color=f"""[255, (1 - properties.{option_color} / {bcn_data["describe"][option_color]["max"]}) * 255, 255]""",
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[bcngeojson], initial_view_state=BCN_INITIAL_VIEW_STATE)
st.pydeck_chart(r)

# credits and version
st.markdown(
    f"Based on [streamlit-urbana](https://github.com/pareyesv/streamlit-urbana), v{version}"
)
