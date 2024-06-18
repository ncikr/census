import pandas as pd
    
# read historical population data
# https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/adhocs/005825populationestimatesforenglandandwales1961to2014singleyearofage0to105
pop_historical = pd.read_excel('./data/historical_pop_england_and_wales.xls', sheet_name='Cleaned')[['Year','Population']]
pop_historical['Sexual Orientation'] = "Unknown"
pop_historical = pop_historical.rename(columns = {'Sexual orientation (6 categories)' : 'sexual_orientation'})
pop_historical['Dataset'] = 'pop_historical'

# 2021 aggregate population data
pop_2021 = pd.read_excel('data\msoa_pop_by_orientation.xlsx')[['MSOA Code','Area','Sexual Orientation', 'Population']]
pop_2021 = pop_2021[pop_2021['Sexual Orientation'] != 'Does not apply']
pop_2021 = pop_2021.replace('All other sexual orientations', 'Other')
pop_2021['Year'] = 2021
pop_2021['Dataset'] = 'pop_2021'

# join msoa coords
msoa_centroids = pd.read_excel('data\msoa_centroids.xlsx')
pop_2021 = pop_2021.merge(msoa_centroids, on='MSOA Code', how='left')

# join upper tier local authorities
# https://www.data.gov.uk/dataset/6338d27a-d19d-45de-b1c8-7660f3c3903b/msoa-2021-to-upper-tier-local-authorities-2023-best-fit-lookup-in-ew
utla = pd.read_csv('data\msoa_to_utla.csv')[['MSOA Code','UTLA Code','UTLA']]
pop_2021 = pop_2021.merge(utla, on='MSOA Code', how='left')

# calculate pct
pop_2021_msoa_agg = pop_2021[['MSOA Code', 'Sexual Orientation','Population']].groupby(['MSOA Code']).sum().reset_index()
pop_2021_msoa_agg = pop_2021_msoa_agg.rename(columns = {'Population' : 'MSOA Population'})

pop_2021_utla_agg = pop_2021[['UTLA Code', 'Sexual Orientation','Population']].groupby(['UTLA Code']).sum().reset_index()
pop_2021_utla_agg = pop_2021_utla_agg.rename(columns = {'Population' : 'UTLA Population'})

pop_2021 = pop_2021.merge(pop_2021_msoa_agg[['MSOA Code','MSOA Population']], on='MSOA Code', how='left')
pop_2021 = pop_2021.merge(pop_2021_utla_agg[['UTLA Code','UTLA Population']], on='UTLA Code', how='left')

pop_2021['MSOA %'] = 100 * pop_2021['Population'] / pop_2021['MSOA Population']
pop_2021['UTLA %'] = 100 * pop_2021['Population'] / pop_2021['UTLA Population']

# append historical pop data
pop = pop_2021._append(pop_historical).sort_values(['Year','Population'], ascending=[True, False])
pop['Year'] = pop['Year'].astype(str)

## industry data ##    
# https://www.ons.gov.uk/datasets/RM184/editions/2021/versions/7/filter-outputs/db062759-a153-46a0-b1f9-f52b2acacc91#get-data
industry = pd.read_excel('data\industry.xlsx')[['UTLA Code','UTLA','Industry','Sexual Orientation', 'Population']]
industry = industry.replace('All other sexual orientations', 'Other')
industry = industry[industry['Sexual Orientation'] != "Does not apply"]
industry = industry[industry['Industry'].notna()]
industry = industry.sort_values(['Population'], ascending=False)

industry = industry[['UTLA Code', 'Industry', 'Sexual Orientation','Population']].groupby(['UTLA Code','Sexual Orientation','Industry']).sum().reset_index()

industry_agg_utla = industry.groupby('UTLA Code').sum().reset_index().rename(columns = {'Population' : 'UTLA Population'})
industry_agg_ind = industry.groupby(['UTLA Code','Industry']).sum().reset_index().rename(columns = {'Population' : 'Industry Population'})
industry_agg = industry_agg_ind.merge(industry_agg_utla[['UTLA Code','UTLA Population']], how='left')
industry_agg['Industry % in UTLA'] = 100 * industry_agg['Industry Population'] / industry_agg['UTLA Population']

industry = industry.merge(industry_agg[['UTLA Code','Industry','Industry Population','UTLA Population','Industry % in UTLA']], how='left')
industry['SO % in Industry'] = 100 * industry['Population'] / industry['Industry Population']

industry['Dataset'] = 'industry'

industry = industry.sort_values('Industry % in UTLA')

pop_with_ind = pop._append(industry)

## age data ##
# https://www.ons.gov.uk/filters/3971c223-d948-4084-b74e-841cb5e876e3/dimensions

age = pd.read_excel('data\\age.xlsx')[['UTLA Code','UTLA','Age','Sexual Orientation', 'Population']]
age = age[age['Population'] != 0]
age = age[age['Age'] != '<15'].sort_values(['UTLA','Age'], ascending=True)

age = age[['Age', 'Sexual Orientation','Population']].groupby(['Age','Sexual Orientation']).sum().reset_index()

age_agg = age.groupby('Sexual Orientation').sum().reset_index()[['Sexual Orientation', 'Population']]
age_agg = age_agg.rename(columns = {'Population':'Total Population'})

age = age.merge(age_agg, how='left')
age['Age %'] = 100 * age['Population'] / age['Total Population']

age['Dataset'] = 'Age'

pop_with_age = pop_with_ind._append(age)

## 2019 election data ##
# https://commonslibrary.parliament.uk/research-briefings/cbp-8647/#fullreport
# https://www.data.gov.uk/dataset/f004674d-d0db-467b-9bd7-009b9d1e2fc6/msoa-2021-to-westminster-parliamentary-constituencies-july-2024-best-fit-lookup-in-ew

constituencies = pd.read_csv('data\\msoa_to_constituencies.csv')[['MSOA Code','Constituency']]
election_results = pd.read_excel('data\\election.xlsx')[['Constituency','Conservative % Share', 'election']]
election_results = election_results[election_results['election'].astype(str).isin(['2015','2017','2019'])]
election_results = election_results[['Constituency','Conservative % Share']].groupby('Constituency').mean().reset_index()

constituencies = constituencies.merge(election_results, on='Constituency', how='left')

pop_final = pop_with_age.merge(constituencies, on='MSOA Code', how='left')

# change units
# pop_final['Population '] = pop['population'].apply(lambda x: x/1000000).round(2)

pop_final.to_csv('data.csv', index = False)