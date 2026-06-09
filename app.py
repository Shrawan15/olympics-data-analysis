import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocessor
import helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

st.set_page_config(page_title="Olympics Analysis", page_icon="🏅", layout="wide")

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://miro.medium.com/v2/resize:fit:928/1*VMlX9-xnnS9Gc-vFgLwf0Q.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Home', 'Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis', 'Sport-wise Analysis', 'World Map', 'Country Comparison', 'Athlete Comparison')
)


if user_menu == 'Home':
    st.title("🏅 Olympic Games Analysis Dashboard")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Editions", df['Year'].nunique())
    with col2:
        st.metric("Host Cities", df['City'].nunique())
    with col3:
        st.metric("Sports", df['Sport'].nunique())
    with col4:
        st.metric("Athletes", df['Name'].nunique())
    st.markdown("---")
    st.markdown("### Welcome! Analysis from 1896 to 2016")
    st.markdown("""
    #### What you can explore:
    - **Medal Tally** - View medals by country and year
    - **Overall Analysis** - Participation trends over 120 years
    - **Country-wise Analysis** - Deep dive into any country
    - **Athlete-wise Analysis** - Age, height, weight analysis
    - **Sport-wise Analysis** - Explore specific sports
    - **World Map** - Global medal distribution
    - **Country Comparison** - Compare two countries
    - **Athlete Comparison** - Compare two athletes
    """)
    st.info("Select an option from the sidebar to get started!")


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.title("Medal Tally")
    st.table(medal_tally)
    helper.download_button(medal_tally, "medal_tally.csv")


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig, use_container_width=True)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig, use_container_width=True)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)
    helper.download_button(x, "most_successful.csv")


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig, use_container_width=True)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if not pt.empty:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    else:
        st.info("Not enough data for heatmap")

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
    helper.download_button(top10_df, "top10_athletes.csv")


if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.title('Height Vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list, key='hw')
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig, use_container_width=True)


if user_menu == 'Sport-wise Analysis':
    st.title("⚽ Sport-wise Deep Analysis")
    sport_list = helper.get_sport_list(df)
    selected_sport = st.sidebar.selectbox("Select a Sport", sport_list)
    st.header(f"Analysis of {selected_sport}")
    st.markdown("---")

    st.subheader(f"Top 10 Countries in {selected_sport}")
    top_countries = helper.sport_top_countries(df, selected_sport)
    fig = px.bar(top_countries, x='Country', y='Total Medals', color='Total Medals', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    helper.download_button(top_countries, f"{selected_sport}_top_countries.csv")

    st.markdown("---")
    st.subheader(f"Top 10 Athletes in {selected_sport}")
    top_athletes = helper.sport_top_athletes(df, selected_sport)
    fig = px.bar(top_athletes, x='Athlete', y='Total Medals', color='Total Medals', color_continuous_scale='Oranges')
    st.plotly_chart(fig, use_container_width=True)
    helper.download_button(top_athletes, f"{selected_sport}_top_athletes.csv")

    st.markdown("---")
    st.subheader(f"Participation Trend in {selected_sport}")
    sport_years = helper.sport_over_years(df, selected_sport)
    fig = px.line(sport_years, x='Year', y='Number of Athletes', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medal Distribution")
        medal_dist = helper.sport_medal_distribution(df, selected_sport)
        fig = px.pie(medal_dist, values='Count', names='Medal', color='Medal', color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Gender Participation")
        gender_dist = helper.sport_gender_distribution(df, selected_sport)
        fig = px.line(gender_dist, x='Year', y='Count', color='Gender', markers=True)
        st.plotly_chart(fig, use_container_width=True)


if user_menu == 'World Map':
    st.title("🗺️ World Medal Map")
    st.markdown("---")
    medal_type = st.sidebar.selectbox("Select Medal Type", ['Total', 'Gold', 'Silver', 'Bronze'])
    medal_data, color_col = helper.country_medal_map(df, medal_type)
    fig = px.choropleth(medal_data, locations="Country", locationmode="country names", color=color_col, hover_name="Country", color_continuous_scale="YlOrRd", title=f"{medal_type} Medal Distribution Across the World")
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True), height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top 20 Countries")
    top20 = medal_data.sort_values(color_col, ascending=False).head(20)
    st.dataframe(top20, use_container_width=True)
    helper.download_button(medal_data, "world_medal_data.csv")


if user_menu == 'Country Comparison':
    st.title("⚔️ Country vs Country Comparison")
    st.markdown("---")
    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select Country 1", countries, index=0)
    with col2:
        country2 = st.selectbox("Select Country 2", countries, index=1)

    if country1 == country2:
        st.warning("Please select two different countries!")
    else:
        st.markdown("---")
        stats1 = helper.get_country_stats(df, country1)
        stats2 = helper.get_country_stats(df, country2)

        st.subheader("Overall Stats Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {country1}")
            for key, value in stats1.items():
                st.metric(key, value)
        with col2:
            st.markdown(f"### {country2}")
            for key, value in stats2.items():
                st.metric(key, value)

        st.markdown("---")
        st.subheader("Medal Trend Over Years")
        medals1 = helper.country_year_medals(df, country1)
        medals1['Country'] = country1
        medals2 = helper.country_year_medals(df, country2)
        medals2['Country'] = country2
        combined = pd.concat([medals1, medals2])
        fig = px.line(combined, x='Year', y='Medals', color='Country', markers=True, title=f'{country1} vs {country2}')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Top Sports Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### {country1}")
            sports1 = helper.country_top_sports(df, country1)
            fig1 = px.bar(sports1, x='Medals', y='Sport', orientation='h', color='Medals', color_continuous_scale='Blues')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.markdown(f"#### {country2}")
            sports2 = helper.country_top_sports(df, country2)
            fig2 = px.bar(sports2, x='Medals', y='Sport', orientation='h', color='Medals', color_continuous_scale='Reds')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("Top Athletes Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### {country1}")
            athletes1 = helper.country_top_athletes(df, country1)
            st.dataframe(athletes1, use_container_width=True)
        with col2:
            st.markdown(f"#### {country2}")
            athletes2 = helper.country_top_athletes(df, country2)
            st.dataframe(athletes2, use_container_width=True)


if user_menu == 'Athlete Comparison':
    st.title("👥 Athlete vs Athlete Comparison")
    st.markdown("---")
    athlete_list = helper.get_athlete_list(df)
    col1, col2 = st.columns(2)
    with col1:
        athlete1 = st.selectbox("Select Athlete 1", athlete_list, index=0)
    with col2:
        athlete2 = st.selectbox("Select Athlete 2", athlete_list, index=1)

    if athlete1 == athlete2:
        st.warning("Please select two different athletes!")
    else:
        st.markdown("---")
        stats1 = helper.get_athlete_stats(df, athlete1)
        stats2 = helper.get_athlete_stats(df, athlete2)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {athlete1}")
            for key, value in stats1.items():
                st.metric(key, value)
        with col2:
            st.markdown(f"### {athlete2}")
            for key, value in stats2.items():
                st.metric(key, value)

        st.markdown("---")
        st.subheader("Medal Comparison")
        comparison_data = pd.DataFrame({
            'Medal Type': ['Gold', 'Silver', 'Bronze'],
            athlete1: [stats1['Gold'], stats1['Silver'], stats1['Bronze']],
            athlete2: [stats2['Gold'], stats2['Silver'], stats2['Bronze']]
        })
        fig = px.bar(comparison_data, x='Medal Type', y=[athlete1, athlete2], barmode='group', title='Medal Comparison', color_discrete_sequence=['#FFD700', '#4169E1'])
        st.plotly_chart(fig, use_container_width=True)