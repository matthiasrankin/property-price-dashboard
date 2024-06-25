import streamlit as st

st.title("About")

st.markdown(
    "This dashboard was made possible through a grant given by OpenData "
    "Northern Ireland, to whom I am deeply thankful for their support. "
)

st.header("Datasets")

st.markdown(
    "Many of the datasets used are available at "
    "[the OpenDataNI website](https://admin.opendatani.gov.uk). In particular: "
)

st.markdown("- [NI House Price Index by Property Type](https://admin.opendatani.gov.uk/dataset/nihpi-by-propertytype)")
st.markdown(
    "- [Largescale Boundaries - District Electoral Areas (2012)]"
    "(https://admin.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-district-electoral-areas-2012)"
)
st.markdown(
    "- [Largescale Boundaries - Wards (2012)](https://admin.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-wards-2012)"
)

st.markdown("")

st.markdown(
    "Additional data for more granular statistics at the level of electoral areas and "
    "electoral wards was obtained from [the Department of Finance]"
    "(https://www.finance-ni.gov.uk/publications/annual-ward-district-electoral-area-and-local-government-districts-statistics)."
)

st.header("GitHub")
st.markdown(
    "The code used to create this web application and the plots within it "
    "can be found [here](https://github.com/matthiasrankin/property-price-dashboard). "
)

st.header("Feedback")
st.markdown(
    "If you have ideas of how to improve this dashboard, please consider submitting feedback by "
    "emailing nipropertypricedashboard@gmail.com."
)