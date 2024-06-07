import streamlit as st
import pandas
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from load_data import load_census_data
from streamlit.components.v1 import html
from render_chart import render_chart


st.title("2021 Census data")

# page counter
if 'count' not in st.session_state:
    st.session_state.page_counter = 1

# load data
census_data = load_census_data()
data = Data()
data.add_df(census_data)

# initialize chart
height = 600
width = 800
chart = Chart(width=f"{width}px", height=f"{height}px", display=DisplayTarget.MANUAL)
chart.animate(data)

# render chart
# chart_html = render_chart(chart, st.session_state.page_counter)

chart.animate(
    Data.filter("record.Year != '2021'"),
    Config.stackedColumn(
        {
            "x": "Year",
            "y": "Population (M)",
            "title": "Slide 1",
            "stackedBy": "Sexual Orientation"
        }
    )
)



html(chart._repr_html_(), width=width, height=height ) 


st.write("""
         This is a test
         
         """)

    
# page buttons    
    
max_pages = 5

left, centre, right = st.columns([2,8,2])

with left:
    if st.button("Previous"):
        if st.session_state.page_counter != 1:
            st.session_state.page_counter-=1
        
with right:
    if st.button("Next"):
        if st.session_state.page_counter != max_pages:
            st.session_state.page_counter += 1
with centre:
    st.write(f"Page: {st.session_state.page_counter}")