import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# Read the data
df = pd.read_excel('tshwane_temperatures.xlsx')
df['Date'] = pd.to_datetime(df['Date'])

# Basic statistics
print("Temperature Statistics:")
print(f"Mean temperature: {df['Maximum Temperature (°C)'].mean():.1f}°C")
print(f"Standard deviation: {df['Maximum Temperature (°C)'].std():.1f}°C")
print(f"Minimum: {df['Maximum Temperature (°C)'].min():.1f}°C")
print(f"Maximum: {df['Maximum Temperature (°C)'].max():.1f}°C")

# Check for outliers (temperatures outside 3 standard deviations)
mean_temp = df['Maximum Temperature (°C)'].mean()
std_temp = df['Maximum Temperature (°C)'].std()
outliers = df[abs(df['Maximum Temperature (°C)'] - mean_temp) > 3*std_temp]

if not outliers.empty:
    print("\nPotential outliers detected:")
    print(outliers)

# Monthly statistics
df['Month'] = df['Date'].dt.strftime('%B %Y')
monthly_stats = df.groupby('Month')['Maximum Temperature (°C)'].agg(['mean', 'min', 'max'])
print("\nMonthly Statistics:")
print(monthly_stats)

# Create a time series plot
plt.figure(figsize=(15, 8))
plt.plot(df['Date'], df['Maximum Temperature (°C)'])
plt.title('Maximum Daily Temperatures in Tshwane')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temperature_trend.png')

# Create a box plot by month
plt.figure(figsize=(15, 8))
df['Month'] = df['Date'].dt.strftime('%B')
sns.boxplot(x='Month', y='Maximum Temperature (°C)', data=df)
plt.title('Temperature Distribution by Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temperature_distribution.png')

# Check for sudden jumps in temperature
df['Temp_Change'] = df['Maximum Temperature (°C)'].diff()
large_changes = df[abs(df['Temp_Change']) > 10]  # Changes greater than 10°C
if not large_changes.empty:
    print("\nLarge temperature changes (>10°C between consecutive days):")
    print(large_changes[['Date', 'Maximum Temperature (°C)', 'Temp_Change']])

# Seasonal pattern check
df['Season'] = pd.cut(df['Date'].dt.month, 
                     bins=[0, 2, 5, 8, 11, 12],
                     labels=['Summer', 'Autumn', 'Winter', 'Spring', 'Summer'])
seasonal_stats = df.groupby('Season')['Maximum Temperature (°C)'].agg(['mean', 'min', 'max'])
print("\nSeasonal Statistics:")
print(seasonal_stats)

# Check data completeness
date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max())
missing_dates = date_range.difference(df['Date'])
if len(missing_dates) > 0:
    print(f"\nMissing dates: {len(missing_dates)} days")
    print("First few missing dates:")
    print(missing_dates[:5])
