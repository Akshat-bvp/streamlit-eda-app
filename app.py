import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report

# Page config
st.set_page_config(page_title="EDA & Visualization App", layout="wide")
st.title("🔍 EDA & Visualization App")
st.markdown("Upload your CSV file to get started with **Exploratory Data Analytics**.")

# File uploader
uploaded_file = st.file_uploader("📂 Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    st.write(f"**Shape of Dataset:** {df.shape}")
    st.write("**Column Data Types:**")
    st.dataframe(df.dtypes)

    # Missing Values
    st.subheader("❓ Missing Values")
    missing = df.isnull().sum()
    st.write(missing[missing > 0])

    # Data Cleaning Options
    st.subheader("🧹 Data Cleaning")
    st.markdown("""
    This option lets users choose how to handle missing values:
    - **Do nothing**: Keep the data as-is
    - **Drop rows with missing values**: Remove any row that contains a missing value.
    - **Fill with mean (numerics only)**: Replace missing numeric values with the column mean.
    """)

    cleaning_option = st.radio("Handle missing values by:", 
                               ["Do nothing", "Drop rows with missing values", "Fill with mean (numerics only)"])

    if cleaning_option == "Drop rows with missing values":
        df = df.dropna()
        st.success("✅ Dropped rows with missing values.")
    elif cleaning_option == "Fill with mean (numerics only)":
        df = df.fillna(df.mean(numeric_only=True))
        st.success("✅ Filled missing numeric values with mean.")

    # Descriptive Statistics
    st.subheader("📊 Descriptive Statistics")
    st.write(df.describe())

    # Pandas Profiling Report
    st.subheader("🧠 Pandas Profiling Report")
    profile = df.profile_report(title="Pandas Profiling Report")
    st_profile_report(profile)

    # Column Selectors
    st.subheader("📈 Visualisation")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    plot_type = st.selectbox("Choose plot type", 
                             ["Histogram", "Boxplot", "Swarmplot", "Scatterplot", "Correlation Heatmap"])

    if plot_type == "Histogram":
        column = st.selectbox("Select a numeric column", numeric_cols)
        fig = px.histogram(df, x=column, nbins=30, title=f"Histogram of {column}")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Boxplot":
        y = st.selectbox("Select numeric column", numeric_cols)
        x = st.selectbox("Select categorical column for X axis", categorical_cols)
        fig = px.box(df, x=x, y=y, title=f"Boxplot of {y} by {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Swarmplot":
        y = st.selectbox("Select numeric column for Y axis (Swarmplot)", numeric_cols)
        x = st.selectbox("Select categorical column for X axis (Swarmplot)", categorical_cols)
        fig, ax = plt.subplots()
        sns.swarmplot(data=df, x=x, y=y, ax=ax)
        st.pyplot(fig)

    elif plot_type == "Scatterplot":
        x = st.selectbox("X axis", numeric_cols)
        y = st.selectbox("Y axis", numeric_cols)
        color = st.selectbox("Colour by (optional)", [None] + categorical_cols)
        fig = px.scatter(df, x=x, y=y, color=color, title=f"Scatterplot of {y} vs {x}")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Correlation Heatmap":
        st.write("📉 Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
else:
    st.info("👆 Upload a CSV file to get started.")
