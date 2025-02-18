import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as PathEffects
import numpy as np
from adjustText import adjust_text

# Partner data with coordinates
partners_data = {
    'Institution': [
        # South Africa
        'University of the Witwatersrand', 'University of Cape Town', 'Wits RHI',
        'IBM Research Africa', 'South African Medical Research Council',
        # East Africa
        'Aga Khan University', 'IBM Research Africa', 
        'Kenya Medical Research Institute',
        # West Africa
        'University Peleforo Gon Coulibaly', 
        'Centre for Sexual Health and HIV/AIDS Research',
        # Europe
        'Trinity College Dublin', 'Liverpool School of Tropical Medicine', 
        'Ghent University', 'University College London',
        'London School of Hygiene & Tropical Medicine',
        'WHO European Centre for Environment and Health',
        # Australia
        'Burnet Institute', 'Monash University',
        # North America
        'University of Michigan', 'University of Washington',
        'National Institute of Environmental Health Sciences',
        'Columbia University', 'Yale School of Public Health'
    ],
    'City': [
        # South Africa
        'Johannesburg', 'Cape Town', 'Johannesburg',
        'Johannesburg', 'Cape Town',
        # East Africa
        'Nairobi', 'Nairobi',
        'Nairobi',
        # West Africa
        'Korhogo',
        'Harare',
        # Europe
        'Dublin', 'Liverpool',
        'Ghent', 'London',
        'London',
        'Bonn',
        # Australia
        'Melbourne', 'Melbourne',
        # North America
        'Ann Arbor', 'Seattle',
        'Research Triangle Park',
        'New York', 'New Haven'
    ],
    'Country': [
        # South Africa
        'South Africa', 'South Africa', 'South Africa',
        'South Africa', 'South Africa',
        # East Africa
        'Kenya', 'Kenya',
        'Kenya',
        # West Africa
        "Côte d'Ivoire",
        'Zimbabwe',
        # Europe
        'Ireland', 'United Kingdom',
        'Belgium', 'United Kingdom',
        'United Kingdom',
        'Germany',
        # Australia
        'Australia', 'Australia',
        # North America
        'United States', 'United States',
        'United States',
        'United States', 'United States'
    ],
    'Type': [
        # South Africa
        'Academic', 'Academic', 'Research',
        'Industry', 'Research',
        # East Africa
        'Academic', 'Industry',
        'Research',
        # West Africa
        'Academic',
        'Research',
        # Europe
        'Academic', 'Academic',
        'Academic', 'Academic',
        'Academic',
        'Research',
        # Australia
        'Research', 'Academic',
        # North America
        'Academic', 'Academic',
        'Research',
        'Academic', 'Academic'
    ]
}

# Add coordinates
coordinates = {
    'Johannesburg': (-26.2041, 28.0473),
    'Cape Town': (-33.9249, 18.4241),
    'Nairobi': (-1.2921, 36.8219),
    'Korhogo': (9.4557, -5.6290),
    'Harare': (-17.8252, 31.0335),
    'Dublin': (53.3438, -6.2546),
    'Liverpool': (53.4084, -2.9916),
    'Ghent': (51.0543, 3.7174),
    'London': (51.5074, -0.1278),
    'Bonn': (50.7374, 7.0982),
    'Melbourne': (-37.8136, 144.9631),
    'Ann Arbor': (42.2808, -83.7430),
    'Seattle': (47.6062, -122.3321),
    'Research Triangle Park': (35.8992, -78.8637),
    'New York': (40.7128, -74.0060),
    'New Haven': (41.3083, -72.9279)
}

# Create latitude and longitude lists
partners_data['Latitude'] = [coordinates[city][0] for city in partners_data['City']]
partners_data['Longitude'] = [coordinates[city][1] for city in partners_data['City']]

# Create DataFrame
df = pd.DataFrame(partners_data)

# Color scheme for different institution types with improved colors
colors = {
    'Academic': '#2E86C1',  # Royal Blue
    'Research': '#28B463',  # Emerald Green
    'Industry': '#E74C3C'   # Bright Red
}

def create_base_map(projection=ccrs.Robinson()):
    fig = plt.figure(figsize=(20, 12), facecolor='white')
    ax = plt.axes(projection=projection)
    
    # Enhanced map features
    ax.add_feature(cfeature.LAND, facecolor='#F5F5F5', alpha=0.8)
    ax.add_feature(cfeature.OCEAN, facecolor='#E6F3F7', alpha=0.8)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#666666')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#999999')
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.2, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    return fig, ax

def plot_partners(ax, df, region=None):
    if region == 'Europe':
        extent = [-15, 15, 45, 60]
    elif region == 'South Africa':
        extent = [15, 35, -35, -20]
    else:
        extent = None
    
    if extent:
        ax.set_extent(extent, crs=ccrs.PlateCarree())
    
    texts = []
    
    for idx, row in df.iterrows():
        # Skip points outside the region if a region is specified
        if region:
            if region == 'Europe' and not (-15 <= row['Longitude'] <= 15 and 45 <= row['Latitude'] <= 60):
                continue
            if region == 'South Africa' and not (15 <= row['Longitude'] <= 35 and -35 <= row['Latitude'] <= -20):
                continue
        
        # Plot marker with white edge for better visibility
        ax.plot(row['Longitude'], row['Latitude'],
                marker='o',
                color=colors[row['Type']],
                markeredgecolor='white',
                markeredgewidth=1,
                markersize=12 if region else 10,
                transform=ccrs.PlateCarree(),
                zorder=5)
        
        # Calculate initial offset based on location
        base_offset = 5
        
        # Custom offsets for specific regions to prevent initial overlap
        if row['City'] in ['New York', 'New Haven']:
            offset_x = -base_offset * 1.5
            offset_y = base_offset if row['City'] == 'New York' else -base_offset
        elif row['City'] in ['Seattle', 'Ann Arbor']:
            offset_x = -base_offset
            offset_y = base_offset * 1.5 if row['City'] == 'Seattle' else -base_offset
        elif row['City'] == 'Research Triangle Park':
            offset_x = base_offset
            offset_y = -base_offset
        elif row['City'] in ['London', 'Liverpool', 'Dublin']:
            offset_x = -base_offset
            offset_y = base_offset * (1 + ['London', 'Liverpool', 'Dublin'].index(row['City']) * 0.5)
        elif row['City'] in ['Bonn', 'Ghent']:
            offset_x = base_offset
            offset_y = base_offset * (1 + ['Bonn', 'Ghent'].index(row['City']) * 0.5)
        else:
            # Default positioning based on hemisphere
            if row['Latitude'] > 0:
                offset_y = base_offset
            else:
                offset_y = -base_offset
                
            if row['Longitude'] > 0:
                offset_x = base_offset
            else:
                offset_x = -base_offset
        
        # Create background patch with clean style
        bbox_props = dict(
            facecolor='white',
            edgecolor=colors[row['Type']],
            boxstyle='round,pad=0.4',
            alpha=0.95,
            linewidth=0.8
        )
        
        # Calculate text position
        text_x = row['Longitude'] + offset_x
        text_y = row['Latitude'] + offset_y
        
        # Create institution text
        text = ax.text(text_x, text_y,
                row['Institution'],
                transform=ccrs.PlateCarree(),
                fontsize=8 if not region else 9,
                horizontalalignment='left' if offset_x > 0 else 'right',
                verticalalignment='center',
                bbox=bbox_props,
                zorder=6)
        
        # Add subtle glow effect
        text.set_path_effects([
            PathEffects.withStroke(linewidth=2, foreground='white', alpha=0.8),
            PathEffects.Normal()
        ])
        
        texts.append(text)
        
        # Add connecting line
        if not region:
            ax.plot([row['Longitude'], text_x],
                   [row['Latitude'], text_y],
                   color='gray',
                   linewidth=0.5,
                   alpha=0.3,
                   transform=ccrs.PlateCarree(),
                   zorder=4)
    
    # Use adjust_text to prevent overlap
    if not region:
        adjust_text(texts, 
                   expand_points=(2.0, 2.0),
                   force_points=(0.5, 1.0),
                   force_text=(0.5, 1.0),
                   arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.5),
                   avoid_self=True,
                   avoid_points=True)

# Create global map
fig, ax = create_base_map()
plot_partners(ax, df)
ax.set_global()

# Adjust figure size for better label spacing
plt.gcf().set_size_inches(24, 15)

# Add title with styling
title = plt.title('Wits Planetary Health Research Global Partners', 
                 pad=20, fontsize=16, fontweight='bold')
title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])

# Add legend with improved styling
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                             markerfacecolor=color, 
                             markeredgecolor='white',
                             markeredgewidth=1,
                             label=type_,
                             markersize=10)
                  for type_, color in colors.items()]
legend = ax.legend(handles=legend_elements, 
                  loc='lower left', 
                  title='Institution Type',
                  title_fontsize=10,
                  fontsize=9,
                  framealpha=0.9,
                  edgecolor='#666666')
legend.get_frame().set_facecolor('white')

plt.savefig('partner_map_global.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# Create Europe map
fig, ax = create_base_map(ccrs.Mercator())
plot_partners(ax, df, 'Europe')
title = plt.title('European Partners - Detailed View', 
                 pad=20, fontsize=16, fontweight='bold')
title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])
legend = ax.legend(handles=legend_elements, 
                  loc='lower left', 
                  title='Institution Type',
                  title_fontsize=10,
                  fontsize=9,
                  framealpha=0.9,
                  edgecolor='#666666')
legend.get_frame().set_facecolor('white')
plt.savefig('partner_map_europe.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# Create South Africa map
fig, ax = create_base_map(ccrs.Mercator())
plot_partners(ax, df, 'South Africa')
title = plt.title('South African Partners - Detailed View', 
                 pad=20, fontsize=16, fontweight='bold')
title.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])
legend = ax.legend(handles=legend_elements, 
                  loc='lower left', 
                  title='Institution Type',
                  title_fontsize=10,
                  fontsize=9,
                  framealpha=0.9,
                  edgecolor='#666666')
legend.get_frame().set_facecolor('white')
plt.savefig('partner_map_sa.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
