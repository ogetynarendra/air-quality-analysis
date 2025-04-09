import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------
# 📥 Load the Dataset
# ---------------------------------------------
df = pd.read_csv('pollution_us_2000_2016.csv', encoding='ISO-8859-1')

# Show actual column names
print("Column names in dataset:")
print(df.columns)

# ---------------------------------------------
# 🧹 Data Cleaning
# ---------------------------------------------

# Convert 'Date Local' to datetime
df['Date Local'] = pd.to_datetime(df['Date Local'], errors='coerce')
df.dropna(subset=['Date Local'], inplace=True)

# Drop rows with no pollution data at all
df.dropna(subset=['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean'], how='all', inplace=True)

# Extract year and month
df['Year'] = df['Date Local'].dt.year
df['Month'] = df['Date Local'].dt.month

# ---------------------------------------------
# 📊 Data Analysis and Visualization
# ---------------------------------------------

# 1️⃣ National yearly average NO2 levels
yearly_no2 = df.groupby('Year')['NO2 Mean'].mean()
yearly_no2.plot(marker='o', title='Average NO2 Levels in the US (2000–2016)', color='darkblue')
plt.xlabel("Year")
plt.ylabel("NO2 Mean (ppb)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 2️⃣ Top 10 cities with highest average NO2
top_no2_cities = df.groupby('City')['NO2 Mean'].mean().sort_values(ascending=False).head(10)
top_no2_cities.plot(kind='barh', title='Top 10 Cities by NO2 Levels', color='crimson')
plt.xlabel("Average NO2 (ppb)")
plt.tight_layout()
plt.show()

# 3️⃣ Monthly average O3 by state (heatmap)
monthly_state_o3 = df.pivot_table(index='Month', columns='State', values='O3 Mean', aggfunc='mean')
plt.figure(figsize=(14, 6))
sns.heatmap(monthly_state_o3, cmap='YlGnBu')
plt.title('Monthly Average O3 Levels by State')
plt.tight_layout()
plt.show()

# 4️⃣ Distribution of CO values
plt.figure(figsize=(8, 5))
sns.histplot(df['CO Mean'].dropna(), bins=50, kde=True, color='green')
plt.title('Distribution of CO Levels')
plt.xlabel('CO Mean (ppm)')
plt.tight_layout()
plt.show()

# 5️⃣ Correlation heatmap of pollutants
pollution_cols = ['NO2 Mean', 'O3 Mean', 'SO2 Mean', 'CO Mean']
corr = df[pollution_cols].corr()

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Between Pollutants')
plt.tight_layout()
plt.show()

# ---------------------------------------------
# 📤 Export to Excel or CSV
# ---------------------------------------------

# Export a sample of the cleaned dataset to Excel (max ~100,000 rows)
df.sample(n=100000, random_state=42).to_excel("cleaned_pollution_us_data_sample.xlsx", index=False)

# Export the full cleaned dataset to CSV (no row limit)
df.to_csv("cleaned_pollution_us_data.csv", index=False)

# Export city-wise average pollutant levels to Excel
city_pollution = df.groupby('City')[pollution_cols].mean().sort_values(by='NO2 Mean', ascending=False)
city_pollution.to_excel("pollution_summary_by_city.xlsx")
