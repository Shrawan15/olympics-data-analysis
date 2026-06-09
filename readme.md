# 🏅 Olympic Games Analysis Dashboard

An interactive web application to analyze **120 years of Olympic Games history (1896-2016)** built using Python, Streamlit, and Plotly.

## 🔴 Live Demo

👉 [Click Here to View Live App](https://olympics-data-analysis-shrawan15.streamlit.app)

---

## 📌 About The Project

This project provides comprehensive analysis of the Olympic Games dataset containing **270,000+ athlete records** spanning **120 years of Olympic history**. The dashboard offers 9 interactive modules ranging from basic medal tallies to advanced country and athlete comparisons.

---

## 🚀 Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | 🏠 **Home Page** | Overview with quick stats and navigation guide |
| 2 | 🏅 **Medal Tally** | View medal counts filtered by year and country |
| 3 | 📈 **Overall Analysis** | Participation trends across 120 years |
| 4 | 🌍 **Country-wise Analysis** | Deep dive into any country's Olympic performance |
| 5 | 🏃 **Athlete-wise Analysis** | Age, height, weight, and gender distribution |
| 6 | ⚽ **Sport-wise Analysis** | Explore any specific sport in detail |
| 7 | 🗺️ **World Map** | Choropleth map showing global medal distribution |
| 8 | ⚔️ **Country Comparison** | Compare two countries side by side |
| 9 | 👥 **Athlete Comparison** | Compare two athletes head to head |

### ✨ Additional Features

- 📥 CSV Download option for every data table
- 🎨 Interactive Plotly visualizations
- 📊 Heatmaps, Choropleth maps, Line charts, Bar charts
- ⚡ Real-time filtering and analysis

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data manipulation and cleaning |
| **NumPy** | Numerical computations |
| **Streamlit** | Web application framework |
| **Plotly** | Interactive visualizations |
| **Matplotlib** | Static visualizations |
| **Seaborn** | Statistical heatmaps |
| **Scipy** | Statistical distributions |

---

## 📊 Dataset

- **Source:** [120 Years of Olympic History - Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
- **Records:** 270,000+ athlete entries
- **Time Period:** 1896 (Athens) to 2016 (Rio)
- **Files Used:**
  - `athlete_events.csv` - Main dataset with athlete information
  - `noc_regions.csv` - National Olympic Committee codes mapping

---

## 📁 Project Structure

```
olympics-analysis/
│
├── app.py                  # Main Streamlit application
├── preprocessor.py         # Data cleaning and preprocessing
├── helper.py               # Analysis and helper functions
├── athlete_events.csv      # Olympic athletes dataset
├── noc_regions.csv         # Country codes dataset
├── requirements.txt        # Required Python libraries
└── README.md              # Project documentation
```

---

## ⚙️ How to Run Locally

### Step 1: Clone the repository

```bash
git clone https://github.com/Shrawan15/olympics-data-analysis.git
cd olympics-data-analysis
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

For Windows:

```bash
.venv\Scripts\activate
```

For Mac/Linux:

```bash
source .venv/bin/activate
```

### Step 3: Install required libraries

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit app

```bash
streamlit run app.py
```

### Step 5: Open in browser

```
http://localhost:8501
```

---

## 📦 Requirements

```
streamlit
pandas
numpy
plotly
matplotlib
seaborn
scipy
```

---

## 🎯 Features Breakdown

### 🏅 Medal Tally
- Filter by Year (1896 - 2016)
- Filter by Country (200+ countries)
- View Gold, Silver, Bronze and Total medals
- Download data as CSV

### 📈 Overall Analysis
- Top statistics (Editions, Hosts, Sports, Events, Nations, Athletes)
- Participating Nations over the years
- Events over the years
- Athletes over the years
- Most successful athletes

### 🌍 Country-wise Analysis
- Medal tally over the years
- Sports excellence heatmap
- Top 10 athletes of selected country

### 🏃 Athlete-wise Analysis
- Age distribution of medalists
- Height vs Weight scatter plot
- Men vs Women participation trends

### ⚽ Sport-wise Analysis
- Top 10 countries in any sport
- Top 10 athletes in any sport
- Participation trends over years
- Gender distribution analysis
- Medal type distribution

### 🗺️ World Map
- Interactive choropleth map
- Filter by medal type (Total/Gold/Silver/Bronze)
- Top 20 countries leaderboard

### ⚔️ Country Comparison
- Compare overall stats of two countries
- Medal trend comparison over years
- Top sports comparison
- Top athletes comparison

### 👥 Athlete Comparison
- Compare two athletes side by side
- Medal count comparison
- Career span and Olympic participation
- Sport and event details

---

## 🔍 Key Insights From Analysis

- **USA** has won the most Olympic medals in history
- 🏊 **Athletics and Swimming** are the most medal-rich sports
- 👩 **Women participation** has increased dramatically over 120 years
- 🏠 Host countries tend to perform **better** in their home Olympics
- 🎯 Peak performance age for most Olympic athletes is **20-25 years**
- 🌍 Over **200 countries** have participated in the Olympics

---

## 🚀 Deployment

This application is deployed on **Streamlit Cloud** which provides free hosting for Streamlit applications.

---

