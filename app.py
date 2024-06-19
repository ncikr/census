import streamlit as st
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
# from load_data import load_census_data
from streamlit.components.v1 import html
from bank_theme import vizzu_bank_theme

st.title("")

census_data = pd.read_csv('data.csv', dtype=str)

# set datatypes
numeric_cols = ['Population',
       'easting', 'northing', 'Lat', 'Lon',
       'MSOA Population', 'UTLA Population', 'MSOA %',
       'UTLA %', 'Industry Population', 'Industry % in UTLA',
       'SO % in Industry', 'Total Population', 'Age %',
       'Conservative % Share']
census_data[numeric_cols] = census_data[numeric_cols].apply(pd.to_numeric)

# split data for speed
census_data_pop = census_data[(census_data['Dataset'] == 'pop_2021') | (census_data['Dataset'] == 'pop_historical')]
# census_data_industry = census_data[census_data['Dataset'] == 'industry']
# census_data_age = census_data[census_data['Dataset'] == 'Age']

# find top LGB+ areas
census_data_top_areas = census_data_pop[(census_data_pop['Sexual Orientation'] == "Gay or Lesbian") |
                                        (census_data_pop['Sexual Orientation'] == "Bisexual") |
                                        (census_data_pop['Sexual Orientation'] == "Other")]

census_data_top_areas = census_data_top_areas[['Area','MSOA %']].groupby('Area').mean().reset_index()
census_data_top_areas = census_data_top_areas.sort_values('MSOA %', ascending=False).head(20)

data = Data()
# census_data_vizzu = census_data[(census_data['Dataset'] == 'pop_2021') | (census_data['Dataset'] == 'pop_historical') | (census_data['Dataset'] == 'Age')]
data.add_df(census_data, max_rows=500000)

# initialise chart
chart = Chart(width=500, height= 500, display=DisplayTarget.MANUAL)
style = vizzu_bank_theme()

# initialise chart
chart.animate(data, style)

delay_time = 5

# Aggregate stats

chart.animate(Config({"title": "In 2021, the population in England & Wales were asked their sexual orientation..."}))

filter_pop_historical = Data.filter(
    """
    record['Dataset'] == 'pop_historical' 
    """
)

chart.animate(
    filter_pop_historical,
    Config({
        "title": "and for the first time in history...",
        "channels": {
            "y": {"set": ["Population"]},
            "x": {"set": ["Year"]},
            }
        }
    ),
        delay = delay_time
)

filter_pop_historical_2021 = Data.filter(
    """
    record['Dataset'] == 'pop_historical' || record['Dataset'] == 'pop_2021' 

    """
)

chart.animate(
    filter_pop_historical_2021,
    Config({"title": "...the adult population could be seen in full colour",
                      "channels": {
                            "y": {"attach": ["Sexual Orientation"]},
                            "color": {"attach": ["Sexual Orientation"]}}
                      }
                     ),
              delay = delay_time
              )


# polar chart for 2021

filter_2021 = Data.filter(
    """
    record['Dataset'] == 'pop_2021' 
    """
)

chart.animate(filter_2021,
              Config({"channels": {
                            "label": {"attach": ["Population"]},
                             "x": {"detach": ["Year"],
                                   "attach":"Population"},
                             "y": {"detach": ["Population"],
                                #    "range": {"min": "+10%"}
                                   }
                        },
                      "coordSystem" : "polar",
                      "reverse": True
                      },
                     ),
              delay = delay_time
              )

chart.animate(Config({"title": "Around 1.5 million people identified as non-heterosexual...",
                      }
                     )
              )

# pie chart
chart.animate(Config({"title": "...or 3.2% of the population.",
                      "channels": {
                          "label": {"detach": ["Population"]},
                          "y": {"detach":"Sexual Orientation"},
                        }
                      },
                     ),
              delay = delay_time
              )

# location chart
filter_lgb = Data.filter(
    """
    record['Dataset'] == 'pop_2021' &
    (record['Sexual Orientation'] == 'Gay or Lesbian' || 
    record['Sexual Orientation'] == 'Bisexual' || 
    record['Sexual Orientation'] == 'Other')
    """
)

chart.animate(filter_lgb,
              Config({"title": "How is the LGB+ community distributed across England & Wales?",
                      "geometry":"circle",
                      "channels": {
                          "x": {"set":None},
                          "y": {"set":None},
                          "size": {"attach":"Population"},
                          "label": {"attach": ["Sexual Orientation","Population"]}
                        },
                      "coordSystem" : "cartesian",
                      },
                     ),
              delay = delay_time
              )




chart.animate(
              Config({"title": "The distribution of LGB+ people is relatively consistent...",
                      "geometry":"rectangle",
                      "channels": {
                          "x": {"set":'mean(MSOA %)'},
                          "y": {"set":'Area'},
                          "label": {"set": None}
                        #   "noop": {"set": "Area"},
                        #   "size": {"detach":"Population"},
                        },
                      "sort": "byValue",
                      "reverse" : False
                      }
                ),
                Style(
                    {"plot": {"yAxis": {"label": {"fontSize" : "0"}}}}
                    ),
              delay = delay_time
              )

area_filter = "(record['Sexual Orientation'] == 'Gay or Lesbian' || record['Sexual Orientation'] == 'Bisexual' || record['Sexual Orientation'] == 'Other') && ("

for i, area in enumerate(census_data_top_areas['Area']):
    if i == 0:
        area_filter = area_filter + f"record['Area'] == '{area}'"
    else:
        area_filter = area_filter + " || " +  f"record['Area'] == '{area}'"
area_filter = area_filter + ")"
        

chart.animate(Data.filter(area_filter),
              Config({
                  "title": "...but with notable outliers in the top 20",
                  "sort": "byValue",
                }
                ),
                Style(
                    {"plot": {"yAxis": {"label": {"fontSize" : "1em"}}}}
                    ),
              delay = delay_time
              )

chart.animate(
    filter_lgb,
    Config({
            "title": "Areas with higher populations tended to have higher % of LGB+ people...",                      
            "geometry":"circle",
            "channels": {
                    "x": {"set":'MSOA %'},
                    "y": {"set":'MSOA Population'},
                    "label": {"set": None},
                    "noop": {"set": "Area"},
                    "color": "Sexual Orientation",
                    "size": {"set":None},
                },
        }),
        delay = delay_time
        )

chart.animate(
    Config({"title": 
        "...but what are the underlying reasons for this?"}),
        delay = delay_time
)

filter_tory_votes = Data.filter(
    """
    record['Dataset'] == 'pop_2021' &&
    (record['Conservative % Share'] != 0) || 
    (record['Sexual Orientation'] == 'Gay or Lesbian' || 
    record['Sexual Orientation'] == 'Bisexual' || 
    record['Sexual Orientation'] == 'Other')
    """
)

chart.animate(
    filter_tory_votes,
    Config({
            "title": "One theory involves different political leanings in cities...",                      
            "geometry":"circle",
            "channels": {
                    "x": {"set":'mean(MSOA %)'},
                    "y": {"set":'mean(Conservative % Share)'},
                    "label": {"set": None},
                    "noop": {"set": "Constituency"},
                    "color": "Sexual Orientation",
                    "size": {"set":None},
                },
        }),
        delay = delay_time
        )

chart.animate(
    Config({"title": 
        "However, by using Conservative party voting share as a proxy for political ideology..."}),
    delay = delay_time
)

chart.animate(
    Config({"title": 
        "...we find surprisingly little correlation between sexuality demographics and politics."}),
        delay = delay_time
)



chart.animate(
    Config({"title": 
        "Maybe cities offer more career opportunities in LGB+ friendly industries?"}),
    delay = delay_time
)

filter_industry_answered = Data.filter(
    """
    record['Dataset'] == 'industry' &&
    record['Sexual Orientation'] != 'Not answered' &&
    record['Sexual Orientation'] != 'Straight or Heterosexual' &&
    record['Industry'] != 'Other'
    """
)

chart.animate(
    filter_industry_answered,
    Config({
        "title":"Indeed the industries with the highest % of LGB+ people...",
        "geometry":"rectangle",
        # "align": "stretch",
            "channels": {
                    "x": {"set":['mean(SO % in Industry)']},
                    "y": {"set":['Industry']},
                    "label": {"set": None},
                    "color": "Sexual Orientation",
                    # "noop": {"set": 'UTLA Code'},
                    "size": {"set":None}
                },
            "sort": "byValue"
            }),
        delay = delay_time
        )

chart.animate(
    Config({"title": 
        "...such as hospitality, public sector and the financial sector..."}),
    delay = delay_time
)

filter_industry = Data.filter(
    """
    record['Dataset'] == 'industry'
    """
)

chart.animate(
    filter_industry,
    Config({
        "title":"...are more prevalent in areas of high population.",
        "geometry":"rectangle",
        # "align": "stretch",
            "channels": {
                    "x": {"set":['UTLA Population']},
                    "y": {"set":['mean(Industry % in UTLA)','Industry']},
                    "label": {"set": None},
                    "color": "Industry",
                    "noop": {"set": 'UTLA Code'},
                    "size": {"set":None}
                },
            "sort": "byValue"
            }),
        delay = delay_time
        )

chart.animate(
    Config({"title": 
        "but it's more than likely this is a correlation, not a causation"}),
    delay = delay_time
)

filter_age = Data.filter(
    """
    record['Dataset'] == 'Age' 
    """
)

chart.animate(
    filter_age,
    Config({
        "title":"Perhaps we can unlock further insight by looking at age distribution of LGB+ people",
        "geometry":"rectangle",
            "channels": {
                    "x": {"set":'Age'},
                    "y": {"set":'Age %'},
                    "label": {"set": None},
                    "color": "Sexual Orientation",
                    "noop": {"set": None},
                    "size": {"set":None}
                },
            "sort": "none"
            }),
        delay = delay_time
        )

chart.animate(
    Data.filter(
    """
    record['Dataset'] == 'Age' && 
    record['Sexual Orientation'] != 'Not answered' 
    """),
    Config({
        "title":"The 2021 census revealed that on average, LGB+ people are younger than non-LGB+",
         "channels": {"y": {"attach":'Sexual Orientation'}},
         "split":True
    })
)

chart.animate(
    Config({"title": 
        "...and as young people are generally more attracted to cities for their career opportunities..."}),
    delay = delay_time
)

chart.animate(
    Config({"title": 
        "...perhaps that is the underlying reason for the trend."}),
    delay = delay_time
)

chart.animate(
    Config({"title": "Happy Pride Month!",
            "channels": {
                    "x": {"set":None},
                    "y": {"set":None},
                    "label": {"set": None},
                    "color": None,
                    "noop": {"set": None},
                    "size": {"set":None}
                }}),
    Style({"title": {"fontSize" : "4em"}}),
    delay = delay_time
)

html(chart._repr_html_(), width=750, height=450)

st.caption("Source: ONS.gov.uk, data.gov.uk, House of Commons Library")
st.caption("")
st.caption('Glossary:')
st.caption("MSOA: Middle Layer Super Output Area")
st.caption("UTLA: Upper Tier Local Authority")
