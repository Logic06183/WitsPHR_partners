import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set the font to a serif font for scientific publication
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['grid.linewidth'] = 0.5

# Read the data
df = pd.read_excel('tshwane_temperatures.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Calculate monthly statistics
monthly_stats = df.groupby('Month')['Maximum Temperature (°C)'].agg([
    'mean', 'std', 'min', 'max'
]).reset_index()

# Create figure with specific dimensions for publication
fig, ax = plt.subplots(figsize=(8, 6))
plt.title('Maximum Temperature Patterns in Tshwane (2024-2025)', 
         fontsize=10, pad=20)

# Plot confidence intervals and range
ax.fill_between(monthly_stats['Month'], 
               monthly_stats['mean'] - monthly_stats['std'],
               monthly_stats['mean'] + monthly_stats['std'],
               alpha=0.2, color='gray', label='±1 SD')
ax.fill_between(monthly_stats['Month'],
               monthly_stats['min'],
               monthly_stats['max'],
               alpha=0.1, color='blue', label='Range')

# Plot mean line
ax.plot(monthly_stats['Month'], monthly_stats['mean'], 
        'k-', linewidth=1.5, label='Mean')

# Add seasonal bands
seasons = [
    ('Summer', (1, 2), '#FF9999'),
    ('Autumn', (3, 5), '#FFCC99'),
    ('Winter', (6, 8), '#99CCFF'),
    ('Spring', (9, 11), '#99FF99'),
    ('Summer', (12, 12), '#FF9999')
]

# Add subtle season indicators at the top
for season, (start, end), color in seasons:
    if start <= end:
        ax.axvspan(start, end + 0.5, ymin=0.95, ymax=1, 
                  color=color, alpha=0.3)
        mid_point = (start + end) / 2
        ax.text(mid_point, ax.get_ylim()[1]*1.02, season, 
                ha='center', va='bottom', fontsize=8)

# Customize the plot
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.set_xlabel('Month', fontsize=9)
ax.set_ylabel('Maximum Temperature (°C)', fontsize=9)
ax.grid(True, linestyle=':', alpha=0.3)
ax.legend(fontsize=8, frameon=False)

# Adjust layout and save
plt.tight_layout()
plt.savefig('scientific_seasonal_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Print statistical summary
print("\nMonthly Temperature Statistics (°C)")
print("=================================")
summary = monthly_stats.copy()
summary['Month'] = month_names
summary = summary.round(2)
summary.columns = ['Month', 'Mean', 'Std Dev', 'Min', 'Max']
print(summary.to_string(index=False))

# Calculate seasonal statistics
def get_season(month):
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'

df['Season'] = df['Month'].apply(get_season)
seasonal_stats = df.groupby('Season')['Maximum Temperature (°C)'].agg([
    'mean', 'std', 'min', 'max'
]).round(2)

print("\nSeasonal Statistics (°C)")
print("=======================")
print(seasonal_stats)
