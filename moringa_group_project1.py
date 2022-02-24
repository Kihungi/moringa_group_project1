# -*- coding: utf-8 -*-
"""MORINGA_GROUP_PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IBYuVye2FCGyVqjfMTnwpujwipbr99uG

# KENYA HEALTHCARE FACILITIES ANALYSIS

Good health is central to human happiness and well-being that contributes significantly to prosperity and wealth and even economic progress, as healthy populations are more productive, save more and live longer. In this project, we want to point out counties that are in dire need of attention from the government health sector and any other funding organizations in order to boost the general health care of the population.

# Loading our libraries
"""

# importing pandas
import pandas as pd

# importing numpy 
import numpy as np 

# importing pyplot
import matplotlib.pyplot as plt

# importing streamlit
import streamlit as st

# importing seaborn
import seaborn as sns
st.title('GROUP 1 FINAL PROJECT')

"""
# Loading the dataset to our environment"""

# Loading the healthcare facilities dataset
# url = 'https://africaopendata.org/dataset/3e95b5cb-39f5-44d3-94b6-f2d5285b0478/resource/0257f153-7228-49ef-b330-8e8ed3c7c7e8/download/ehealth-kenya-facilities-download-21102015.xls'

st.title("KENYA HEALTHCARE FACILITIES ANALYSIS")  # add a title
st.write("Hospitals Dataset")
uploaded_file = st.file_uploader("Chooose a file")
if uploaded_file is not None:
   hospitals = pd.read_csv(uploaded_file)
   st.write(hospitals)

hospitals = pd.read_csv('ehealth.csv')
#st.title("Moringa Project")  # add a title
#st.write(hospitals) 
# Preview the dataset 
#
hospitals.head()

# Loading the number of icubeds per county dataset
url = 'https://data.humdata.org/dataset/e231c2f5-11c6-4006-b0f8-f6cb41410b30/resource/57af4fb4-1141-41aa-a5f8-a92ccd5663c9/download/number-of-icu-beds-per-county.xlsx'

icubeds = pd.read_excel(url)

# Preview icubeds dataset
icubeds.head(0)
#icubeds.isnull().sum()
#np.count_nonzero(icubeds['Unnamed: 3'].isnull())
icubeds.loc[icubeds['Number of Hospital ICU Beds per county'] == 'Bomet']

# Loading health staff dataset per 10000 population
url = 'https://open.africa/dataset/4acc4709-cd40-43da-ad95-3b4a1224f97c/resource/43cea114-a929-4984-bd1c-b665d4a7ea5e/download/cfafrica-_-data-team-_-outbreak-_-covid19-_-data-_-openafrica-uploads-_-kenya-healthworkers.csv'

healthworkers = pd.read_csv(url)

#Preview the dataset
healthworkers.tail()
#healthworkers.shape

# Loading the population per county dataset
url = 'https://data.humdata.org/dataset/fa58ed8d-1daa-48b6-bae1-19746c32c85f/resource/82f909ce-7358-48da-9639-8fe9c3318251/download/2019-population_census-report-per-county.csv'
population = pd.read_csv(url)

# Preview population dataset
population.head()

"""# Getting information about our dataset"""

# info regarding the hospitals dataset
hospitals.info()

"""The hospitals dataframe has <b>29 columns and 10505 hospitals</b>. <b><i> Division, Location, sub_location, beds, cots, official fax, official mobile, official address, official landline, official alternate no., town, postcode, in charge, job title of incharge, open 24hrs, open weekends, ART, C-IMCI, FP, HBC and IPD</i></b> have null values.<b><i>ANC, BLOOD, BEOC, CAES SEC, CEOC, EPI, GROWM, HCT, OPD, OUTREACH, PMTC, RAD/XRAY, RHTC/RHDC, TB DIAG, TB LABS, TB TREAT and YOUTH</i></b> have no values."""

# Info regarding icebeds dataset
icubeds.info()

"""The icubeds dataframe has 4 columns and 100 entries. <b>unnamed: 3</b> coulmn has one null value.  """

# Info regarding healthworkers dataset
healthworkers.info()

"""The healthworkers dataframe has 2 columns and 48 entries. None of the columns have null values."""

# Info regarding population dataset
population.info()

"""The population dataframe has 11 columns and 47 entries representing the 47 counties. There are no missing values in this dataframe.

# DATA PREPARATION

We are first going to drop unnecessary columns in each dataset then merge our dataframes based on similarities.
"""

hospitals.columns

population.columns

icubeds.columns

# Dropping irrelevant columns

# Create a function to drop tables
def drop_columns(dataframe, columns):
  # Use the drop method on the dataframe to drop a list of columns
  dataframe.drop(columns, axis=1, inplace=True)
  # Return the dataframe without the dropped columns
  return dataframe.head()

hospitals_columns = ['Official Fax', 'Official Mobile', 'Official Address', 'Official Landline', 
                     'Official Alternate No','Official Email', 'Description of Location', 'Town','Post Code', 'In Charge', 
                     'Job Title of in Charge','Division', 'Location', 'Sub Location','ANC', 'BLOOD', 'BEOC', 
                     'CAES SEC', 'CEOC', 'EPI', 'GROWM', 'HCT', 'OPD', 'OUTREACH', 'PMTCT', 'RAD/XRAY', 'RHTC/RHDC', 
                     'TB DIAG', 'TB LABS', 'TB TREAT', 'YOUTH']

population_columns = ['Male populatio 2019','Female population 2019','Households','Av_HH_Size','LandArea', 
                      'Population Density','Population in 2009','Pop_change','Intersex population 2019'] 

icubeds_columns = ['Unnamed: 0', 'Unnamed: 2']
drop_columns(hospitals,hospitals_columns)
drop_columns(population, population_columns)
drop_columns(icubeds, icubeds_columns)

# For the icubeds dataset, we shall also drop the first row
icubeds.drop([0], inplace=True)
icubeds.head()
 
# We shall the group by county and sum number of icubeds
icubeds = icubeds.groupby(['Number of Hospital ICU Beds per county'], as_index=False)[['Unnamed: 3']].sum()
icubeds.head(10)

# drop last column in healthworkers dataset
healthworkers.drop([47], inplace=True)

# make county columns uniform
def combine_lower(value):
  return value.lower().replace(' ','').replace('_','').replace('-','')

hospitals['County'] = hospitals['County'].map(combine_lower)
healthworkers['County'] = healthworkers['County'].map(combine_lower)
population['County'] = population['County'].map(combine_lower)

icubeds['Number of Hospital ICU Beds per county'] = icubeds['Number of Hospital ICU Beds per county'].map(combine_lower)
# merge hospitals dataset with healthworkers dataset by county.
hospitals_healthworkers = hospitals.merge(healthworkers, how= 'left', on = 'County')
hospitals_healthworkers.head(2)

# Let us now merge the hospitals_healthworkers dataset with population dataset
hospitals_healthworkers_pop = hospitals_healthworkers.merge(population, how='left', on='County')
hospitals_healthworkers_pop.head(2)

# Let us now merge the hospitals_healthcare_pop dataset with icubeds dataset
hospitals = hospitals_healthworkers_pop.merge(icubeds, how='left', left_on='County', 
                                                          right_on='Number of Hospital ICU Beds per county')
hospitals.head(2)
hospitals.drop('Number of Hospital ICU Beds per county', axis=1, inplace=True)
hospitals.rename(columns={'Unnamed: 3':'Number of Hospital ICU Beds per county'},inplace=True)

# Display the columns of our dataset
hospitals.columns

# We shall rename and rearrange our columns

# Renaming our columns
hospitals.columns = ['Facility Code', 'Facility Name', 'Province', 'County', 'District',
       'Hospital Type', 'Owner', 'Constituency', 'Nearest Town', 'No of Beds', 'No of Cots', 'Open 24 Hours',
      'Open Weekends', 'Operational Status', 'ART', 'C-IMCI', 'FP', 'HBC', 'IPD',
       'Core health workforce per 10,000 population', 'Total Population', 'No of ICU beds']

# Rearranging our columns
hospitals = hospitals[['Facility Code', 'Facility Name', 'Hospital Type', 'Owner', 
                                               'No of Beds', 'No of Cots', 'No of ICU beds', 'Open 24 Hours',
                                               'Open Weekends', 'Operational Status', 'ART', 'C-IMCI', 'FP', 
                                               'HBC', 'IPD', 'Core health workforce per 10,000 population', 
                                               'Total Population', 'County',  'Province',  'District', 
                                               'Constituency', 'Nearest Town']]
hospitals.head(2)

# Let's get information about our dataset
hospitals.info()

# Describing our dataset
hospitals.describe()

"""# DATA CLEANING

## a.) Validity
"""

#Procedure 1: Irrelevant data
# Data cleaning action: Drop columns 
# Explanation: Not required

columns = ['District','Province']
drop_columns(hospitals, columns)

#Procedure 1:
# Data cleaning action: Check whitespaces
# Explanation:
hospitals['Facility Name'] = hospitals['Facility Name'].str.strip()
hospitals['County'] = hospitals['County'].str.strip()
hospitals['Hospital Type'] = hospitals['Hospital Type'].str.strip()
hospitals['Owner'] = hospitals['Owner'].str.strip()
hospitals['Operational Status'] = hospitals['Operational Status'].str.strip()
hospitals['Nearest Town'] = hospitals['Nearest Town'].str.strip()
hospitals.head(10)

"""## b.) Accuracy"""



"""## c.) Completness"""

# Check null values
hospitals.isnull().sum()

# We assume that hospitals with null values of open 24hrs and open weekends are not opened on these hours and days respectively.
# Replace 'NaN' with 'N' for No

def fillna_N(dataframe, column):
  dataframe[column] = dataframe[column].fillna('N')
  return dataframe

columns = ['Open 24 Hours', 'Open Weekends', 'ART', 'C-IMCI', 'FP', 'HBC', 'IPD' ]
fillna_N(hospitals, columns)


hospitals.head(10)

# Hospitals with missing values of beds and cots are likely to not have these resources
# Fill missing values with 0
def fillna_0(dataframe, column):
  dataframe[column] = dataframe[column].fillna('0')
  return dataframe

columns = ['No of Beds', 'No of Cots', 'Nearest Town', 'No of ICU beds']  
fillna_0(hospitals, columns)

# Fill 'Core health workforce per 10,000 population' null values with the mean
hospitals['Core health workforce per 10,000 population'].fillna(hospitals['Core health workforce per 10,000 population'].mean(), inplace=True)

hospitals.isnull().any()

"""## d.) Consistency"""

# Check duplicates
hospitals.duplicated().sum()

"""## e.) Uniformity"""

hospitals.columns = hospitals.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('  ','   ')
#hospitals.columns = hospitals.columns.str.lower().str.replace(' ', '_')
hospitals.head()

#combine compound county names
def combine(column):
  return column.replace(' ','')

hospitals['county'] =  hospitals['county'].map(combine)

hospitals.info()

def str_to_int(column):
  return int(column)

hospitals['no_of_beds'] = hospitals['no_of_beds'].map(str_to_int)
hospitals['no_of_cots'] = hospitals['no_of_cots'].map(str_to_int)
hospitals['total_population'] = hospitals['total_population'].str.replace(',', '').astype(int)

hospitals['facility_code'] = hospitals['facility_code'].astype(str)
hospitals.head()

hospitals.describe()

"""# We export our clean dataset into a csv file and then load it to our notebook."""

hospitals = hospitals[hospitals['operational_status'] == 'Operational']

hospitals.to_csv('hospitals.csv')

# load csv into the notebook
hospitals = pd.read_csv('hospitals.csv')

"""# DATA ANALYSIS

i.) Which county has the highest number of medical resources?
"""

# beds

# Group data by county while summing number of beds
normal_beds = hospitals.groupby(['county', 'total_population'], as_index=False)[['no_of_beds']].sum()
st.dataframe(normal_beds)
# Sort values by no of beds.
normal_beds.sort_values(by='no_of_beds', ascending=False).head()

# Finding bed to 10000 population ratio.
normal_beds['bed_ratio_per_10000pop'] = normal_beds['no_of_beds'] * 10000 * 1.0 / normal_beds['total_population']
normal_beds.sort_values(by='bed_ratio_per_10000pop', ascending=1).head()

normal_beds.plot.bar('county', 'bed_ratio_per_10000pop', width=1, figsize=(20,10))
normal_beds = normal_beds.set_index('county')
st.write(normal_beds)
chart_data = pd.DataFrame(normal_beds,columns=['bed_ratio_per_10000pop'])
st.bar_chart(chart_data)

"""Kwale county lies slightly below the acceptable number of beds per 10000 population(5 beds per 10000 population). This is in accordance with World Health Organization report."""

#number of cots
cots = hospitals.groupby(['county'], as_index=False)[['no_of_cots']].sum()
cots.sort_values(by='no_of_cots').head()
cots.plot.bar('county', 'no_of_cots', width=1, figsize=(10,5), grid=True)
cots = cots.set_index('county')
st.write(cots)
chart_data = pd.DataFrame(cots,columns=['no_of_cots'])
st.bar_chart(chart_data)

"""ii.) Ratio of hospitals to population per county"""

no_of_hospitals = hospitals.groupby(['county', 'total_population', 'core_health_workforce_per_10,000_population'], as_index=False)[['facility_code']].count()

no_of_hospitals.rename(columns={'facility_code': 'no_of_hospitals'}, inplace=True)

no_of_hospitals.sort_values(by='total_population', ascending=0)
no_of_hospitals['hospital_pop_ratio'] = no_of_hospitals['no_of_hospitals']*1.0/ no_of_hospitals['total_population']
no_of_hospitals.sort_values(by='hospital_pop_ratio', ascending=1).head()

no_of_hospitals.plot.bar('county', 'hospital_pop_ratio', width=1, figsize=(15,9), grid=True)
no_of_hospitals = no_of_hospitals.set_index('county')
st.write(no_of_hospitals)
chart_data = pd.DataFrame(no_of_hospitals,columns=['hospital_pop_ratio'])
st.bar_chart(chart_data)

"""iii.) Find the county with lowest number of core_health_workforce_per_10,000_population."""

# Sort records by core_health_workforce_per_10,000_population

# Sort by core_health_workforce_per_10,000_population in the no_of_hospitals dataframe.
no_of_hospitals.sort_values(by='core_health_workforce_per_10,000_population', ascending=1).head()
no_of_hospitals.plot.bar()
# 'county', 'core_health_workforce_per_10,000_population', width=1, figsize=(15,9), grid=True
#no_of_hospitals = no_of_hospitals.set_index('county')
st.write(no_of_hospitals)
chart_data = pd.DataFrame(no_of_hospitals,columns=['core_health_workforce_per_10,000_population'])
st.bar_chart(chart_data)

"""The minimum number of healthworkforce as stated by WHO is a minimum of 4.45 healthworkers for 10000 population. This criteria has been met successfully with Mandera having the least ratio of 5.2. """

no_of_hospitals['healthworker_to_pop_ratio'] = 10000/ no_of_hospitals['core_health_workforce_per_10,000_population']
no_of_hospitals.sort_values(by='healthworker_to_pop_ratio', ascending=1).head()
no_of_hospitals[no_of_hospitals['healthworker_to_pop_ratio'] < 854.0].head()

"""iv.) How many hospitals are open at night hours for emergencies per county?

"""

opened_24_hrs = hospitals[hospitals['open_24_hours'].map(lambda open_24_hours: 'Y' in open_24_hours)]
opened_24_hrs = opened_24_hrs.groupby(['county', 'total_population'], as_index=False)[['open_24_hours']].count()
opened_24_hrs.sort_values(by='open_24_hours', ascending=1).head()
opened_24_hrs.plot.bar('county', 'open_24_hours', width=1, figsize=(15,9), grid=True)
opened_24_hrs = opened_24_hrs.set_index('county')
st.write(opened_24_hrs)
chart_data = pd.DataFrame(opened_24_hrs,columns=['open_24_hours'])
st.bar_chart(chart_data)
"""Nairobi has the largest number of hospitals opening 24hrs. Lamu has the least number of hospitals that can attend to night emergencies.

v.) Determining the number of ICU beds per county.
"""

hospitals_icu_beds = hospitals.groupby(['county'], as_index=False)[['no_of_icu_beds']].sum()
hospitals_icu_beds.plot.bar('county', 'no_of_icu_beds', width=1, figsize=(15,9), grid=True)
hospitals_icu_beds = hospitals_icu_beds.set_index('county')
st.write(hospitals_icu_beds)
chart_data = pd.DataFrame(hospitals_icu_beds,columns=['no_of_icu_beds'])
st.bar_chart(chart_data)

# counties with no icu beds
#hospitals_icu_beds.loc[hospitals_icu_beds['no_of_icu_beds'] != 0, ['county', 'no_of_icu_beds']]

"""Very few hospitals countrywide offer icu services. Nairobi has the highest number of ICU beds. Counties such as Mandera, Marsabit, Nyamira, Nyandarua , Siaya, Tana River, Turkana, Wajir and Vihiga had no icu services as of March 2020.

vi.) How many (in)patients can be admitted when the hospital is at full capacity per county?
"""

hospitals['total_beds'] = hospitals['no_of_icu_beds'] + hospitals['no_of_beds']
hospitals_beds = hospitals.groupby(['county', 'total_population'], as_index=False)[['total_beds']].sum()
hospitals_beds.sort_values(by='total_beds', ascending=True).head()
hospitals_beds['bed_ratio_per_10000pop'] = hospitals_beds['total_beds'] * 10000 * 1.0/ hospitals_beds['total_population']
hospitals_beds.sort_values(by='bed_ratio_per_10000pop', ascending=True).head()
hospitals_below_threshold =hospitals_beds[hospitals_beds['bed_ratio_per_10000pop'] < 20 ]
hospitals_below_threshold.sort_values(by='bed_ratio_per_10000pop', ascending=1)

hospitals_beds.plot.bar('county', 'bed_ratio_per_10000pop', width=1, figsize=(15,9), grid=True)
hospitals_beds = hospitals_beds.set_index('county')
st.write(hospitals_beds)
chart_data = pd.DataFrame(hospitals_beds,columns=['bed_ratio_per_10000pop'])
st.bar_chart(chart_data)
"""<b>Mandera, Kilfi, Wajir, Nandi, Tan River, Turkana, Siaya, Nyandarua, Bomet, Kitui, Baringo, Lamu, Kajiado, Busia, Marsabit, Vihiga, Kwale, Laikipia, Nyamira, Migori and Narok</b> counties lie below the accpetable standard of 20 beds per 10000 population. Mandera has the list ratio of 5.106881.

vi.) The percentage (%) of private and government owned hospitals per county.
"""

# Finding the percentage of government hospitals versus private hospitals in the whole country
hospitals_types = pd.DataFrame()
gvt = hospitals[(hospitals['owner'] == 'Ministry of Health') | 
                (hospitals['owner'] == 'Local Authority T Fund') | 
                (hospitals['owner'] == 'Community Development Fund') |
                (hospitals['owner'] == 'Local Authority')]

priv = hospitals[(hospitals['owner'] != 'Ministry of Health') & 
                (hospitals['owner'] != 'Local Authority T Fund') & 
                (hospitals['owner'] != 'Community Development Fund') &
                (hospitals['owner'] != 'Local Authority')]


gvt_count = gvt['owner'].value_counts()
# print the counts
print(gvt_count)
priv_count = priv['owner'].value_counts()
# print the counts
print(priv_count)

# Visualize all types of hospitals on graph
hos_types = hospitals['owner'].value_counts()
hos_types.plot.bar(grid=True)

st.bar_chart(hos_types)

# visualize types of government hospitals on a bar graph.
gvt_count.plot.bar(grid=True)
st.bar_chart(gvt_count)
# print the counts
#print(gvt_count)

priv_count.plot.bar(figsize=(8,5), grid=True)
st.bar_chart(priv_count)
# To find the percentage (%) of private and government owned hospitals per county.
total_facilities = hospitals.groupby(['county','core_health_workforce_per_10,000_population','total_population'],
                                     as_index=False)[['facility_code']].count()
total_facilities.head()

# Rename facility_code column to no_of_hospitals
total_facilities.rename(columns={'facility_code':'total_hospitals'}, inplace=True)  

# convert no of hospitlas to int
total_facilities['total_hospitals'] =  total_facilities['total_hospitals'].astype(int)

# count hospitals for each county
total_gvt = gvt.groupby(['county', 'total_population','core_health_workforce_per_10,000_population'],
                        as_index=False)[['facility_name']].count()
# Rename facility_name column to no_of_hospitals
total_gvt.rename(columns={'facility_name':'no_of_hospitals'}, inplace=True)                        
total_gvt['no_of_hospitals'] = total_gvt['no_of_hospitals'].astype(int) 

total_facilities['no_of_gvt_hospitals_%']  = (
   total_gvt['no_of_hospitals'] * 1.0/total_facilities['total_hospitals']) * 100
total_facilities['private_hospitals_%'] = 100 -  total_facilities['no_of_gvt_hospitals_%']   
total_facilities.sort_values(by='no_of_gvt_hospitals_%', ascending=1).head()

total_facilities.plot.bar('county', 'no_of_gvt_hospitals_%', width=1, figsize=(15,9), grid=True)
total_facilities = total_facilities.set_index('county')
st.write(total_facilities)
chart_data = pd.DataFrame(total_facilities,columns=['no_of_gvt_hospitals_%'])
st.bar_chart(chart_data)
"""Only 5.9% of the hospitals in Nairobi are government hospitals. Government hospitals offer free medical services with only a small charge which is more affordable to the public compared to private hospitals:
Private hospital inpatient fees averages at 9500/- while public hospital inpatient fees averages at 
4000/-. 
Private hospitals ICU charges averages at 30k while public hospital ICU charges averages at  
Maternal charges for private hospitals averages at 200k. 
"""

# Find hospital with highest number of private hospitals
total_facilities.plot.bar('county', 'private_hospitals_%', width=1, figsize=(15,9), grid=True)
total_facilities = total_facilities.set_index('county')
st.write(total_facilities)
chart_data = pd.DataFrame(total_facilities,columns=['private_hospitals_%'])
st.bar_chart(chart_data)
"""Lamu, Isiolo, Tana River, Mandera and Vihiga have less than 100 hospitals despite having a population of more than 100000. Moreover, there are few healthworkers in each hospital. This implies that the ratio of health workers to the total population is also small. """

# number of antiretroviral therapy per county
art_ = hospitals[(hospitals['art']=='Y') & (hospitals['operational_status']=='Operational')]
art_ = art_.groupby('county',as_index=False)['facility_code'].count()
art_.sort_values(by='facility_code', ascending=1).head()
art_.plot.bar(x='county', y='facility_code', width=1, figsize=(15,5), grid=True)
art_ = art_.set_index('county')
st.write(art_)
chart_data = pd.DataFrame(art_,columns=['facility_code'])
st.bar_chart(chart_data)
# number of family practitioners per county
fp_= hospitals[(hospitals['fp']=='Y') & (hospitals['operational_status']=='Operational')]
fp_ = fp_.groupby('county',as_index=False)['facility_code'].count()
fp_.sort_values(by='facility_code', ascending=1).head()
fp_.plot.bar(x='county', y='facility_code', width=1, figsize=(15,5), grid=True)
fp_ = fp_.set_index('county')
st.write(fp_)
chart_data = pd.DataFrame(fp_,columns=['facility_code'])
st.bar_chart(chart_data)
# number of haemoglobin testing per county
hbc_= hospitals[(hospitals['hbc']=='Y') & (hospitals['operational_status']=='Operational')]
hbc_ = hbc_.groupby('county',as_index=False)['facility_code'].count()
hbc_.sort_values(by='facility_code', ascending=1).head()
hbc_.plot.bar('county', 'facility_code', width=1, figsize=(15,5), grid=True)
hbc_ =hbc_.set_index('county')
st.write(hbc_)
chart_data = pd.DataFrame(hbc_,columns=['facility_code'])
st.bar_chart(chart_data)

# number of intermmitent peritoneal dialysis per county
ipd_= hospitals[(hospitals['ipd']=='Y') & (hospitals['operational_status']=='Operational')]
ipd_ = ipd_.groupby('county',as_index=False)['facility_code'].count()
ipd_.sort_values(by='facility_code', ascending=1).head().head()
ipd_.plot.bar('county', 'facility_code', width=1, figsize=(15,5), grid=True)
ipd_ =ipd_.set_index('county')
st.write(ipd_)
chart_data = pd.DataFrame(ipd_,columns=['facility_code'])
st.bar_chart(chart_data)
"""Nairobi county has the highest number of resources."""
