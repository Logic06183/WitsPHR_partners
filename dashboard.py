from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

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
    'Region': [
        # CHAMNHA
        'Africa', 'Africa', 'Europe', 'North America', 'Europe', 'Europe', 'Africa',
        
        # HE2AT
        'Africa', 'Africa', 'Africa', 'Africa', 'Africa', 'North America', 'North America',
        
        # HIGH
        'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
        
        # ENBEL
        'Africa', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
        'Europe', 'Europe', 'Europe', 'Europe'
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
    ],
    'Latitude': [
        -1.2921, 12.3714, 51.5074, 47.6062, 59.9139, 59.3293, -33.9249,
        -17.8252, 9.4557, -26.2041, -1.2921, 42.2808, 47.6062,
        46.2044, 55.7047, 59.3293, 41.9028, 55.6761, 47.0707,
        -24.6282, 63.8258, 58.3780, 59.9139, 59.9139, 53.3498, 50.8503,
        52.0705, 43.6047, 57.7089, 60.1699
    ],
    'Longitude': [
        36.8219, -1.5197, -0.1278, -122.3321, 10.7522, 18.0686, 18.4241,
        31.0335, -5.6290, 28.0473, 36.8219, -83.7430, -122.3321,
        6.1432, 13.1910, 18.0686, 12.4964, 12.5683, 15.4395,
        25.9231, 20.2630, 26.7290, 10.7522, 10.7522, -6.2603, 4.3517,
        4.3007, 1.4442, 11.9746, 24.9384
    ]
}

# Convert to DataFrame
df = pd.DataFrame(partners_data)

# Color scheme for different projects
colors = {
    'CHAMNHA': '#1f77b4',  # Blue
    'HE2AT': '#2ca02c',    # Green
    'HIGH': '#ff7f0e',     # Orange
    'ENBEL': '#d62728'     # Red
}

# Initialize the Dash app
app = Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1('Wits Planetary Health Research Global Partners',
            style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dcc.Graph(id='map-graph'),
    
    html.Div([
        html.Label('Select Projects:'),
        dcc.Checklist(
            id='project-filter',
            options=[{'label': p, 'value': p} for p in colors.keys()],
            value=['CHAMNHA'],
            inline=True
        )
    ])
])

@app.callback(
    Output('map-graph', 'figure'),
    Input('project-filter', 'value')
)
def update_map(selected_projects):
    # Filter data based on selected projects
    mask = df['Projects'].apply(lambda x: any(p in x for p in selected_projects))
    filtered_df = df[mask]
    
    # Create the map
    fig = px.scatter_geo(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        hover_name='Institution',
        hover_data=['City', 'Country', 'Projects'],
        color='Projects',
        color_discrete_map={str(['CHAMNHA']): colors['CHAMNHA'],
                          str(['HE2AT']): colors['HE2AT'],
                          str(['HIGH']): colors['HIGH'],
                          str(['ENBEL']): colors['ENBEL']},
        title='Global Research Partners',
        height=600
    )
    
    # Update the layout
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="LightGray",
        showocean=True,
        oceancolor="LightBlue",
        projection_type="equirectangular",
        showframe=False,
        showcountries=True,
        countrycolor="Gray",
        showlakes=True,
        lakecolor="LightBlue"
    )
    
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
