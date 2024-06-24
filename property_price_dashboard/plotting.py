"""Functions for producing plots used in the dashboard."""

import pandas as pd
import plotly_express as px
# import folium
# import branca.colormap as cm


def plot_chloropleth(
    gdf,
    region_key="FinalR_DEA",
    price_key="median_sale_price_total",
    mapped_region_key="District Electoral Ward",
    mapped_price_key="Median Sale Price (All Residential)"
):
    """
    Plot chloropleth map to show average property price in regions of Northern Ireland.

    Parameters:
    -----------
    gdf: geopandas.DataFrame
    region_key: str, default="FinalR_DEA"
    price_key: str, default="median_sale_price_total"
    mapped_region_key: str, default="District Electoral Ward",
    mapped_price_key: str, default="Median Sale Price (All Residential)"

    Returns:
    --------
    HTML for `plotly_express.chloropleth_mapbox`.
    """
    gdf.set_index(region_key, inplace=True)
    gdf.crs = "EPSG:4326"
    gdf[price_key] = gdf[price_key].apply(pd.to_numeric)
    x_mean = gdf.centroid.x.mean()
    y_mean = gdf.centroid.y.mean()
    # mean_longitude = gdf.centroid.x
    # mean_latitude = gdf.centroid.y

    hover_name = list(gdf.index)

    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf["geometry"],
        locations=gdf.index,
        color=price_key,
        center={"lat": y_mean, "lon": x_mean},
        mapbox_style="carto-positron",
        zoom=7,
        opacity=0.5,
        color_continuous_scale="viridis",
        labels={
            price_key: mapped_price_key,
            region_key: mapped_region_key
        },
        hover_name=hover_name
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig.to_html()
