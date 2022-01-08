# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 22:26:04 2022

@author: ilias
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import regex as re

st.set_page_config(layout = "wide")

st.markdown("""# Playstore Apps -Statistics""")

def useRegex(input):
        pattern = re.compile(r"\$([0-9]*\.[0-9]+)")
        result = pattern.match(input)
        return result[1]
    
def useRegex_size(input):
        result = re.match('.+?(?=k|M)', input)
        return result[0]  

# this function cjhecks if this unit is in kb
def Checking_if_unit_is_kb(col1, col2):
    if 'k' in col1:
        return col2/1000
    else:
        return col2
    
def useRegex_android_version(input):
        result = re.match('\d{1}', input)
        return result[0]

data = pd.read_csv('../archive/googleplaystore.csv')

# Manipulation of 'Price' column using regex
data['Price_mod'] = data.Price # modified column "Price"
data['Price_mod'].replace('Everyone', '$0.0', inplace=True)
data['Price_mod'].replace('0', '$0.0', inplace=True)
data['Price_mod'] = data['Price_mod'].apply(useRegex)
# covert the type of the column into float
data['Price_mod'] = data['Price_mod'].apply(lambda x : float(x))
cat_names = data.Category.unique()
price_names = data.Category.unique()

# Manipulation of 'Size' column using regex
# Rows with value 'Varies with device' were erased
data = data.loc[data.Size != 'Varies with device']
data['Size_mod'] = data['Size']
data['Size_mod'].replace('1,000+', '1000k', inplace=True)
data['Size'].replace('1,000+', '1000k', inplace=True)
data['Size_mod'] = data['Size_mod'].apply(useRegex_size)
data['Size_mod'] = data['Size_mod'].astype('float')
data['Size_mod_2'] = data.apply(lambda x: Checking_if_unit_is_kb(x['Size'], x['Size_mod']), axis=1)

# Last update
data['Last Updated'] = pd.to_datetime(data['Last Updated'], format="%B %d, %Y", errors='coerce')

# Android version - remoning null values
data.dropna(subset=['Android Ver'], inplace=True)

col2, space2, col3 = st.columns((10,1,10))

with col2:
    # Category
    selected_cat = st.selectbox(label='Select category', options=cat_names)
    # selected_price = st.selectbox(label='Select category', options=cat_names)
    data_crop = data.loc[data.Category == selected_cat].copy()
    
    # Price
    min_price, max_price = data_crop.Price_mod.min(), data_crop.Price_mod.max()
    mean_price = (min_price + max_price)/2
    selected_price = st.slider("Select Maximum Price", min_value=min_price, max_value=max_price, value=mean_price)
    data_crop_2 = data_crop.loc[data_crop.Price_mod <= selected_price]
    
    #Size
    max_size, min_size = data_crop.Size_mod_2.max(), data_crop.Size_mod_2.min()
    mean_size = (max_size + min_size)/2
    selected_size = st.slider("Select Maximum Size", min_value=min_size, max_value=max_size, value=mean_size)
    data_crop_2 = data_crop.loc[data_crop.Size_mod_2 <= selected_size]

       
    # Date of latest update
    min_date, max_date = data['Last Updated'].min(), data['Last Updated'].max()
    series_dates = pd.Series([min_date, max_date]) # Pd.Series was used to extimate teh mean date
    mean_date = series_dates.mean()
    date_thershold = st.date_input('Select the date after which latest update of the app took place', value=mean_date, min_value=min_date, max_value = max_date)
    data_crop_2 = data_crop_2.loc[data_crop_2['Last Updated'] >= pd.to_datetime(date_thershold)].copy()
    
    # Android Version
    varied_android = st.checkbox('Include Varied Android version with device in pie chart', False)
    
    data_varied_Android = data_crop_2.loc[data_crop_2['Android Ver'] == 'Varies with device']
    data_crop_2 = data_crop_2.loc[data_crop_2['Android Ver'] != 'Varies with device']
    data_crop_2['Android_mod'] = data_crop_2['Android Ver'].apply(useRegex_android_version)
    android_breadkown = data_crop_2.groupby('Android_mod').agg(['count'])['App'].apply(list).to_dict()['count']
    
    if varied_android:
         android_breadkown['Varies with device'] = data_varied_Android.shape[0]
    

    
    # if varied_size == False:
    #     data_crop_2 = data_crop_2.loc[data_crop_2['Android Ver'] != 'Varies with device']
    
    data_crop_2.sort_values(by='Rating', inplace=True)
    

with col3:  
    st.subheader("The 5 apps with the highest rating")
    fig = px.bar(data_crop_2[:5], y='App', x='Reviews', title="Age groups", orientation='h')
    st.plotly_chart(fig, use_container_width=True)

col4, space3, col5 = st.columns((10,1,10))

with col4:
    st.subheader("Pie plot")
    fig_pie = px.pie(values=android_breadkown.values(), names=android_breadkown.keys(), title='Android Verion Required')
    st.plotly_chart(fig_pie, use_container_width=True)
    
    