"""Demo app

Ref:
- https://docs.streamlit.io/en/stable/getting_started.html
- https://deckgl.readthedocs.io/en/latest/gallery/geojson_layer.html
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import geopandas as gpd
import json
from __version__ import version

YEAR = 2017
MONTH = 5
URL_GEO = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_geo.json"
URL_DATA = "https://raw.githubusercontent.com/egregorimar/urbana/master/data/interim/sections_{}_{:02d}.csv".format(
    YEAR, MONTH
)
INITIAL_LAT = 41.38879
INITIAL_LON = 2.15899
CITY_NAME = "Barcelona"


st.title(f"InsideAirBnB data in {CITY_NAME}")


# data
@st.cache(allow_output_mutation=True)
def get_data(url_geo: str, url_data: str) -> dict:
    """Load and merge data.

    Returns:
        dict: {"describe": pandas decribe() of the features,
               "geojson": geojson formatted dictionary}
    """

    df_geo = gpd.read_file(url_geo)
    df_geo.set_index("Tag", inplace=True)

    df = pd.read_csv(url_data)
    df.set_index("Tag", inplace=True)

    full_df = df_geo.merge(df, on="Tag")

    return {
        "describe": df.describe().to_dict(),
        "geojson": json.loads(full_df.to_json()),
    }


city_data = get_data(url_geo=URL_GEO, url_data=URL_DATA)
features = city_data["describe"].keys()

# select features for elevation & color
option_elevation = st.selectbox(
    "Which feature do you like to visualize as elevation?", features
)
option_color = st.selectbox(
    "Which feature do you like to visualize as color?", features
)

# plot
INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=INITIAL_LAT,
    longitude=INITIAL_LON,
    zoom=11,
    max_zoom=16,
    pitch=45,
    bearing=0,
)

geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    data=city_data["geojson"],
    # opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation=f"properties.{option_elevation}",
    elevation_scale=max(v["max"] for v in city_data["describe"].values())
    / city_data["describe"][option_elevation]["max"],
    get_fill_color=f"""[255, (1 - properties.{option_color} / {city_data["describe"][option_color]["max"]}) * 255, 255]""",
    get_line_color=[255, 255, 255],
)

st.pydeck_chart(pdk.Deck(layers=[geojson_layer], initial_view_state=INITIAL_VIEW_STATE))

# credits and version
st.markdown(
    f"Based on [streamlit-urbana](https://github.com/pareyesv/streamlit-urbana), v{version}"
)
