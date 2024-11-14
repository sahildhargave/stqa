import streamlit as st


def render_powerbi_page_1():
    st.write("Power BI Visualization 1:")
    st.components.v1.iframe(
        "https://app.powerbi.com/view?r=YOUR_REPORT_ID", width=800, height=600
    )


def render_powerbi_page_2():
    st.write("Power BI Visualization 2:")
    st.components.v1.iframe(
        "https://app.powerbi.com/view?r=YOUR_REPORT_ID_2", width=800, height=600
    )
