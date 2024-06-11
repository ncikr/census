import streamlit as st
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from load_data import load_census_data
from streamlit.components.v1 import html
from render_chart import *
from bank_theme import vizzu_bank_theme


# st.title("2021 Census data")

# read old pop data
pop_old = pd.read_csv('./data/uk_adult_pop.csv')
pop_old['sexual_orientation'] = "Unknown"

# read 2021 data
pop_2021 = pd.read_excel('data\msoa_pop_by_orientation.xlsx')[['Sexual orientation (6 categories)', 'Observation']]

# cleaning
pop_2021 = pop_2021.rename(columns = {'Sexual orientation (6 categories)' : 'sexual_orientation', 'Observation' : 'population'})
pop_2021 = pop_2021.groupby(['sexual_orientation']).sum().reset_index()
pop_2021 = pop_2021[pop_2021['sexual_orientation'] != 'Does not apply']
pop_2021 = pop_2021.replace('All other sexual orientations', 'Other')
pop_2021['year'] = 2021

# append
pop = pop_old._append(pop_2021).sort_values('year')
# pop['year'] = pop['year'].astype(int)
pop['year'] = pop['year'].apply(lambda x: '01-01-' + str(x))
pop['year'] = pd.to_datetime(pop['year'])

# change units
pop['population'] = pop['population'].apply(lambda x: x/1000000).round(2)
pop = pop.rename(columns = {'population' : 'Population (M)',
                            'sexual_orientation' : 'Sexual Orientation',
                            'year' : 'Year'})

# data
data = Data()
data.add_df(pop)

# chart
chart = Chart(width=600, height= 400, display=DisplayTarget.MANUAL)
style = vizzu_bank_theme()
chart.animate(data, style)

chart.animate(Config({"title": "For the first time in over 200 years of censuses..."}))

chart.animate(
    Config(
        {
            "channels": {
                "y": {"set": ["Population (M)"]},
                "x": {"set": ["Year"]},
            }
        }
    )
)

html(chart._repr_html_(), width=750, height=450)
