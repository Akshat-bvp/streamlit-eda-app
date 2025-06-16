import numpy as np 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report
import jinja2

st.set_page_config(page_title="EDA & Visualization App", layout="wide")
st.markdown("Upload your CSV file to get started with ExploratOry Data Analytics ", type="csv")

#File uploader

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head())


    st.write("**Shape of Dataset", df.shape)
    st.write("**Column data types**")
    st.dataframe(df.dtypes)

    #Missing Values
    st..subheader("? Missing Values")
    missing = df.isnull().sum()
    st.write(missing[missing > 0])

    #Data Cleaning Python
    st.subheader("🧹 Data Cleaning")
    st.markdown("""
    This option lets users choose how to handle missing values
    - **Do nothing**: Keep the data as-is
    - **Drop rows with missing values**: Remove any row that contains a missing value.
    - **Fill with mean (numerics only)**: Replace missing numeric values with the column mean.
    """)
    cleaning_options = st.radio("Handle missing values by:", 
    ["Do-nothing", "Drop rows with missing vakues", "Fill with mean(numerics only)"]
    )
    if cleaning_option == "Drop rows with missing values":
        df = df.dropna()
        st.success("Dropped rows with missing values")
    elif cleaning_option == "Fill with mean (numeric only)":
        df = df.fillna(df.mean(numeric_only = True))
        st.success("Filled missing numeric values with mean")


    #Descriptive stats
    st.subheader("📈 Descriptive Statistics")
    st.write(df.describe())

    #profiling Report
    st.subheader("🧠 Pandas Profiling Report")
    profile = df.profile_report(title="Pandas Profiling Report")
    st_profile_report(profile)

    #Column Selector
    st.subheader("📊 Visualization")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).column.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category'].columns.tolist())

    plot_type = st.selectbox("Choose plot type", ["Histogram", "Boxplot", "Swarmplot", "Correlation Heatmap"])

    if plot_type == "Histogram":
        column = st.selectbox("Select a numeric column", numeric_cols)
        fig = px.histogram(df, x=column, nbins=30, title=f"Histogram of {column}")
        st.ploty_chart(fig, use_container_width=True)

    elif plot_type == "Boxplot":
        y = st.selectbox("Select numeric column",numeric_cols)
        x = st.selectbox("Select categorical column for X axis", categorical_cols)
        fig = px.box(df, x=x, y=y, title=f"Boxplot of {y} by {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Swarmplot":
        y = st.selectbox("Select numeric column for Y axis (swarmplot)", numeric_cols)
        x = st.selectbox("Select categorical column for X axis (swarmplot)", categorical_cols)
        fig, ax = plt.subplots()
        sns.swarmplot(data=df, x=x, y=y, ax=ax)
        st.pyplot(fig)

    elif plot_type == "Scatterplot":
        x = st.selectbox("X axis", numeric_cols)
        y = st.selectbox("Y axis", numeric cols)
        color = st.selectbox("Color by (optional)", [None] + categorical_cols)
        fig = px.scatter(df, x=x, y=y, color=color, title=f"Scatterplot of {y} vs {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Correlation Heatmap":
        st.write("Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)  

    else:
        st.info("👆 Upload a CSV file to start.") 

        
                       




