import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import pandas_datareader.data as web
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from PIL import Image
import requests
import json
from streamlit_lottie import st_lottie
import re


selected = option_menu(
    menu_title=None,
    options=['Home', 'Dashboard', 'Prediction'],
    icons=['house', '', ''],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important", "background-color": "#11e2"},
        "icon": {},
        "nav-link": {
            "font-size": "14px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "green"}
    },
)

if selected == "Home":

    with st.container():
        st.subheader("UTT AMIS NAV FORECASTING")
        st.write('Your Obvious Investment Partner')
        # image = Image.open('images/inv.jpeg')
        # st.image(image, caption='Unlock the Future of Your Investments!', width=700)
    with st.container():
        left_col, right_col = st.columns(2)
        with left_col:
            st.write("Welcome to the NAV Forecasting System, your gateway to informed investment decisions. We empower you to anticipate and plan for the future of your investments with precision and confidence. Whether you're a seasoned investor or just starting your journey, our cutting-edge forecasting tools and insights will be your financial compass.")
            st.write("[Learn more](https://www.uttamis.co.tz/)")
        with right_col:
            def load_lottiefile(filepath: str):
                with open(filepath, "r") as f:
                    return json.load(f)
            lottie_inv = load_lottiefile("images/investor.json")
            st.lottie(
                lottie_inv,
                speed=1,
                reverse=False,
                loop=True,
                quality="medium",
                # renderer="svg",
                height=None,
                width=None,
                key=None,
            )
    with st.container():
        st.write("---")
        st.header('Why Choose Us?')
        st.write("1. Accurate Predictions: Our advanced algorithms provide highly accurate forecasts of Net Asset Value (NAV) for various investment schemes.")
        st.write("2. Diverse Schemes: Explore and forecast NAV for six different investment schemes, including mutual funds, ETFs, and more.")
        st.write("3. User-Friendly Interface: Our intuitive interface makes it easy for anyone, regardless of experience, to access powerful investment analytics.")
        st.write("4. In-Depth Analysis: Dive deeper into historical NAV data, trends, and visualizations, enabling you to make data-driven investment decisions.")
        st.write(
            "5. Plan Your Future: Secure your financial future by making informed investment choices.")

    with st.container():
        st.markdown(
            """<div style="text-align:center">
            <h3>Our Product</h3>
            </div>""",
            unsafe_allow_html=True
        )
        umoja, wekeza, watoto = st.columns(3)
        with umoja:
            imageU = Image.open('images/umoja-fund-logo.gif')
            st.image(imageU, caption='')
            st.subheader('Umoja Fund')
            st.write('It is an open-ended balance fund that invests in a diversified portfolio which makes this fund best suited for a medium risk profile.')
        with wekeza:
            imageU = Image.open('images/wekeza maisha.jpeg')
            st.image(imageU, caption='')
            st.subheader('Wekeza  Fund')
            st.write('The Wekeza Maisha/Invest life Unit Trust is the first investment cum insurance scheme to be established by UTT AMIS in the country.')

        with watoto:
            imageU = Image.open('images/watoto1.jpeg')
            st.image(imageU, caption='')
            st.subheader('Watoto Fund')
            st.write(
                'A child benefits an open-end balanced fund, which seeks to generate long-term capital appreciation.')
        with st.container():
            jikimu, liquid, bond = st.columns(3)
            with jikimu:
                imageJ = Image.open('images/jikimu logo.jpeg')
                st.image(imageJ, caption='')
                st.subheader('Jikimu Fund')
                st.write(
                    'It is an open-ended balance fund that invests in a diversified portfolio which makes this fund best suited for a medium risk profile.')
            with liquid:
                imageL = Image.open('images/liquid_logo.jpeg')
                st.image(imageL, caption='')
                st.subheader('Liquid  Fund')
                st.write(
                    'The Wekeza Maisha/Invest life Unit Trust is the first investment cum insurance scheme to be established by UTT AMIS in the country.')
            with bond:
                imageB = Image.open('images/bondfund.jpeg')
                st.image(imageB, caption='')
                st.subheader('Bond Fund')
                st.write(
                    'A child benefits an open-end balanced fund, which seeks to generate long-term capital appreciation')
        with st.container():
            st.subheader('Get started:')
            st.write('1. Select your preferred investment scheme.')
            st.write('2. Explore historical data and trends.')
            st.write('3. Get highly accurate forecasts for your investments.')


if selected == "Dashboard":

    @st.cache_data
    def load_data():
        df = pd.read_csv('Data/nat2.csv')

        # Clean and extract numbers
        def clean_and_extract_number(s):
            cleaned_value = re.sub(r'[^\d.]', '', str(s))
            return cleaned_value

        numeric_columns = ['Net Asset Value', 'Outstanding Number of Units']
        for col in numeric_columns:
            df[col] = df[col].apply(clean_and_extract_number)
        df[numeric_columns] = df[numeric_columns].apply(
            pd.to_numeric, errors='coerce')

        # Custom date conversion
        def custom_date_conversion(date_str):
            try:
                return pd.to_datetime(date_str)
            except:
                pass
            return pd.NaT

        df["Date Valued"] = df["Date Valued"].apply(custom_date_conversion)
        df['Year'] = df['Date Valued'].dt.year
        df['Month'] = df['Date Valued'].dt.month
        df['Week'] = df['Date Valued'].dt.isocalendar().week
        df['Day'] = df['Date Valued'].dt.day

        return df, df["Date Valued"].isna().sum()

    df, nat_values = load_data()

    st.sidebar.image('uttamislogof.png',
                     caption='Your Obvious Investment Partner')

    # Display alerts based on nat_values
    if nat_values > 0:
        st.warning(f"Warning: {nat_values} values could not be converted.")
    else:
        st.success("Date conversion successful!")

    # Data Overview
    st.write("## Data Overview")
    st.write("Here's a glimpse of the dataset:")
    st.write(df.head())

    st.write("Basic statistics of the dataset:")
    st.write(df.describe(include='all').T)

    # Sidebar additions
    st.sidebar.write("Choose a visualization:")

    # Unified sidebar settings for scheme, year, and month selection
    schemes = df['Scheme Name'].unique().tolist()
    selected_scheme = st.sidebar.selectbox(
        'Select a scheme for visualization:', schemes, key='scheme_select')
    years = sorted(df['Year'].unique().tolist())
    selected_year = st.sidebar.selectbox(
        'Select a year:', years, key='year_select')
    months = list(range(1, 13))
    selected_month = st.sidebar.selectbox(
        'Select a month:', months, key='month_select')

    monthly_data = df[(df['Scheme Name'] == selected_scheme) &
                      (df['Year'] == selected_year) &
                      (df['Month'] == selected_month)]

    filtered_df = df[df['Scheme Name'] == selected_scheme]

    # Time Series Plot for NAV
    st.write("## Time Series Plot of NAV values")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=filtered_df, x='Year', y='Net Asset Value')
    plt.title(f"Net Asset Value Trend for {selected_scheme} Over the Years")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Time Series Plot for Nav Per Unit
    st.write("## Time Series Plot of Nav Per Unit")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=filtered_df, x='Year', y='Nav Per Unit')
    plt.title(f"Nav Per Unit Trend for {selected_scheme} Over the Years")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Monthly Trend Plot for Nav Per Unit
    st.write(
        f"## Monthly Trend Plot of Nav Per Unit for {selected_month}/{selected_year}")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=monthly_data, x='Day', y='Nav Per Unit')
    plt.title(
        f"Nav Per Unit for {selected_month}/{selected_year} for {selected_scheme}")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Monthly Trend Plot for NAV
    st.write(
        f"## Monthly Trend Plot of NAV values for {selected_month}/{selected_year}")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=monthly_data, x='Day', y='Net Asset Value')
    plt.title(
        f"NAV values for {selected_month}/{selected_year} for {selected_scheme}")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Monthly Trend Plot with Outstanding Number of Units Bar Overlay
    st.write("## Monthly Trend Plot of NAV values with Outstanding Number of Units")
    st.write(
        f"Displaying NAV values for {selected_month}/{selected_year} for scheme: {selected_scheme}")
    monthly_data = df[(df['Scheme Name'] == selected_scheme) &
                      (df['Year'] == selected_year) &
                      (df['Month'] == selected_month)]
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Bar plot for Outstanding Number of Units
    ax1.bar(monthly_data['Day'], monthly_data['Outstanding Number of Units'],
            color='gray', alpha=0.5, label='Outstanding Number of Units')
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Outstanding Number of Units', color='gray')
    ax1.tick_params(axis='y', labelcolor='gray')
    ax1.set_title(
        f"NAV values & Outstanding Units for {selected_month}/{selected_year} for {selected_scheme}")

    # Line plot for NAV values
    ax2 = ax1.twinx()
    sns.lineplot(data=monthly_data, x='Day', y='Net Asset Value',
                 ax=ax2, color='blue', label='NAV Value')
    ax2.set_ylabel('Net Asset Value', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.xticks(rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    st.write("\n")
    st.write("""
    Overlaying the outstanding number of units with the NAV values provides a holistic view. While the NAV values give insights into the scheme's performance, the number of units can indicate the scheme's popularity or trustworthiness among investors.
    """)

    # Bar Plot of Average NAV Values for Top N Schemes
    st.write("## Average NAV Values for Top 10 Schemes")
    top_n = 10
    avg_nav = df.groupby('Scheme Name')['Net Asset Value'].mean(
    ).sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(14, 7))
    avg_nav.plot(kind='bar', color='skyblue')
    plt.title(f"Average NAV Values for Top {top_n} Schemes")
    plt.ylabel("Average NAV Value")
    plt.xlabel("Scheme Name")
    plt.xticks(rotation=45)
    st.pyplot(plt)
    st.write("\n")
    st.write("""
    Highlighting the top schemes based on their average NAV values can guide investors towards the best-performing schemes. However, past performance is not indicative of future results, so a deeper analysis and consultation with financial experts is recommended.
    """)

    # Facet Grid
    st.write(
        "### Relationship between NAV and Outstanding Number of Units - Faceted by Scheme")
    facet = sns.FacetGrid(df, col="Scheme Name", col_wrap=3,
                          height=3, sharex=False, sharey=False)
    facet.map(sns.scatterplot, "Net Asset Value",
              "Outstanding Number of Units", alpha=0.4)
    facet.add_legend()
    st.pyplot(plt)

    # Pair Plot
    st.write("### Pair Plot")
    sns.pairplot(data=df[[
                 'Net Asset Value', 'Outstanding Number of Units', 'Nav Per Unit']], diag_kind="kde")
    st.pyplot(plt)
    st.write("---")

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    correlation_matrix = df[['Net Asset Value',
                             'Outstanding Number of Units', 'Nav Per Unit']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    st.pyplot(plt)
    st.write("---")


if selected == "Prediction":
    st.sidebar.image('uttamislogof.png',
                     caption='Your Obvious Investment Partner')
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=['Demo', 'Demo', 'Demo', 'Demo', 'Demo', 'Demo'],
        )


# theme
hide_st_style = """

<style>



</style>



"""
