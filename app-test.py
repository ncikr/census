import streamlit as st
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from load_data import load_census_data
from streamlit.components.v1 import html
from render_chart import *
from bank_theme import vizzu_bank_theme

st.title("")
   
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
pop_2021 = pop_2021.sort_values('population', ascending=False)

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

# initialise data
data = Data()
data.add_df(pop)

# initialise chart
chart = Chart(width=1000, height= 1000, display=DisplayTarget.MANUAL)
style = vizzu_bank_theme()
chart.animate(data, style)

# Aggregate stats
chart.animate(Config({"title": "In 2021, the England & Wales census asked about sexual orientation..."}))

chart.animate(Config({"title": "and for the first time in history..."}),delay = 5)

chart.animate(
    Config(
        {
            "channels": {
                "y": {"set": ["Population (M)"]},
                "x": {"set": ["Year"]},
            }
        }
    ),
        delay = 5
)

chart.animate(Config({"title": "...the adult population could be seen in full technicolour.",
                      "channels": {
                            "y": {"attach": ["Sexual Orientation"]},
                            "color": {"attach": ["Sexual Orientation"]}}
                      }
                     ),
              delay = 3
              )


# polar chart for 2021

filter1 = Data.filter(
    """
    record['Year'] == '2021-01-01' 
    """
)

chart.animate(filter1,
              Config({"channels": {
                            "label": {"attach": ["Population (M)"]},
                             "x": {"detach": ["Year"],
                                   "attach":"Population (M)"},
                             "y": {"detach": ["Population (M)"],
                                #    "range": {"min": "+10%"}
                                   }
                        },
                      "coordSystem" : "polar",
                      "reverse": True
                      },
                     ),
              delay = 3
              )

chart.animate(Config({"title": "Around 1.5 million people identified as non-heterosexual...",
                      }
                     )
              )

chart.animate(Config({"title": "...or 3.2% of the population.",
                      "channels": {
                          "label": {"detach": ["Population (M)"]},
                          "y": {"detach":"Sexual Orientation"},
                        }
                      },
                     ),
              delay = 3
              )

html(chart._repr_html_(), width=750, height=450)

st.caption("Source: ONS")