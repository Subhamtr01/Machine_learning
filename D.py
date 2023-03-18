

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import sys
sys.set_int_max_str_digits(0)


st.set_page_config(page_title="Adidas sales Dashboard",
                  page_icon="bar_chart:",
                  layout="wide")


# In[ ]:

# In[14]:
df = pd.read_csv("a.csv")




df1=df.sort_values("Price per Unit")

# In[15]:


df = df.set_index("Retailer")

st.sidebar.header('Please Filter Here:')
Region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique())


# In[ ]:
Product = st.sidebar.multiselect(
    "Select the store:",
    options=df["Product"].unique(),
    default=df["Product"].unique())


Sales_Method = st.sidebar.multiselect(
    "Select the store:",
    options=df["Sales_Method"].unique(),
    default=df["Sales_Method"].unique())

df_selection = df1.query(
    "Region ==@Region & Product ==@Product & Sales_Method ==@Sales_Method")
st.dataframe(df_selection)


Pie_chart= px.pie(df_selection, title='Price per Unit', values='Units_Sold',  color_discrete_sequence=["#0083B8"], names='Product')
Regional_sales =px.pie(df_selection, title='Sale Region Wise', values='Total_Sales', color_discrete_sequence=["#0083B8"], names='Region')



right_column, left_column= st.columns(2)
right_column.plotly_chart(Pie_chart, use_container_width=True)
left_column.plotly_chart(Regional_sales, use_container_width=True)

Histo = px.histogram(df, x="Price per Unit", nbins=20)
Store_sales =px.pie(df_selection, title='Sale Store Wise', values='Total_Sales', color_discrete_sequence=["#0083B8"],names='Sales_Method')

right_column, left_column= st.columns(2)
left_column.plotly_chart( Histo,use_container_width=True)
right_column.plotly_chart( Store_sales,use_container_width=True)


df2=df_selection.copy()

df2['Region']=pd.factorize(df2.Region)[0]
df2['State']=pd.factorize(df2.State)[0]
df2['City']=pd.factorize(df2.City)[0]
df2['Product']=pd.factorize(df2.Product)[0]
df2['Retailer']=pd.factorize(df2.Retailer)[0]

df2.rename(columns = {'Sales_Method':'Method'}, inplace = True)
df2['Method']=pd.factorize(df2.Method)[0]
df2 = df2.drop('Retailer ID',axis=1)
df2 = df2.drop('Invoice Date',axis=1)
df2.head()

corr=df2.corr()
print(corr)


fig = px.imshow(df2.corr())



map = px.choropleth(df_selection,
                        locations = 'State',
                        locationmode = 'USA-states',
                        scope = 'usa',
                        color = 'Total_Sales',
                        hover_name = 'State',
                        hover_data = ['Total_Sales'],
                        range_color = [00,825000],
                        color_continuous_scale = 'blues',
                        title = 'Sales state wise')


right_column, left_column= st.columns(2)
right_column.write(fig, use_container_width=True)
left_column.write(map)


hide_st_style = """
            <style>
            #mainMenu {Visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

