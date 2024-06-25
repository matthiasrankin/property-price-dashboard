import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (5, 2.5)

cleaned_properties = pd.read_csv("data/properties/cleaned_properties.csv")

property_type_mapping = {
    "All Residential": "",
    "Detached": "is_detached",
    "Semi-Detached": "is_semidetached",
    "Terrace": "is_terrace",
    "Apartment": "is_apartment_or_flat"
}

st.title("Property Price Distributions")

st.markdown(
    "Between September 2022 and April 2023, data was gathered from property websites on the asking "
    "price for different properties on the market at that time. This data can be used to gain a sense "
    "of the distribution of prices in the market."
)

st.markdown(
    "**Note:** Since this data only takes asking prices into account, it does not perfectly represent "
    "real property market prices. Additionally, due to the strong right skew of the data, prices above "
    "the 99th percentile have been clipped to the 99th percentile value."
)

property_type = st.selectbox("Property Type", list(property_type_mapping.keys()))

if property_type == "All Residential":
    plot_data = cleaned_properties.copy()
else:
    plot_data = cleaned_properties.query(f"{property_type_mapping[property_type]} == True").copy()

plot_data["price"].clip(0, np.quantile(plot_data["price"], 0.99), inplace=True)

seaborn_fig = sns.histplot(data=plot_data, x="price")
seaborn_fig.set_xlabel("Price / £",fontdict={"size": 6})
seaborn_fig.set_ylabel("No. Properties", fontdict={"size": 6})
seaborn_fig.tick_params(axis="x", labelrotation=45,labelsize=6)
seaborn_fig.tick_params(axis="y", labelsize=6)
seaborn_fig.ticklabel_format(style="plain")

if property_type:
    st.pyplot(seaborn_fig.get_figure())


