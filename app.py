# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

def clean_data(df):
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('_', '')
    df = df.reset_index()
    df.dropna(subset=['Income'], inplace=True)
    df['DtCustomer']= pd.to_datetime(df['DtCustomer'])
    df['Income'] = df['Income'].str.replace('$', '').str.replace(',', '').str.replace(' ', '').str.replace('.','').str.replace('00','').astype(np.int64)
    df['TotalPrice'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
    df['YearMonth'] = pd.to_datetime(df['DtCustomer'].dt.year.astype('str') + '-' + df['DtCustomer'].dt.month.astype('str'))
    df = df[df['YearBirth'] > 1900].reset_index(drop=True)
    return df
df = pd.read_csv('original_marketing_data.csv')
df_clean = pd.read_csv('marketing_data.csv')
df_clean = clean_data(df_clean)

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Cleaning","Data Visualization"],
        icons=["house", "clipboard-data", "book"],
        menu_icon="cast",
        default_index=0,
    )
    
if selected == 'Home':
    st.title(':chart_with_upwards_trend: Customer Application Overview')
    st.markdown("***")
    image = Image.open('Images/cart_i.jpg')
    st.image(image, use_column_width=True)
    st.write('In this demo we will go through the data of customers who has signed up for a company\
             with their data regarding purchases, their home country and so on. Some of the data that we will tackle\
             are:')
    st.write("""
            - Date of the customer when they signed up for this company
            - Their origins
            - Marital status
            - Total purchases
            """)
    st.markdown("***")
    st.write('The data we will use for this demo is the following:')
    st.write(df_clean.head(5))


if selected == 'Data Cleaning':
    st.title(':sparkles: Data Cleaning')
    st.markdown("***")   
    # First header with smaller size
    st.markdown("<h2 style='text-align: center; color: black;'><u>1- Data Management</u></h2>"
                , unsafe_allow_html=True)
    st.write('We notice that there are several cleaning that we need to do in order to proceed with our analysis.')
    st.write('- We will start by removing spaces and underscores in columns such as **Dt_Customer** and **Income**.')
    st.write('- We will also remove the null values in **Income** column.')
    df[df[' Income '].isna()]
    st.write('- Then we will convert the **Dt_Customer** column to datetime format.')
    st.write('- Finally we will calculate the **TotalPrice** of purchases and create a new column **YearMonth** which will help us in our analysis.')
    st.write('Our data will look as follows:')
    st.write(df_clean.head(5))
    
    ###########################################
    
    # Second header with smaller size
    st.markdown("<h2 style='text-align: center; color: black;'><u>2- Remove Outliers</u></h2>"
                , unsafe_allow_html=True)
    st.write('We notice in our data there are some outliers that we need to handle.')
    st.write('Below you can see the list of unique data in **YearBirth** column with the box plots of before removing the outliers and after:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(df_clean['YearBirth'].sort_values().unique())
    with col2:
        st.write(df['Year_Birth'].plot(kind='box', figsize=(3,4), patch_artist=True))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with col3:
        st.write(df_clean['YearBirth'].plot(kind='box', figsize=(3,4), patch_artist=True))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
if selected == 'Data Visualization':
    st.title(':white_check_mark: Customer Application Overview')
    st.markdown("***")   


    data1 = st.selectbox('Select One Item:', ['MaritalStatus','Kidhome','Teenhome','Education','Country'])
    
    #grouped_df = df_clean.groupby(['Education',data2]).count().reset_index()
    
    if data1:
        grouped_df = df_clean.groupby(data1)['TotalPrice'].sum().reset_index()
        st.plotly_chart(px.bar(grouped_df, x=data1, y='TotalPrice', color='TotalPrice', barmode='group'))
    
    st.markdown('***')
    

    col1 , col2 = st.columns(2)

    with col1:
        df_Income_Education = df_clean.groupby('Education')['ID'].count().reset_index()
        df_Income_Education.sort_values('ID', ascending=False, inplace=True)
        st.plotly_chart(px.bar(df_Income_Education, x='Education',y='ID',color='Education',title='Number of People per Education'), use_container_width=True)
    
    with col2:
        df_Most_Payed_By_Country = df_clean.groupby('Education')['Complain'].count().reset_index()
        df_Most_Payed_By_Country.sort_values('Education', ascending=False, inplace=True)
        #px.bar(df_Most_Payed_By_Country, x='Country',y='TotalPrice',color='Country',title='Most Payed By Country')
        st.plotly_chart(px.pie(df_Most_Payed_By_Country, values='Complain', names='Education', title='Most People Complain per Education'), use_container_width=True)
    

    st.markdown('***')

    col1 , col2 = st.columns(2)

    with col1:
        # Create multi select dropdown for unique values in 'Category' column
        selected_education = st.multiselect("Select Education", df_clean['Education'].unique())

    with col2:
        # Create dropdown for selecting column names
        selected_column = st.selectbox("Select Column to Group By", ['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases','NumWebVisitsMonth'])
    
    grouped_df = df_clean[df_clean['Education'].isin(selected_education)].groupby('Education')[selected_column].count().reset_index() 
    fig = px.bar(grouped_df, x='Education', y=selected_column, color='Education', title=f"Grouped by {selected_column}")
    st.plotly_chart(fig)


    st.markdown('***')

    col1 , col2 = st.columns(2)

    with col1:
        # Create multi select dropdown for unique values in 'Category' column
        selected_marital = st.multiselect("Select Marital Status", df_clean['MaritalStatus'].unique())

    with col2:
        # Create dropdown for selecting column names
        selected_column = st.selectbox("Select Column to Group By", ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'])
    
    grouped_df = df_clean[df_clean['MaritalStatus'].isin(selected_marital)].groupby('MaritalStatus')[selected_column].sum().reset_index() 
    fig = px.pie(grouped_df, values=selected_column, names='MaritalStatus', title='Most Products with respect to Marital Status')
    #px.pie(grouped_df, x=selected_column, y='MaritalStatus', color='MaritalStatus', title=f"Grouped by {selected_column}")
    st.plotly_chart(fig)


# st.plotly_chart(px.bar(filtered_df, x=group_by_columns[0], y='Count', color=group_by_columns[1], barmode='group'))


    # st.write('## Bar Chart')
    # bar_fig = px.bar(data, x='category_column', y='numeric_column')
    # st.plotly_chart(bar_fig)

    # st.write('## Line Chart')
    # line_fig = px.line(data, x='date_column', y='numeric_column')
    # st.plotly_chart(line_fig)

    # st.write('## Histogram')
    # hist_fig = px.histogram(data, x='numeric_column')
    # st.plotly_chart(hist_fig)
