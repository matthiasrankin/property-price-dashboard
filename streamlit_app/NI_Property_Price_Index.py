import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

def _switch_quarter_and_year(quarter_year: str) -> str:
    quarter, year = quarter_year.split(" ")
    return f"{year} {quarter}"


@st.cache_data
def load_property_price_index():
    property_price_index = pd.read_csv("data/ni-hpi-by-property-type-q1-2005---q1-2024.csv")
    property_price_index.rename(
        {
            "NI_Detached_Property_Price_Index": "Detached",
            "NI_SemiDetached_Property_Price_Index": "Semi-Detached",
            "NI_Terrace_Property_Price_Index": "Terrace",
            "NI_Apartment_Price_Index": "Apartment",
            "NI_Residential_Property_Price_Index": "All Residential",
        },
        axis=1,
        inplace=True
    )
    property_price_index["Year_Quarter"] = property_price_index["Quarter_Year"].apply(
        lambda x: _switch_quarter_and_year(x)
    )
    for col in ["Detached", "Semi-Detached", "Terrace", "Apartment", "All Residential"]:
        property_price_index[col] = property_price_index[col].apply(lambda x: x * 1000)
    return property_price_index


def load_electoral_area_data(excel, government_district, property_type):
    sheet_name = f"{government_district}_{property_type}"
    df = pd.read_excel(excel, sheet_name)
    df = df.drop([0, 1, 2]).reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.drop([0])
    df["Median Sale Price"] = df["Median Sale Price"].apply(lambda x: clean_price(x))

    return df


def clean_price(price):
    if price == ".":
        return float("nan")
    price = price.replace("£", "").replace(",", "")
    return int(price)


def prepare_regional_data_for_plotting(df, key):
    first_col = df[key].unique()[0]
    
    df1 = (
        df
        .query(f"`{key}` == '{first_col}'")
        .reset_index(drop=True)
        .filter(items=["Sale Year", "Median Sale Price", ])
        .rename({"Median Sale Price": first_col}, axis=1)
    )
    
    list_of_dfs = [df1]
    list_of_dfs.extend(
        [
            (
                df
                .query(f"`{key}` == '{col}'")
                .reset_index(drop=True)
                .filter(items=["Median Sale Price"])
                .rename({"Median Sale Price": col}, axis=1)
            )
            for col in [i for i in df[key].unique() if i != first_col]
        ]
    )

    return pd.concat(list_of_dfs, axis=1)


data = load_property_price_index()

st.title("NI Property Price Index")

st.markdown(
    "The graph below shows quarterly average property prices for different property "
    "types from 2005 to present. For more information on the data used, refer to "
    "[the dataset listing at opendatani.gov.uk](https://admin.opendatani.gov.uk/dataset/nihpi-by-propertytype)."
)

possible_properties = ["All Residential", "Detached", "Semi-Detached", "Terrace", "Apartment"]
property_types = st.multiselect(
    "Property Types", possible_properties, default=possible_properties
)

if property_types:
    st.line_chart(data=data, x="Year_Quarter", y=property_types)

st.header("Regional Prices (2005 - 2022)")

st.markdown("For a more granular view of average house prices over time, we can look at certain electoral areas or electoral wards.")

st.markdown(
    "**Note:** In some cases there is not enough data to provide a figure "
    "(i.e., fewer than 30 suitable property sales took place within a given area). "
    "As such, some graphs will have sections which are empty."
)

tab1, tab2 = st.tabs(["Electoral Areas", "Electoral Wards"])

property_type_mapping = {
    "Detached": "DET",
    "Semi-Detached": "SDT",
    "Terrace": "TER",
    "Apartment": "Apt",
    "All Residential": "Total"
}

government_district_mapping = {
    "Antrim and Newtownabbey": "AntrimNewtownabbey",
    "Ards and North Down": "Ards_N_Down",
    "Armagh City, Banbridge and Craigavon": "Armagh_Ban_Craig",
    "Belfast": "Belfast",
    "Causeway Coast and Glens": "Causeway",
    "Derry and Strabane": "DerryC_Strabane",
    "Fermanagh and Omagh": "Fermanagh_Omagh",
    "Lisburn and Castlereagh": "Lisburn_Castlereagh",
    "Mid and East Antrim": "Mid_E_Antrim",
    "Mid Ulster": "Mid_Ulster",
    "Newry, Mourne and Down": "Newry_M_Down"
}

with tab1:
    electoral_area_annual = pd.ExcelFile(
        "data/properties/District Electoral Area Annual Price Statistics Property Types_Frozen.xlsx"
    )

    property_type = st.selectbox("Type of Property", possible_properties)

    mapped_property_type = property_type_mapping[property_type]

    district = st.selectbox("Government District", government_district_mapping.keys())
    
    mapped_government_district = government_district_mapping[district]
    
    sheet_name = f"{mapped_government_district}_{mapped_property_type}"
    
    df = load_electoral_area_data(electoral_area_annual, mapped_government_district, mapped_property_type)
    
    possible_electoral_areas = df["District Electoral Area (2014)"].unique().tolist()
    
    electoral_areas = st.multiselect("Electoral Areas", possible_electoral_areas, default=possible_electoral_areas)
    
    if electoral_areas:
        filtered_df = df.query(f"`District Electoral Area (2014)` in {electoral_areas}")
        plot_data = prepare_regional_data_for_plotting(filtered_df, key="District Electoral Area (2014)")
        
        st.line_chart(data=plot_data, x="Sale Year", y=electoral_areas)

with tab2:
    electoral_area_annual = pd.ExcelFile(
        "data/properties/Electoral Ward Annual Price Statistics Property Types_Frozen.xlsx"
    )

    property_type = st.selectbox("Type of Property ", possible_properties)

    mapped_property_type = property_type_mapping[property_type]

    district = st.selectbox("Government District ", government_district_mapping.keys())
    
    mapped_government_district = government_district_mapping[district]
    
    sheet_name = f"{mapped_government_district}_{mapped_property_type}"
    
    df = load_electoral_area_data(electoral_area_annual, mapped_government_district, mapped_property_type)
    
    possible_electoral_wards = df["Electoral Ward (2014)"].unique().tolist()
    
    electoral_wards = st.multiselect("Electoral Wards", possible_electoral_wards, default=[])
    
    if electoral_wards:
        filtered_df = df.query(f"`Electoral Ward (2014)` in {electoral_wards}")
        plot_data = prepare_regional_data_for_plotting(filtered_df, key="Electoral Ward (2014)")
        
        st.line_chart(data=plot_data, x="Sale Year", y=electoral_wards)
