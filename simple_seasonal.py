import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_excel('tshwane_temperatures.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Calculate monthly averages
monthly_stats = df.groupby('Month')['Maximum Temperature (°C)'].agg(['mean', 'min', 'max']).reset_index()

# Create the plot
plt.figure(figsize=(12, 6))

# Plot the temperature range
plt.fill_between(monthly_stats['Month'], 
                monthly_stats['min'], 
                monthly_stats['max'],
                alpha=0.2,
                color='blue',
                label='Temperature Range')

# Plot the mean line
plt.plot(monthly_stats['Month'],
         monthly_stats['mean'],
         'r-',
         linewidth=2,
         label='Average Temperature')

# Customize the plot
plt.title('Tshwane Temperature Patterns (2024-2025)', pad=20)
plt.xlabel('Month')
plt.ylabel('Maximum Temperature (°C)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Set x-axis ticks to month names
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(1, 13), month_names)

# Add seasonal annotations
seasons = [
    ('Summer', (1, 2)),
    ('Autumn', (3, 5)),
    ('Winter', (6, 8)),
    ('Spring', (9, 11)),
    ('Summer', (12, 12))
]

# Print statistics
print("Seasonal Temperature Analysis")
print("============================")
for season, (start, end) in seasons:
    if start <= end:
        mask = df['Month'].between(start, end)
    else:
        mask = df['Month'].between(start, 12) | df['Month'].between(1, end)
    
    season_data = df[mask]['Maximum Temperature (°C)']
    print(f"\n{season}:")
    print(f"  Average: {season_data.mean():.1f}°C")
    print(f"  Maximum: {season_data.max():.1f}°C")
    print(f"  Minimum: {season_data.min():.1f}°C")

# Save the plot
plt.tight_layout()
plt.savefig('seasonal_pattern.png')
plt.close()
