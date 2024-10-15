import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

import os
file_path = "Dashboard/all_data.csv"

if os.path.exists(file_path):
    all_df = pd.read_csv(file_path)
    print("File loaded successfully!")
else:
    print(f"File not found: {file_path}")

# Load the dataset
all_df = pd.read_csv("Dashboard/all_data.csv")

# Convert 'dteday' to datetime format
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Map season codes to season names
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
all_df['season_name'] = all_df['season'].map(season_map)

all_df['is_weekend'] = all_df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)

# Function 1: Temperature vs Rentals
def temperature_vs_rentals():
    st.subheader("Temperature vs Total Bike Rentals")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=all_df, hue='weathersit', palette='coolwarm', alpha=0.7)
    plt.title('Temperature vs Total Bike Rentals')
    plt.xlabel('Temperature')
    plt.ylabel('Total Bike Rentals')
    plt.legend(title='Weather Condition', loc='upper left')
    st.pyplot(plt)

# Function 2: Humidity vs Rentals
def humidity_vs_rentals():
    st.subheader("Humidity vs Total Bike Rentals")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hum', y='cnt', data=all_df, hue='weathersit', palette='coolwarm', alpha=0.7)
    plt.title('Humidity vs Total Bike Rentals')
    plt.xlabel('Humidity')
    plt.ylabel('Total Bike Rentals')
    plt.legend(title='Weather Condition', loc='upper left')
    st.pyplot(plt)

# Function 3: Correlation Heatmap
def correlation_heatmap():
    st.subheader("Correlation Matrix: Weather Features and Total Rentals")
    weather_cols = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
    correlation_matrix = all_df[weather_cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix: Weather Features and Total Rentals (cnt)')
    st.pyplot(plt)

# Function 4: Weekdays vs Weekends
def weekdays_vs_weekends():
    st.subheader("Average Bike Rentals: Weekdays vs Weekends")
    all_df['is_weekend'] = all_df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
    avg_rentals = all_df.groupby('is_weekend')['cnt'].mean().reset_index()
    avg_rentals['day_type'] = avg_rentals['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})

    plt.figure(figsize=(10, 6))
    sns.barplot(x='day_type', y='cnt', data=avg_rentals, palette='Set2')
    plt.title('Average Bike Rentals: Weekdays vs Weekends')
    plt.xlabel('Day Type')
    plt.ylabel('Average Total Bike Rentals')

    for i, v in enumerate(avg_rentals['cnt']):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom', fontweight='bold')

    plt.ylim(bottom=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function 5: Weekdays vs Weekends by Season
def weekdays_vs_weekends_by_season():
    st.subheader("Average Bike Rentals: Weekdays vs Weekends by Season")
    avg_rentals = all_df.groupby(['season_name', 'is_weekend'])['cnt'].mean().reset_index()
    avg_rentals['day_type'] = avg_rentals['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})

    plt.figure(figsize=(12, 6))
    sns.barplot(x='season_name', y='cnt', hue='day_type', data=avg_rentals, palette='Set2')
    plt.title('Average Bike Rentals: Weekdays vs Weekends by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Total Bike Rentals')
    plt.legend(title='Day Type')
    plt.ylim(bottom=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function 6: Hourly Rentals
def hourly_rentals():
    st.subheader("Average Bike Rentals by Hour of the Day")
    hourly_stats = all_df.groupby('hr')['cnt'].agg(['mean', 'sem']).reset_index()

    plt.figure(figsize=(12, 6))
    plt.plot(hourly_stats['hr'], hourly_stats['mean'], marker='o', linestyle='-', color='#3498db')
    plt.title('Average Bike Rentals by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Total Rentals')
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function 7: Rentals Across Seasons
def rentals_across_seasons():
    st.subheader("Average Bike Rentals Across Seasons")
    season_avg = all_df.groupby('season')['cnt'].mean().reset_index()
    season_avg['season_name'] = season_avg['season'].map(season_map)

    plt.figure(figsize=(10, 6))
    plt.plot(season_avg['season_name'], season_avg['cnt'], marker='o', linewidth=2, markersize=10)
    plt.title('Average Bike Rentals Across Seasons')
    plt.xlabel('Season')
    plt.ylabel('Average Total Rentals')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(bottom=0)
    st.pyplot(plt)

# Streamlit app layout
st.title("Bike Rental Analysis Dashboard")

# Sidebar for choosing visualizations
st.sidebar.header("Choose Visualization")
visualization = st.sidebar.selectbox(
    "Select a plot to display",
    ("Temperature vs Rentals", "Humidity vs Rentals", "Correlation Heatmap",
     "Weekdays vs Weekends", "Weekdays vs Weekends by Season", "Hourly Rentals", "Rentals Across Seasons")
)

# Mapping the selected option to the corresponding function
visualization_functions = {
    "Temperature vs Rentals": temperature_vs_rentals,
    "Humidity vs Rentals": humidity_vs_rentals,
    "Correlation Heatmap": correlation_heatmap,
    "Weekdays vs Weekends": weekdays_vs_weekends,
    "Weekdays vs Weekends by Season": weekdays_vs_weekends_by_season,
    "Hourly Rentals": hourly_rentals,
    "Rentals Across Seasons": rentals_across_seasons
}

# Call the appropriate function based on user selection
visualization_functions[visualization]()
