import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Partner data with coordinates and project affiliations
partners_data = {
    'Institution': [
        # CHAMNHA Project Partners
        'Aga Khan University', 'Institut de Recherche en Sciences de la Santé',
        'London School of Hygiene and Tropical Medicine', 'University of Washington',
        'University of Oslo', 'Karolinska University', 'South African Medical Research Council',
        
        # HE2AT Center Partners
        'CeSHHAR', 'University of Cape Town', 'University Peleforo Gon Coulibaly',
        'IBM Research Africa (Johannesburg)', 'IBM Research Africa (Nairobi)',
        'University of Michigan', 'University of Washington',
        
        # HIGH Horizons Partners
        'World Health Organization', 'Lunds University', 'Karolinska University',
        'Azienda Sanitaria Locale Roma', 'Denmark Technical University',
        'University of Graz',
        
        # ENBEL Project Partners
        'University of Botswana', 'Umea University', 'Tartu Ulikool',
        'Folkehelseinstituttet', 'Center for International Climate Research',
        'Royal College of Surgeons in Ireland', 'Health and Environment Alliance',
        'International Red Cross Red Crescent Centre', 'University Paul Sabatier Toulouse',
        'Goeteborgs University', 'Ilmatieteen Laitos'
    ],
    'City': [
        # CHAMNHA
        'Nairobi', 'Ouagadougou', 'London', 'Seattle', 'Oslo', 'Stockholm', 'Cape Town',
        
        # HE2AT
        'Harare', 'Cape Town', 'Korhogo', 'Johannesburg', 'Nairobi', 'Ann Arbor', 'Seattle',
        
        # HIGH
        'Geneva', 'Lund', 'Stockholm', 'Rome', 'Copenhagen', 'Graz',
        
        # ENBEL
        'Gaborone', 'Umea', 'Tartu', 'Oslo', 'Oslo', 'Dublin', 'Brussels',
        'The Hague', 'Toulouse', 'Gothenburg', 'Helsinki'
    ],
    'Country': [
        # CHAMNHA
        'Kenya', 'Burkina Faso', 'United Kingdom', 'United States', 'Norway', 'Sweden', 'South Africa',
        
        # HE2AT
        'Zimbabwe', 'South Africa', "Côte d'Ivoire", 'South Africa', 'Kenya', 'United States', 'United States',
        
        # HIGH
        'Switzerland', 'Sweden', 'Sweden', 'Italy', 'Denmark', 'Austria',
        
        # ENBEL
        'Botswana', 'Sweden', 'Estonia', 'Norway', 'Norway', 'Ireland', 'Belgium',
        'Netherlands', 'France', 'Sweden', 'Finland'
    ],
    'Projects': [
        # CHAMNHA
        ['CHAMNHA'], ['CHAMNHA'], ['CHAMNHA'], ['CHAMNHA', 'HE2AT'], 
        ['CHAMNHA'], ['CHAMNHA'], ['CHAMNHA'],
        
        # HE2AT
        ['HE2AT'], ['HE2AT'], ['HE2AT'], ['HE2AT'], ['HE2AT'],
        ['HE2AT'], ['CHAMNHA', 'HE2AT'],
        
        # HIGH
        ['HIGH'], ['HIGH'], ['CHAMNHA', 'HIGH'], ['HIGH', 'ENBEL'],
        ['HIGH'], ['HIGH', 'ENBEL'],
        
        # ENBEL
        ['ENBEL'], ['ENBEL'], ['ENBEL'], ['ENBEL'], ['ENBEL'],
        ['ENBEL'], ['ENBEL'], ['ENBEL'], ['ENBEL'], ['ENBEL'], ['ENBEL']
    ]
}

# Add coordinates
coordinates = {
    'Nairobi': (-1.2921, 36.8219),
    'Ouagadougou': (12.3714, -1.5197),
    'London': (51.5074, -0.1278),
    'Seattle': (47.6062, -122.3321),
    'Oslo': (59.9139, 10.7522),
    'Stockholm': (59.3293, 18.0686),
    'Cape Town': (-33.9249, 18.4241),
    'Harare': (-17.8252, 31.0335),
    'Korhogo': (9.4557, -5.6290),
    'Johannesburg': (-26.2041, 28.0473),
    'Ann Arbor': (42.2808, -83.7430),
    'Geneva': (46.2044, 6.1432),
    'Lund': (55.7047, 13.1910),
    'Rome': (41.9028, 12.4964),
    'Copenhagen': (55.6761, 12.5683),
    'Graz': (47.0707, 15.4395),
    'Gaborone': (-24.6282, 25.9231),
    'Umea': (63.8258, 20.2630),
    'Tartu': (58.3780, 26.7290),
    'Dublin': (53.3498, -6.2603),
    'Brussels': (50.8503, 4.3517),
    'The Hague': (52.0705, 4.3007),
    'Toulouse': (43.6047, 1.4442),
    'Gothenburg': (57.7089, 11.9746),
    'Helsinki': (60.1699, 24.9384)
}

# Create latitude and longitude lists
partners_data['Latitude'] = [coordinates[city][0] for city in partners_data['City']]
partners_data['Longitude'] = [coordinates[city][1] for city in partners_data['City']]

# Convert to DataFrame
df = pd.DataFrame(partners_data)

# Create the interactive map
def create_interactive_map():
    # Create figure
    fig = go.Figure()
    
    # Color scheme for different projects
    colors = {
        'CHAMNHA': '#1f77b4',  # Blue
        'HE2AT': '#2ca02c',    # Green
        'HIGH': '#ff7f0e',     # Orange
        'ENBEL': '#d62728'     # Red
    }
    
    # Add base map
    fig.add_trace(go.Scattergeo(
        lon=[],
        lat=[],
        mode='markers',
        name='Base Map',
        showlegend=False
    ))
    
    # Add traces for each project
    for project in colors.keys():
        # Get partners for this project
        project_partners = df[df['Projects'].apply(lambda x: project in x)]
        
        # Add markers
        fig.add_trace(go.Scattergeo(
            lon=project_partners['Longitude'],
            lat=project_partners['Latitude'],
            text=project_partners.apply(
                lambda row: f"<b>{row['Institution']}</b><br>" +
                          f"{row['City']}, {row['Country']}<br>" +
                          f"Projects: {', '.join(row['Projects'])}",
                axis=1
            ),
            name=project,
            mode='markers+text',
            marker=dict(
                size=10,
                color=colors[project],
                line=dict(width=1, color='white')
            ),
            textposition='top center',
            textfont=dict(size=10, color='black'),
            hoverinfo='text',
            visible=True
        ))
        
        # Add connections to Wits (Johannesburg)
        fig.add_trace(go.Scattergeo(
            lon=[28.0473, 28.0473] + project_partners['Longitude'].tolist(),
            lat=[-26.2041, -26.2041] + project_partners['Latitude'].tolist(),
            mode='lines',
            line=dict(
                width=1,
                color=colors[project],
                dash='solid'
            ),
            name=f'{project} Connections',
            hoverinfo='skip',
            showlegend=False,
            visible=True
        ))
    
    # Update layout
    fig.update_layout(
        title='Wits Planetary Health Research Global Partners',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        geo=dict(
            projection_type='equirectangular',
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.5,
            landcolor='rgb(243, 243, 243)',
            oceancolor='rgb(204, 229, 255)',
            bgcolor='rgb(255, 255, 255)',
            showframe=False,
            showcoastlines=True,
            coastlinecolor='rgb(128, 128, 128)',
            countrycolor='rgb(204, 204, 204)'
        ),
        updatemenus=[
            # Dropdown for project visibility
            dict(
                buttons=[
                    dict(
                        args=[{'visible': [True] * (len(colors) * 2 + 1)}],
                        label='All Projects',
                        method='restyle'
                    )
                ] + [
                    dict(
                        args=[{'visible': [i == j or i == j + len(colors) or i == 0 
                                         for i in range(len(colors) * 2 + 1)]}],
                        label=project,
                        method='restyle'
                    ) for j, project in enumerate(colors.keys())
                ],
                direction='down',
                showactive=True,
                x=0.1,
                y=1.1,
                xanchor='left',
                yanchor='top'
            )
        ]
    )
    
    return fig

# Create and save the map
fig = create_interactive_map()
fig.write_html('interactive_partner_map.html')
