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
data['Size_mod'].replace('1,000+', '1,000k', inplace=True)
data['Size_mod'] = data['Size_mod'].apply(useRegex_size)




col2, space2, col3 = st.columns((10,1,10))

with col2:
    # Category
    selected_cat = st.selectbox(label='Select category', options=cat_names)
    # selected_price = st.selectbox(label='Select category', options=cat_names)
    data_crop = data.loc[data.Category == selected_cat].copy()
    
    # Price
    min_price = data_crop.Price_mod.min()
    max_price = data_crop.Price_mod.max()
    mean_price = (min_price + max_price)/2
    selected_price = st.slider("Select Maximum Price", min_value=min_price, max_value=max_price, value=mean_price)
    data_crop_2 = data_crop.loc[data_crop.Price_mod <= selected_price]
    
    #Size
    selected_size = st.slider("Select Maximum Size", 10,20,30)
    varied_size = st.checkbox('Include Varied size with device', False)
    
    
    # # Android Version
    # varied_android = st.checkbox('Include Varied Android version with device in pie chart', False)
    # if varied_size == False:
    #     data_crop_2 = data_crop_2.loc[data_crop_2['Android Ver'] != 'Varies with device']
    
    # Date of latest update
    # Select the date when the oldest update took place
    st.date_input('Select the date when the latest update of the app took place')

    
    data_crop_2.sort_values(by='Rating', inplace=True)
    

with col3:  
    st.subheader("The 5 apps with the highest rating")
    fig = px.bar(data_crop_2[:5], y='App', x='Reviews', title="Age groups", orientation='h')
    st.plotly_chart(fig, use_container_width=True)

        
