import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
# create a function to load the dataset
def load_data():
    df= pd.read_csv("supermarket_sales new.csv")
    df.loc[:,"Revenue"] =(df['Unit price'] * df['Quantity']) - df['Tax 5%']

    return df

# load dataset

data = load_data()

#create a title for the app

st.title("Supermarket sales Analysis")

# add a filter
filters = {
    "Gender": data["Gender"].unique(),
    "Branch": data["Branch"].unique(),
    "City": data["City"].unique(),
    "Customer type": data["Customer type"].unique(),
    "Product line": data[ "Product line"].unique()
}
# store user selection
selected_filters ={}

# generate multi-select widgets dynamically
for key, options in filters.items():
    selected_filters[key]=st.sidebar.multiselect(key,options)

# add a dynamic filter 
filtered_data = data # start with the full data
for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_data = filtered_data[filtered_data[key].isin(selected_values)]
                                                              
# dispaly the data in the browser
st.dataframe(filtered_data)

# calculate total revenue, total quantity, average unit price, average tax
no_of_items = len(data)
total_revenue = data["Revenue"].sum()
total_qty = data["Quantity"].sum()
avg_price = data["Unit price"].mean()
avg_tax = data["Tax 5%"].mean()

# streamlit column component 
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("No of Items", no_of_items)
    
with col2:
     st.metric("Total Revenue", total_revenue)

with col3:
    st.metric("Total Qty", total_qty)

with col4:
    st.metric("Avg Unit Price", avg_price)

with col5:
    st.metric("Avg Tax", avg_tax)
    

# find the product with the highest revenue
# use a bar chart

con = st.container()

with con:
    # plotly chart
    bar1 = px.bar(data, x="Product line", y="Revenue")
    st.plotly_chart(bar1)



