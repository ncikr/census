import streamlit as st
import pandas
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from ipyvizzustory import Story, Slide, Step
from load_data import load_census_data
from streamlit.components.v1 import html

def aggregate_stats_chart(data, width, height):
    
    story = Story(data)
    story.set_size(width, height)

    slide1 = Slide(
        Step(
            Data.filter("record.Year != '2021'"),
            Config.stackedColumn({"x": "Year",
                    "y": "Population (M)",
                    "title": "Adult (16+) population in England and Wales",
                    "stackedBy": "Sexual Orientation",
                    'label' : "Sexual Orientation"
                    })
        )
    )
    story.add_slide(slide1)

    slide2 = Slide()

    slide2.add_step(
        Step(
            Data.filter("record.Year <= '2021'")
    ))

    slide2.add_step(
        Step(
            Data.filter("record.Year == '2021'"),
            Config({
                'y' : 'Sexual Orientation',
                'x' : 'Population (M)',
                'coordSystem' : 'polar',
                'title': '2021 Sexual Orientation Breakdown'
                    })
        )
    )

    story.add_slide(slide2)

    html(story._repr_html_(), width=width, height=height)
