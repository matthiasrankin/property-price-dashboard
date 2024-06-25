import streamlit as st
import streamlit.components.v1 as components
import json


region_shapefile_and_key_mapping = {
    "District Electoral Area": {
        "shapefile": "data/chloropleth_data/electoral_areas.csv",
        "region_key": "FinalR_DEA"
    },
    "Electoral Ward": {
        "shapefile": "data/chloropleth_data/electoral_wards.csv",
        "region_key": "WARDNAME"
    }
}

property_type_mapping = {
    "All Residential": "median_sale_price_total",
    "Detached": "median_sale_price_det",
    "Semi-Detached": "median_sale_price_sdt",
    "Terrace": "median_sale_price_ter",
    "Apartment": "median_sale_price_apt"
}

st.title("NI Property Price By Region")

st.markdown(
    "The price of a property depends on a number of factors specific to the property itself, "
    "and we should not rely solely on regional averages to obtain a fair valuation of a house. "
    "Still, it is sometimes of interest to see how average prices change based on the surrounding area."
)

st.markdown(
    "The graphs shown here aim to provide a comparison between average house prices in different areas of "
    "Northern Ireland. This is done at both the District Electoral Area level, as well as that of Electoral Wards. "
    "The pricing data is taken from 2022 averages by property type."
)

st.markdown(
    "If fewer than 30 suitable property sales occurred within an area, no value is given. "
    "This is why some regions are not represented when filtering to electoral wards, for example."
)

property_type = st.selectbox("Types of Property", list(property_type_mapping.keys()))
region_type = st.selectbox("Region Choice", list(region_shapefile_and_key_mapping.keys()))

with open(f"static/{property_type.replace(' ', '_').lower()}_chloropleths.json", "r", encoding="utf-8") as file_:
    chloropleths = json.load(file_)

my_map = chloropleths[region_type]

with st.container():
    components.html(my_map, width=1450, height=1450)
