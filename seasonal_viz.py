import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Read the data
df = pd.read_excel('tshwane_temperatures.xlsx')
df['Date'] = pd.to_datetime(df['Date'])

# Add month and season columns
df['Month'] = df['Date'].dt.strftime('%B')
df['MonthNum'] = df['Date'].dt.month
df['Season'] = pd.cut(df['Date'].dt.month, 
                     bins=[0, 2, 5, 8, 11, 12],
                     labels=['Summer', 'Autumn', 'Winter', 'Spring', 'Summer'])

# 1. Seasonal Box Plot
plt.figure(figsize=(15, 8))
sns.boxplot(x='Season', y='Maximum Temperature (°C)', data=df)
plt.title('Temperature Distribution by Season in Tshwane', fontsize=14)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Maximum Temperature (°C)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig('seasonal_boxplot.png', bbox_inches='tight')
plt.close()

# 2. Monthly Temperature Trends
plt.figure(figsize=(15, 8))
monthly_avg = df.groupby('MonthNum')['Maximum Temperature (°C)'].agg(['mean', 'min', 'max']).reset_index()
plt.fill_between(monthly_avg['MonthNum'], monthly_avg['min'], monthly_avg['max'], alpha=0.3, color='lightblue', label='Range')
plt.plot(monthly_avg['MonthNum'], monthly_avg['mean'], 'r-', linewidth=2, label='Mean')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.title('Monthly Temperature Patterns in Tshwane', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Maximum Temperature (°C)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('monthly_trends.png', bbox_inches='tight')
plt.close()

# 3. Time Series with Seasonal Highlight
plt.figure(figsize=(15, 8))
colors = {'Summer': 'red', 'Autumn': 'orange', 'Winter': 'blue', 'Spring': 'green'}
for season in df['Season'].unique():
    mask = df['Season'] == season
    plt.scatter(df[mask]['Date'], df[mask]['Maximum Temperature (°C)'], 
               c=colors[season], label=season, alpha=0.6)
plt.plot(df['Date'], df['Maximum Temperature (°C)'], color='gray', alpha=0.3)
plt.title('Temperature Time Series with Seasonal Patterns', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Maximum Temperature (°C)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.savefig('seasonal_timeseries.png', bbox_inches='tight')
plt.close()

# Print seasonal statistics
seasonal_stats = df.groupby('Season')['Maximum Temperature (°C)'].agg(['mean', 'std', 'min', 'max'])
print("\nSeasonal Temperature Statistics:")
print("================================")
for season in seasonal_stats.index:
    print(f"\n{season}:")
    print(f"  Average: {seasonal_stats.loc[season, 'mean']:.1f}°C")
    print(f"  Std Dev: {seasonal_stats.loc[season, 'std']:.1f}°C")
    print(f"  Range: {seasonal_stats.loc[season, 'min']:.1f}°C to {seasonal_stats.loc[season, 'max']:.1f}°C")
