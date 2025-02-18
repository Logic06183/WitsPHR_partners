import pandas as pd

# Read the existing Excel file
df = pd.read_excel('tshwane_temperatures.xlsx')

# Convert date column to datetime and format it
df['date'] = pd.to_datetime(df['date'])
df['Date'] = df['date'].dt.strftime('%d %B %Y')

# Drop the original date column and rename temperature column
df = df[['Date', 'tmax']]
df.columns = ['Date', 'Maximum Temperature (°C)']

# Save back to Excel
df.to_excel('tshwane_temperatures.xlsx', index=False)
