import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")

else:
    os.chdir(r"E:\materials\streamlit_projects\superstore")
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")


col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# getting the start and end date of the data
start_date = pd.to_datetime(df["Order Date"]).min()
end_date = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", end_date))


df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose the Filter: ")

# create region filter 
region = st.sidebar.multiselect("Select the Region", df["Region"].unique())

if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)].copy()

# create sate filter
state = st.sidebar.multiselect("Select the State", df2["State"].unique())

if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)].copy()

# create city filter
city = st.sidebar.multiselect("Select the City", df3["City"].unique())

if not city and not state and not region:
    filtered_data = df.copy()

elif not city and not state:
    filtered_data = df[df["Region"].isin(region)].copy()

elif not city and not region:
    filtered_data = df[df["State"].isin(state)].copy()

elif city and state:
    filtered_data = df3[df["State"].isin(state) & df3["City"].isin(city)].copy()

elif city and region:
    filtered_data = df3[df["Region"].isin(region) & df3["City"].isin(city)].copy()

elif state and region:
    filtered_data = df3[df["Region"].isin(region) & df3["State"].isin(state)].copy()

elif city:
    filtered_data = df3[df3["City"].isin(city)].copy()

else:
    filtered_data = df3[df3["Region"].isin(region) & 
                        df3["State"].isin(state) & 
                        df3["City"].isin(city)].copy()


# create category filter
category_data = filtered_data.groupby(by = ["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Sales Distribution by Category")
    fig = px.bar(category_data, x = "Category", y = "Sales", 
                text = ['${:,.2f}'.format(x) for x in category_data["Sales"]],
                template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Sales Share by Region")
    fig = px.pie(filtered_data, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtered_data["Region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category View Data"):
        st.write(category_data.style.background_gradient(cmap = "Blues"))
        category_csv = category_data.to_csv(index = False).encode('utf-8')
        st.download_button("Download as csv", data = category_csv, 
                    file_name = "Category.csv", mime = "text/csv",
                    help = "Click here to download the data in csv format")

region_data = filtered_data.groupby(by = ["Region"], as_index = False)["Sales"].sum()
with cl2:
    with st.expander("Region View Data"):
        st.write(region_data.style.background_gradient(cmap = "Oranges"))
        region_csv = region_data.to_csv(index = False).encode('utf-8')
        st.download_button("Download as csv", data = region_csv, 
                    file_name = "Region.csv", mime = "text/csv",
                    help = "Click here to download the data in csv format")



#  Time Series Analysis
filtered_data["month_year"] = filtered_data["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart_df = pd.DataFrame(filtered_data.groupby(
                                by = filtered_data["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line( linechart_df, x = "month_year", y = "Sales",
                labels = {"Sales":"Amount"}, height=500, width=1000,
                template="gridon" )
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of the Time Series Analysis"):
    st.write(linechart_df.T.style.background_gradient(cmap = "Blues"))
    linechart_csv = linechart_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download as csv", data = linechart_csv, 
                    file_name = "Linechart.csv", mime = "text/csv",
                    help = "Click here to download the data in csv format")


# create a tree structure based on Region, Category, and Sub-Category
st.subheader("Tree Structure of the Data by TreeMap")
fig3 = px.treemap(filtered_data, path = ["Region", "Category", "Sub-Category"], 
                values = "Sales", color = "Sub-Category", hover_data = ["Sales"])
fig3.update_layout(height = 650, width = 800)
st.plotly_chart(fig3, use_container_width=True)


chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Sales Distribution by Segment")
    fig = px.pie(filtered_data, names = "Segment", values = "Sales",
                template = "gridon")
    fig.update_traces(
        text=filtered_data["Segment"], 
        textposition="inside",
        insidetextfont=dict(family="Arial Black", size=11, color="black")  
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Sales Distribution by Category")
    fig = px.pie(filtered_data, names = "Category", values = "Sales",
                template = "plotly_dark")
    fig.update_traces(
        text=filtered_data["Category"], 
        textposition="inside",
        insidetextfont=dict(family="Arial Black", size=11, color="black")  
    )
    st.plotly_chart(fig, use_container_width=True)




st.subheader(":point_right: Summary of sub-category sales by month")

with st.expander("Summary of sub-category sales by month"):
    summary_df = df[0:5][['Region', 'Category', 'Quantity', 'City', 'Profit', 'State', 'Sales']]
    fig = ff.create_table(summary_df, colorscale='cividis')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Table of sub-categories organized by month")

    filtered_data["month"] = filtered_data["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_data, values = "Sales", 
                                index = ["Sub-Category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))


# create a scatter plot of the data
scattered_data = px.scatter(filtered_data, x = "Sales", y = "Profit",
                            size = "Quantity")
scattered_data['layout'].update(titlefont = dict(size = 19),
                        title = "Visualizing the relationship between sales and profits using a scatter plot",
                        xaxis = dict(title = "Sales", titlefont = dict(size = 17)),
                        yaxis = dict(title = "Profit", titlefont = dict(size = 17)))

st.plotly_chart(scattered_data, use_container_width=True)



# let the user view and download the data

with st.expander("View Data"):
    st.write(filtered_data.iloc[0:500, 1:20:2].style.background_gradient(cmap = "Reds"))

data_csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download as csv", data = data_csv, 
                    file_name = "Superstore.csv", mime = "text/csv",
                    help = "Click here to download the data in csv format")

