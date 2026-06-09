import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


def download_button(df, filename, label="Download Data as CSV"):
    import streamlit as st
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime='text/csv',
    )


def get_sport_list(df):
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    return sport_list


def sport_top_countries(df, sport):
    temp = df[df['Sport'] == sport]
    temp = temp[temp['Medal'].notna()]
    result = temp.groupby('region')['Medal'].count().reset_index()
    result.columns = ['Country', 'Total Medals']
    result = result.sort_values('Total Medals', ascending=False).head(10)
    return result


def sport_top_athletes(df, sport):
    temp = df[df['Sport'] == sport]
    temp = temp[temp['Medal'].notna()]
    result = temp.groupby('Name')['Medal'].count().reset_index()
    result.columns = ['Athlete', 'Total Medals']
    result = result.sort_values('Total Medals', ascending=False).head(10)
    return result


def sport_over_years(df, sport):
    temp = df[df['Sport'] == sport]
    result = temp.groupby('Year')['Name'].nunique().reset_index()
    result.columns = ['Year', 'Number of Athletes']
    return result


def sport_medal_distribution(df, sport):
    temp = df[df['Sport'] == sport]
    temp = temp[temp['Medal'].notna()]
    result = temp['Medal'].value_counts().reset_index()
    result.columns = ['Medal', 'Count']
    return result


def sport_gender_distribution(df, sport):
    temp = df[df['Sport'] == sport]
    result = temp.groupby(['Year', 'Sex'])['Name'].nunique().reset_index()
    result.columns = ['Year', 'Gender', 'Count']
    return result


def country_medal_map(df, medal_type='Total'):
    temp = df.dropna(subset=['Medal'])

    if medal_type == 'Total':
        result = temp.groupby('region')['Medal'].count().reset_index()
        result.columns = ['Country', 'Total Medals']
        color_col = 'Total Medals'
    else:
        result = temp[temp['Medal'] == medal_type].groupby('region')['Medal'].count().reset_index()
        result.columns = ['Country', f'{medal_type} Medals']
        color_col = f'{medal_type} Medals'

    return result, color_col


def get_country_stats(df, country):
    temp = df[df['region'] == country]

    total_medals = temp[temp['Medal'].notna()]['Medal'].count()
    gold = temp[temp['Medal'] == 'Gold']['Medal'].count()
    silver = temp[temp['Medal'] == 'Silver']['Medal'].count()
    bronze = temp[temp['Medal'] == 'Bronze']['Medal'].count()
    total_athletes = temp['Name'].nunique()
    total_sports = temp['Sport'].nunique()
    total_years = temp['Year'].nunique()

    stats = {
        'Total Medals': total_medals,
        'Gold': gold,
        'Silver': silver,
        'Bronze': bronze,
        'Total Athletes': total_athletes,
        'Total Sports': total_sports,
        'Olympics Participated': total_years
    }

    return stats


def country_year_medals(df, country):
    temp = df[df['region'] == country]
    temp = temp[temp['Medal'].notna()]
    result = temp.groupby('Year')['Medal'].count().reset_index()
    result.columns = ['Year', 'Medals']
    return result


def country_top_sports(df, country):
    temp = df[df['region'] == country]
    temp = temp[temp['Medal'].notna()]
    result = temp.groupby('Sport')['Medal'].count().reset_index()
    result.columns = ['Sport', 'Medals']
    result = result.sort_values('Medals', ascending=False).head(10)
    return result


def country_top_athletes(df, country):
    temp = df[df['region'] == country]
    temp = temp[temp['Medal'].notna()]
    result = temp.groupby('Name')['Medal'].count().reset_index()
    result.columns = ['Athlete', 'Medals']
    result = result.sort_values('Medals', ascending=False).head(10)
    return result


def get_athlete_list(df):
    athletes = df[df['Medal'].notna()]['Name'].unique().tolist()
    athletes.sort()
    return athletes


def get_athlete_stats(df, athlete):
    temp = df[df['Name'] == athlete]

    stats = {
        'Country': temp['region'].iloc[0] if len(temp) > 0 else 'Unknown',
        'Sport': temp['Sport'].iloc[0] if len(temp) > 0 else 'Unknown',
        'Total Medals': int(temp[temp['Medal'].notna()]['Medal'].count()),
        'Gold': int(temp[temp['Medal'] == 'Gold']['Medal'].count()),
        'Silver': int(temp[temp['Medal'] == 'Silver']['Medal'].count()),
        'Bronze': int(temp[temp['Medal'] == 'Bronze']['Medal'].count()),
        'Olympics Participated': int(temp['Year'].nunique()),
        'Years Active': f"{temp['Year'].min()} - {temp['Year'].max()}",
        'Events': int(temp['Event'].nunique())
    }

    return stats