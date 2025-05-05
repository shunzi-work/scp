import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime, timedelta

# Generate daily data from Jan 2022 to May 2025
start_date = datetime(2022, 1, 1)
end_date = datetime(2025, 5, 1)
dates = pd.date_range(start=start_date, end=end_date)
n_days = len(dates)

# Create dummy values (replace with actual data)
values = np.random.rand(n_days)
data = pd.DataFrame({'date': dates, 'value': values})
data['weekday'] = data['date'].dt.weekday  # Monday=0
data['week'] = data['date'].dt.isocalendar().week
data['year'] = data['date'].dt.year

# Normalize values for color mapping
data['norm'] = (data['value'] - data['value'].min()) / (data['value'].max() - data['value'].min())

# Spiral parameters
n_weeks = int(n_days / 7)
theta = np.linspace(0, 2 * np.pi * (n_weeks), n_days)  # One loop per 52 weeks
radius_start = 1
r = radius_start + (data['date'] - start_date).dt.days / 365.0  # grow slowly
spiral_thickness = 1

# Set up polar plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
ax.set_axis_off()

# Color mapping
colors = cm.YlGnBu(data['norm'])

# Plot each rectangle
for i in range(n_days):
    day_of_week = data['weekday'].iloc[i]
    week_number = int((data['date'].iloc[i] - start_date).days // 7)
    
    theta_val = 2 * np.pi * (week_number / 52)  # One loop = one year
    bar_width = 2 * np.pi / 52  # 52 weeks in circle
    dr = spiral_thickness / 7   # width per day in radius

    # Bar radius: based on spiral + offset for weekday
    r_base = radius_start + 0.2 * (week_number)
    dr = spiral_thickness + 0.013 * (week_number) / 7   # width per day in radius
    bar_bottom = r_base + dr * day_of_week

    ax.bar(theta_val, dr, width=bar_width, bottom=bar_bottom, color=colors[i], edgecolor='none')

plt.title("Spiral Calendar Heatmap (7-day width)", va='bottom')
plt.tight_layout()
plt.show()
