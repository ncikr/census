import pandas as pd
from ipyvizzu import Chart, Data, Config, Style,  DisplayTarget
from bank_theme import vizzu_bank_theme

census_data = pd.read_csv('data.csv', dtype=str)

# set datatypes
numeric_cols = ['Population', 'easting', 'northing', 'Lat', 'Lon','MSOA Population', 'UTLA Population', 'MSOA %','UTLA %','Industry Population','Industry %','Age Population', 'Age %', 'Conservative % Share']
census_data[numeric_cols] = census_data[numeric_cols].apply(pd.to_numeric)

census_data = census_data.sort_values(['Year','Population'], ascending=[True, False])

# split data for speed
census_data_pop = census_data[(census_data['Dataset'] == 'pop_2021') | (census_data['Dataset'] == 'pop_historical')]
census_data_industry = census_data[census_data['Dataset'] == 'industry']
census_data_age = census_data[census_data['Dataset'] == 'Age']

# find top LGB+ areas
census_data_top_areas = census_data_pop[(census_data_pop['Sexual Orientation'] == "Gay or Lesbian") |
                                        (census_data_pop['Sexual Orientation'] == "Bisexual") |
                                        (census_data_pop['Sexual Orientation'] == "Other")]

census_data_top_areas = census_data_top_areas[['Area','MSOA %']].groupby('Area').mean().reset_index()
census_data_top_areas = census_data_top_areas.sort_values('MSOA %', ascending=False).head(20)

data = Data()
data.add_df(census_data_pop, max_rows=500000)

# initialise chart
chart = Chart(width=500, height= 500, display=DisplayTarget.MANUAL)
style = vizzu_bank_theme()

# initialise chart
chart.animate(data, style)

delay_time = 0

# Aggregate stats
chart.animate(Config({"title": "In 2021, the population in England & Wales were asked their sexual orientation..."}))

chart.animate(
    Config(
        {
        "title": "and for the first time in history...",
        "channels": {
            "y": {"set": ["Population"]},
            "x": {"set": ["Year"]},
            }
        }
    ),
        delay = delay_time
)

# ####### add new rows ########
data.add_np_array(census_data_age.to_numpy())

filter_age = Data.filter(
    """
    record['Dataset'] == 'Age' 
    """
)

chart.animate(
    filter_age,
    Config({
            "channels": {
                    "x": {"set":'Age'},
                    "y": {"set":'Age %'},
                    "label": {"set": None},
                    "color": "Sexual Orientation",
                    "size": {"set":None},
                }
            }),
        delay = delay_time
        )

###################################

# chart.animate(Config({"title": "...the adult population could be seen in full technicolour.",
#                       "channels": {
#                             "y": {"attach": ["Sexual Orientation"]},
#                             "color": {"attach": ["Sexual Orientation"]}}
#                       }
#                      ),
#               delay = delay_time
#               )


# # polar chart for 2021

# filter_2021 = Data.filter(
#     """
#     record['Year'] == '2021' 
#     """
# )

# chart.animate(filter_2021,
#               Config({"channels": {
#                             "label": {"attach": ["Population"]},
#                              "x": {"detach": ["Year"],
#                                    "attach":"Population"},
#                              "y": {"detach": ["Population"],
#                                 #    "range": {"min": "+10%"}
#                                    }
#                         },
#                       "coordSystem" : "polar",
#                       "reverse": True
#                       },
#                      ),
#               delay = delay_time
#               )

# chart.animate(Config({"title": "Around 1.5 million people identified as non-heterosexual...",
#                       }
#                      )
#               )

# # pie chart
# chart.animate(Config({"title": "...or 3.2% of the population.",
#                       "channels": {
#                           "label": {"detach": ["Population"]},
#                           "y": {"detach":"Sexual Orientation"},
#                         }
#                       },
#                      ),
#               delay = delay_time
#               )

# # location chart
# filter_lgb = Data.filter(
#     """
#     record['Sexual Orientation'] == 'Gay or Lesbian' || 
#     record['Sexual Orientation'] == 'Bisexual' || 
#     record['Sexual Orientation'] == 'Other'
#     """
# )

# chart.animate(filter_lgb,
#               Config({"title": "How is the LGB+ community distributed across England & Wales?",
#                       "geometry":"circle",
#                       "channels": {
#                           "x": {"set":None},
#                           "y": {"set":None},
#                           "size": {"attach":"Population"},
#                           "label": {"attach": ["Sexual Orientation","Population"]}
#                         },
#                       "coordSystem" : "cartesian",
#                       },
#                      ),
#               delay = delay_time
#               )




# chart.animate(
#               Config({"title": "The distribution of LGB+ people is relatively consistent...",
#                       "geometry":"rectangle",
#                       "channels": {
#                           "x": {"set":'mean(MSOA %)'},
#                           "y": {"set":'Area'},
#                           "label": {"set": None}
#                         #   "noop": {"set": "Area"},
#                         #   "size": {"detach":"Population"},
#                         },
#                       "sort": "byValue",
#                       "reverse" : False
#                       }
#                 ),
#                 Style(
#                     {"plot": {"yAxis": {"label": {"fontSize" : "0"}}}}
#                     ),
#               delay = delay_time
#               )

# area_filter = "(record['Sexual Orientation'] == 'Gay or Lesbian' || record['Sexual Orientation'] == 'Bisexual' || record['Sexual Orientation'] == 'Other') && ("

# for i, area in enumerate(census_data_top_areas['Area']):
#     if i == 0:
#         area_filter = area_filter + f"record['Area'] == '{area}'"
#     else:
#         area_filter = area_filter + " || " +  f"record['Area'] == '{area}'"
# area_filter = area_filter + ")"
        

# chart.animate(Data.filter(area_filter),
#               Config({
#                   "title": "...but with notable outliers in the top 20",
#                   "sort": "byValue",
#                 }
#                 ),
#                 Style(
#                     {"plot": {"yAxis": {"label": {"fontSize" : "1em"}}}}
#                     ),
#               delay = delay_time
#               )

# chart.animate(
#     filter_lgb,
#     Config({
#             "title": "Areas with higher populations tended to have higher % of LGB+ people...",                      
#             "geometry":"circle",
#             "channels": {
#                     "x": {"set":'MSOA %'},
#                     "y": {"set":'MSOA Population'},
#                     "label": {"set": None},
#                     "noop": {"set": "Area"},
#                     "color": "Sexual Orientation",
#                     "size": {"set":None},
#                 },
#         }),
#         delay = delay_time
#         )

# chart.animate(
#     Config({"title": 
#         "Why is this?"})
# )

# filter_tory_votes = Data.filter(
#     """
#     record['Conservative % Share'] != 0 || 
#     record['Sexual Orientation'] == 'Gay or Lesbian' || 
#     record['Sexual Orientation'] == 'Bisexual' || 
#     record['Sexual Orientation'] == 'Other'
#     """
# )

# chart.animate(
#     filter_tory_votes,
#     Config({
#             "title": "One reason could be cultural differences in areas of high population...",                      
#             "geometry":"circle",
#             "channels": {
#                     "x": {"set":'mean(MSOA %)'},
#                     "y": {"set":'mean(Conservative % Share)'},
#                     "label": {"set": None},
#                     "noop": {"set": "Constituency"},
#                     "color": "Sexual Orientation",
#                     "size": {"set":None},
#                 },
#         }),
#         delay = delay_time
#         )

# chart.animate(
#     Config({"title": 
#         "The chart below uses the liklihood of voting for the Conservative party as a proxy for political views..."}),
#     delay = delay_time
# )

# chart.animate(
#     Config({"title": 
#         "...but it shows little correlation with the % of LGB+ people in an area"}),
#         delay = delay_time
# )


chart.show()