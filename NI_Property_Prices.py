import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import streamlit.components.v1 as components

st.set_page_config(layout="wide")


def create_folium_chloropleth(gdf, key):
    my_map = folium.Map(location=[y_mean, x_mean], zoom_start=9, tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(my_map)
    my_scale = (gdf['price'].quantile((0,0.25,0.5,0.75,0.9,0.98,1))).tolist()
    folium.Choropleth( 
        geo_data=gdf,
        name='Choropleth',
        data=gdf,
        columns=['CountyName','price'],
        key_on=f"feature.properties.{key}",
        fill_color='YlGnBu',
        threshold_scale=my_scale,
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name='Average property price / £',
        smooth_factor=0
    ).add_to(my_map)
    
    for _, row in gdf.iterrows():
        marker = folium.Marker(
            location=[row["mean_latitude"], row["mean_longitude"]],
            tooltip=row["CountyName"],
            popup=f'<h3>{row["CountyName"]}</h3><br><a> <b>Average Property Price:</b> £{int(round(row["price"], 0))}</a>'
        ).add_to(my_map)
        
    return my_map


region_shapefile_mapping = {
    "County": "data/shapefiles/OSNI_Open_Data_-_Largescale_Boundaries_-_County_Boundaries_.geojson",
    "Electoral Ward": "data/shapefiles/OSNI_Open_Data_-_Largescale_Boundaries_-_Wards_(2012).geojson"
}

st.title("NI Property Price Dashboard")

st.markdown(
    "The purpose of this dashboard is to give an insight into property prices in Northern Ireland. "
    "The price of a property can depend on a number of factors "
)

st.header("Property Price By Area")

property_types = st.multiselect("Types of Property", ["Detached", "Semi-Detached", "Bungalow", "Apartment"])
region_type = st.selectbox("Region Choice", ["County", "Electoral Ward", "Electoral Area"])

shapefile_path = region_shapefile_mapping[region_type]


gdf = gpd.read_file(shapefile_path)
gdf["CountyName"] = gdf["CountyName"].apply(lambda x: x.lower().capitalize())
properties = pd.read_csv("data/properties/cleaned_properties.csv", low_memory=False)
price_by_region = properties.groupby("region", as_index=False)["price"].mean()

gdf = gdf.merge(price_by_region, left_on="CountyName", right_on="region", how="inner")

x_mean = gdf.centroid.x.mean()
y_mean = gdf.centroid.y.mean()
gdf["mean_longitude"]= gdf.centroid.x
gdf["mean_latitude"] = gdf.centroid.y

my_map = create_folium_chloropleth(gdf, key="CountyName")

with st.container():
    components.html(my_map._repr_html_(), width=1000, height=1000)
