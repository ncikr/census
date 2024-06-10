import pandas as pd
import streamlit as st

@st.cache_data
def load_census_data():
    
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
    pop['year'] = pop['year'].astype(str)
    # pop['Year'] = pop['Year'].apply(lambda x: '01-01-' + str(x))
    # pop['Year'] = pd.to_datetime(pop['Year'])

    # change units
    pop['population'] = pop['population'].apply(lambda x: x/1000000).round(2)
    pop = pop.rename(columns = {'population' : 'Population (M)',
                                'sexual_orientation' : 'Sexual Orientation',
                                'year' : 'Year'})


    pop.to_csv('data.csv', index = False)
