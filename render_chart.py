import streamlit as st
import pandas
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from load_data import load_census_data
from streamlit.components.v1 import html

def render_chart(_chart, page):
    
    if page == 1 :
        
        _chart.animate(
            Data.filter("record.Year != '2021'"),
            Config.stackedColumn(
                {
                    "x": "Year",
                    "y": "Population (M)",
                    "title": "Adult (16+) population in England and Wales",
                    "stackedBy": "Sexual Orientation"
                }
            )
        )
        
    if page == 2 :
        
        _chart.animate(
            Data.filter("record.Year <= '2021'"),
            Config.stackedColumn(
                {
                    "x": "Year",
                    "y": "Population (M)",
                    "title": "Adult (16+) population in England and Wales",
                    "stackedBy": "Sexual Orientation"
                }
            )
        )
    
    return _chart._repr_html_()
