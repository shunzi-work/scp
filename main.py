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














import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import random

def spiral_arc_patch(from_radius, to_radius, width, from_angle, to_angle, n_segments=20):
    """Create a PathPatch approximating a spiral arc segment."""
    # Outer arc (from from_angle to to_angle at radius + width)
    outer_arc = [
        ((from_radius + width) * np.sin(t), -(from_radius + width) * np.cos(t))
        for t in np.linspace(from_angle, to_angle, n_segments)
    ]

    # Inner arc (from to_angle back to from_angle at inner radius)
    inner_arc = [
        (from_radius * np.sin(t), -from_radius * np.cos(t))
        for t in np.linspace(to_angle, from_angle, n_segments)
    ]

    verts = []
    codes = []

    # Move to starting point of inner arc
    verts.append((from_radius * np.sin(from_angle), -from_radius * np.cos(from_angle)))
    codes.append(Path.MOVETO)

    # Line to outer arc start
    verts.append(outer_arc[0])
    codes.append(Path.LINETO)

    # Outer arc
    verts.extend(outer_arc[1:])
    codes.extend([Path.LINETO] * (n_segments - 1))

    # Line to inner arc end
    verts.append(inner_arc[0])
    codes.append(Path.LINETO)

    # Inner arc back
    verts.extend(inner_arc[1:])
    codes.extend([Path.LINETO] * (n_segments - 1))

    # Close
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)

    return PathPatch(Path(verts, codes), facecolor=random_color(), edgecolor='none')

def random_color():
    return (0, random.uniform(0.75, 1.0), 1.0)  # RGB tuple

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.axis('off')

# Spiral parameters
WIDTH = 10
BASE_RADIUS = 30
angle_step = 2 * np.pi / 30

# Track outermost radius to set axis limits
max_radius = 0

for index in range(100):
    from_angle = angle_step * index
    to_angle = angle_step * (index + 1)

    for level in range(5):
        from_radius = BASE_RADIUS + index * 2 + WIDTH * level
        to_radius = BASE_RADIUS + (index + 1) * 2 + WIDTH * level
        max_radius = max(max_radius, to_radius + WIDTH)

        patch = spiral_arc_patch(from_radius, to_radius, WIDTH, from_angle, to_angle)
        ax.add_patch(patch)

# Set visible area
ax.set_xlim(-max_radius, max_radius)
ax.set_ylim(-max_radius, max_radius)
plt.title("Spiral Heatmap (Python D3 Port)", fontsize=16)
plt.show()
