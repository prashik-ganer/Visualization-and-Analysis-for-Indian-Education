import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input,callback
import json
import geopandas as gpd
import plotly.express as px
import dash
from shapely.geometry import Point
from dash_extensions.javascript import assign
from dash import dcc
from shapely.geometry import shape, Point
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
with open('Indian_states.geojson', 'r') as file:
    dev_borders = json.load(file)
df = pd.read_csv('EnrollByMEd.csv')
df1 = pd.read_csv('enrollment.csv')
df1 = df1.sort_values(by="ENRBTOT", ascending=False).head(10)
df1 = df1.sort_values(by="ENRBTOT", ascending=True).head(10)
6
df2 = pd.read_csv('Facilities.csv')
# print(df)
# Define unique school types
school_types = df['School Type'].unique()
#********************************
state_name='Gujarat'
df3 = pd.read_csv("stream.csv")
df3=df3[df3['STATE']==state_name]
# print(df3)
df4 = pd.read_csv('StudentToTeacher.csv')
# Filter data for specific state and year
year = '2016-17'
df4 = df4[df4['STATENAME'] == state_name]
df5 = pd.read_csv('TeachersByQual.csv')
data1=df5[df5['State']==state_name]

# print(data1)
#********************************
data2=pd.read_csv("india-education-spending.csv")
data2["Year"]=pd.to_datetime(data2["Date"]).dt.year
school_types1 = ['1', '2', '3', '4', '5']    #6,7
get_name={
            '1': 'Primary',
            '2': 'Primary & Upper Primary',
            '3': 'Primary, Upper Primary & SEC/HSEC',
            '4': 'Upper Primary',
            '5': 'Upper Primary & SEC/HSEC'#,
            # '6': 'Primary, Upper Primary & SEC',
            # '7': 'Upper Primary & SEC'
        }
# Calculate maximum value across all school types for each qualification
max_values = []
for school_type in school_types1:
    qualifications = [f'TCHHS{school_type}', f'TCHGD{school_type}', f'TCHPG{school_type}', f'TCHMD{school_type}']
    max_values.append(data1[qualifications].values.max())
def create_bar_graph(title, x_data_boys, x_data_girls, y_data, color_boys, color_girls, show_yaxis_label=False,x_range=None):
    return dcc.Graph(
        figure={
            'data': [
                go.Bar(
                    x=x_data_boys,
                    y=y_data,
                    orientation='h',
                    marker=dict(color=color_boys),  # Set color of boys bars
                    name='Boys'
                ),
                go.Bar(
                    x=x_data_girls,
                    y=y_data,
                    orientation='h',
                    marker=dict(color=color_girls),  # Set color of girls bars
                    name='Girls'
                )
            ],
            'layout': go.Layout(
                title=title,
                xaxis=dict(title='Count', showgrid=False, range= x_range),  # Hide gridlines
                yaxis=dict(title='Stream' if show_yaxis_label else '', showgrid=False, showticklabels=show_yaxis_label),  # Hide gridlines and tick labels
                margin=dict(l=100, r=100, t=50, b=50),  # Adjust margins as needed
                barmode='stack'  # Stack bars on top of each other
            )
        }
    )
# Select specific columns
selected_columns = ['Primary Only_R', 'Primary with Upper Primary_R', 'Primary with upper Primary Sec/H.Sec_R', 
                    'Upper Primary Only_R', 'Upper Primary with Sec./H.Sec_R', 'Primary with upper Primary Sec_R', 
                    'Upper Primary with Sec._R']
# Calculate sum of values for each column
# Define custom colors for each bar
# custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
custom_colors = [
    '#CC0033',
    '#E40039',
    '#F2003F',
    '#FF0044',
    '#FF3355',
    '#FF6677',
    '#FF99AA'
]
heading_style = {'color': 'white', 'text-align': 'center', 'font-size': '5rem'}
button_style = {'display': 'inline-block', 'width': '24px', 'height': '24px', 'margin-left': '5px'}
graph_style = {'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '2%'}
graph_container_style = {'padding': '20px', 'text-align': 'center'}
box_container_style = {'text-align': 'right'}
# Define layout
def create_Page2_layout():
    dff = df4[(df4['YEAR'] == year)]
    selected_df = dff[selected_columns]
    sum_values = selected_df.sum()
    global state_name
    return html.Div([
        
        # First section
        html.Div([
            html.H1("{}".format(state_name), style=heading_style),
            html.Div(style=box_container_style, children=[
                html.A(html.Div(style={**button_style, 'background-color': 'red'}),href='/'),
                html.Div(style={**button_style, 'background-color': 'blue'}),
                html.Div(style={**button_style, 'background-color': 'green'}),
            ]),
        ], style={'background-color': 'black', 'padding': '20px'}),
        
        # Second section
        html.Div([
            # First row of graphs
            html.Div([
                html.Div([

                    html.Div([
                        html.H1("STREAM SELECTION PREFERENCE BY STUDENTS"),
                        dcc.RadioItems(
                            id='class-selector',
                            options=[
                                {'label': '11th Class', 'value': '11'},
                                {'label': '12th Class', 'value': '12'}
                            ],
                            value='11',  # Default value
                            labelStyle={'display': 'inline-block'}
                        ),
                        html.Div(id='graphs-container')
                    ])

                ]),     
            ], className='row', style=graph_container_style),
            # Second row of graphs
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id='bar-chart',
                                figure={
                                    'data': [
                                        go.Bar(
                                            x=sum_values.index,
                                            y=sum_values.values,
                                            marker_color=custom_colors  # Set color for each bar individually
                                        )
                                    ],
                                    'layout': go.Layout(
                                        title='Distribution of Student to Teacher Ratio by Category',
                                        xaxis={'title': 'Student to Teacher Ratio'},
                                        yaxis={'title': 'Type of school'},
                                        plot_bgcolor='#f5f5f5',  # Set plot background color
                                        barmode='group'  # Set mode for stacking bars
                                    )
                                }
                            ),
                        ], style={'display': 'inline-block', 'width': '50%'}),  # Place bar chart in a div with 50% width

                        html.Div([
                            dcc.Graph(id='line-chart')
                        ], style={'display': 'inline-block', 'width': '50%'})  # Place line chart in a div with 50% width
                        ])
                ]),
                
            ], className='row', style=graph_container_style),
            
            # Third of graphs
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='school-type-dropdown_1',
                        options=[
                            {'label': 'Primary', 'value': '1'},
                            {'label': 'Primary & Upper Primary', 'value': '2'},
                            {'label': 'Primary, Upper Primary & SEC/HSEC', 'value': '3'},
                            {'label': 'Upper Primary', 'value': '4'},
                            {'label': 'Upper Primary & SEC/HSEC', 'value': '5'}#,
                            # {'label': 'Primary, Upper Primary & SEC', 'value': '6'},
                            # {'label': 'Upper Primary & SEC', 'value': '7'}
                        ],
                        value='1',
                        style={'width': '60%',"text-align":"center"} 
                        # Default value
                    ),
                        # dcc.Graph(id='teacher-qualification-graph')
                        html.Div(
                            dcc.Graph(id='teacher-qualification-graph'),
                            style={'width': '90%'}  # Adjust the width here
                        )
],style={"text-align": "-webkit-center"}),
                
            ], className='row', style=graph_container_style),
        ]),
    ], style={'padding': '20px'})
# lay = create_Page2_layout()
#  Load data from CSV
df6 = pd.read_csv("Enrollment_P&G.csv")

# Get unique states from the dataset
states = df6['State'].unique()


data_new = {
    "State" : ["LAKSHADWEEP", "KERALA", "GOA", "KARNATAKA", "TAMIL NADU", "PONDICHERRY", "ANDHRA PRADESH", 
          "MAHARASHTRA", "DADRA & NAGAR HAVELI", "DAMAN & DIU", "GUJARAT", "CHHATTISGARH", 
          "ODISHA", "RAJASTHAN", "DELHI", "MADHYA PRADESH", "UTTAR PRADESH", "HARYANA", "PUNJAB", 
          "CHANDIGARH", "JAMMU & KASHMIR", "UTTARAKHAND", "JHARKHAND", "WEST BENGAL", "BIHAR", 
          "SIKKIM", "MEGHALAYA", "MIZORAM", "TRIPURA", "MANIPUR", "ASSAM", "NAGALAND", "ARUNACHAL PRADESH", 
          "A & N ISLANDS","HIMACHAL PRADESH"],
    "Literacy Rate (1961)": [27.15, 55.08, 35.41, 29.8, 36.39, 43.65, 21.19, 35.08,15.52, 16 ,31.47, 18.14, 21.66, 
                              18.12, 61.95, 21.41, 20.87, 20.23, 25.63, 60.96, 12.95, 18.05, 21.14, 34.46, 21.95, 
                              12.65, 26.92, 44.01, 20.24, 36.04, 32.95, 21.95, 7.13, 40.07,26],
    "Literacy Rate (1971)": [51.76, 69.75, 51.96, 36.83, 45.4, 53.38, 24.57, 45.77, 18.13, 20 ,36.95, 24.08, 26.18, 
                              22.57, 65.08, 27.27, 23.99, 25.71, 34.12, 70.43, 21.71, 33.26, 23.87, 38.86, 23.17, 
                              17.74, 29.49, 53.8, 30.98, 38.47, 33.94, 33.78, 11.29, 51.15,36.5],
    "Literacy Rate (1981)": [68.42, 78.85, 65.71, 46.21, 54.39, 65.14, 35.66, 57.24, 32.9, 30 ,44.92, 32.63, 33.62, 
                              30.11, 71.94, 38.63, 32.65, 37.13, 43.37, 74.8, 30.64, 46.06, 35.03, 48.65, 32.32, 
                              34.05, 42.05, 59.88, 50.1, 49.66, 42.62, 50.28, 25.55, 63.19,49.6],
    "Literacy Rate (1991)": [81.78, 89.81, 75.51, 56.04, 62.66, 74.74, 44.08, 64.87, 55.955, 56, 61.29, 42.91, 49.09, 
                              38.55, 75.29, 44.67, 40.71, 55.85, 58.51, 77.81, 45.69, 57.75, 41.39, 57.7, 37.49, 
                              56.94, 49.1, 82.26, 60.44, 59.89, 52.89, 61.65, 41.59, 73.02,60.5],
    "Literacy Rate (2001)": [86.66, 90.86, 82.01, 66.64, 73.45, 81.24, 60.47, 76.88, 67.905,68,69.14, 64.66, 63.08, 
                              60.41, 81.67, 63.74, 56.27, 67.91, 69.65, 81.94, 55.52, 71.62, 53.56, 68.64, 47, 
                              68.81, 62.56, 88.8, 73.19, 70.53, 63.25, 66.59, 54.34, 81.3,68.6],
    "Literacy Rate (2011)": [91.8, 94, 88.7, 75.4, 80.1, 85.8, 67, 82.3, 81.65,82, 78, 70.3, 72.9, 66.1, 86.2, 
                              69.3, 67.7, 75.6, 75.8, 86, 67.2, 78.8, 66.4, 76.3, 61.8, 81.4, 74.4, 91.3, 87.2, 
                              76.9, 72.2, 79.6, 65.4, 86.6,84]
}

df7 = pd.DataFrame(data_new)


# Load primary and secondary education data
# primary_df = pd.read_csv("education_data.csv")
secondary_df = pd.read_csv("education_data_sec.csv")

grade_8_9 = secondary_df[secondary_df['grade'].isin([8, 9])]

# Group by 'state' and 'grade' and sum the 'total', 'girls', and 'boys' columns for each state and grade
statewise_grade_total = grade_8_9.groupby(['State', 'grade'])['total'].sum().reset_index()
statewise_grade_girls = grade_8_9.groupby(['State', 'grade'])['girls'].sum().reset_index()
statewise_grade_boys = grade_8_9.groupby(['State', 'grade'])['boys'].sum().reset_index()

# Filter to include only 8th and 9th grades
grade_8_total = statewise_grade_total[statewise_grade_total['grade'] == 8]
grade_9_total = statewise_grade_total[statewise_grade_total['grade'] == 9]

state_totals = {}

for index, row in grade_8_total.iterrows():
    state = row['State']
    total_primary_students = row['total']
    total_primary_girls = statewise_grade_girls[(statewise_grade_girls['State'] == state) & (statewise_grade_girls['grade'] == 8)]['girls'].values[0]
    total_primary_boys = statewise_grade_boys[(statewise_grade_boys['State'] == state) & (statewise_grade_boys['grade'] == 8)]['boys'].values[0]

    state_totals[state] = {
        'total_primary_students': total_primary_students,
        'total_primary_girls': total_primary_girls,
        'total_primary_boys': total_primary_boys,
        'total_students_1_12': total_primary_students,
        'total_girls_1_12': total_primary_girls,
        'total_boys_1_12': total_primary_boys
    }

# Now add total secondary students for each state
for index, row in grade_9_total.iterrows():
    state = row['State']
    total_secondary_students = row['total']
    total_secondary_girls = statewise_grade_girls[(statewise_grade_girls['State'] == state) & (statewise_grade_girls['grade'] == 9)]['girls'].values[0]
    total_secondary_boys = statewise_grade_boys[(statewise_grade_boys['State'] == state) & (statewise_grade_boys['grade'] == 9)]['boys'].values[0]

    if state in state_totals:
        state_totals[state]['total_secondary_students'] = total_secondary_students
        state_totals[state]['total_secondary_girls'] = total_secondary_girls
        state_totals[state]['total_secondary_boys'] = total_secondary_boys

        state_totals[state]['total_students_1_12'] += total_secondary_students
        state_totals[state]['total_girls_1_12'] += total_secondary_girls
        state_totals[state]['total_boys_1_12'] += total_secondary_boys

        transition_rate = (total_secondary_students / state_totals[state]['total_primary_students']) * 100
        state_totals[state]['transition_rate'] = transition_rate

        transition_rate_girls = (total_secondary_girls / state_totals[state]['total_primary_girls']) * 100
        state_totals[state]['transition_rate_girls'] = transition_rate_girls

        transition_rate_boys = (total_secondary_boys / state_totals[state]['total_primary_boys']) * 100
        state_totals[state]['transition_rate_boys'] = transition_rate_boys


data2_new = {
    "State/UT": ["A & N ISLANDS", "ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR", "CHANDIGARH",
                "CHHATTISGARH", "DADRA & NAGAR HAVELI", "DAMAN & DIU", "DELHI", "GOA", "GUJARAT", "HARYANA",
                "HIMACHAL PRADESH", "JAMMU & KASHMIR", "JHARKHAND", "KARNATAKA", "KERALA", "LADAKH",
                "LAKSHADWEEP", "MADHYA PRADESH", "MAHARASHTRA", "MANIPUR", "MEGHALAYA", "MIZORAM",
                "NAGALAND", "ODISHA", "PONDICHERRY", "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU",
                "TELANGANA", "TRIPURA", "UTTAR PRADESH", "UTTARAKHAND", "WEST BENGAL"],
    "2018": [8, 2678, 37, 544, 840, 25, 760, 8, 10, 180, 57, 2232, 1038, 336, 293, 313, 3670, 1348, None, 0,
             2191, 4340, 92, 63, 32, 67, 1062, 76, 1063, 3156, 19, 2466, 1988, 52, 7078, 438, 1371],
    "2019": [8, 2750, 39, 558, 874, 25, 810, 8, 10, 179, 58, 2275, 1087, 344, 316, 323, 4047, 1417, 5, 0,
             2411, 4494, 102, 67, 35, 67, 1087, 79, 1079, 3380, 22, 2610, 2071, 53, 7788, 454, 1411],
    "2020": [9, 2601, 42, 595, 1035, 26, 870, 8, 11, 180, 61, 2267, 1083, 348, 348, 336, 4233, 1448, 3, 0,
             2610, 4532, 105, 75, 39, 68, 1206, 81, 1039, 3694, 23, 2667, 2062, 54, 8114, 477, 1446],
    "2021": [9, 2602, 44, 607, 1092, 26, 917, 8, 11, 188, 62, 2395, 1090, 349, 341, 366, 4430, 1463, 6, 0,
             2742, 4692, 108, 77, 40, 69, 1300, 82, 1044, 3934, 24, 2829, 2083, 54, 8375, 500, 1514]
}

df8 = pd.DataFrame(data2_new)

data_uppercase = {
    "A & N ISLANDS": {"Primary (1 to 5) Boys": 0.2, "Primary (1 to 5) Girls": 0.7, "Upper Primary (6-8) Boys": 0.9, "Upper Primary (6-8) Girls": 1.0, "Secondary (9-10) Boys": 6.0, "Secondary (9-10) Girls": 3.9},
    "ANDHRA PRADESH": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 1.7, "Upper Primary (6-8) Girls": 1.5, "Secondary (9-10) Boys": 17.5, "Secondary (9-10) Girls": 15.0},
    "ARUNACHAL PRADESH": {"Primary (1 to 5) Boys": 9.3, "Primary (1 to 5) Girls": 9.2, "Upper Primary (6-8) Boys": 4.8, "Upper Primary (6-8) Girls": 8.4, "Secondary (9-10) Boys": 11.2, "Secondary (9-10) Girls": 12.3},
    "ASSAM": {"Primary (1 to 5) Boys": 6.8, "Primary (1 to 5) Girls": 5.2, "Upper Primary (6-8) Boys": 10.1, "Upper Primary (6-8) Girls": 7.6, "Secondary (9-10) Boys": 19.8, "Secondary (9-10) Girls": 20.7},
    "BIHAR": {"Primary (1 to 5) Boys": 2.8, "Primary (1 to 5) Girls": 4.2, "Upper Primary (6-8) Boys": 4.0, "Upper Primary (6-8) Girls": 5.2, "Secondary (9-10) Boys": 19.5, "Secondary (9-10) Girls": 21.4},
    "CHANDIGARH": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 0.0, "Secondary (9-10) Girls": 0.0},
    "CHHATTISGARH": {"Primary (1 to 5) Boys": 1.0, "Primary (1 to 5) Girls": 0.6, "Upper Primary (6-8) Boys": 4.8, "Upper Primary (6-8) Girls": 3.3, "Secondary (9-10) Boys": 11.5, "Secondary (9-10) Girls": 8.1},
    "DADRA & NAGAR HAVELI": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 10.5, "Secondary (9-10) Girls": 8.4},
    "DAMAN & DIU": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 10.5, "Secondary (9-10) Girls": 8.4},
    "DELHI": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 5.9, "Secondary (9-10) Girls": 3.7},
    "GOA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 12.1, "Secondary (9-10) Girls": 5.5},
    "GUJARAT": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 4.2, "Upper Primary (6-8) Girls": 5.8, "Secondary (9-10) Boys": 19.4, "Secondary (9-10) Girls": 15.9},
    "HARYANA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.3, "Upper Primary (6-8) Girls": 0.2, "Secondary (9-10) Boys": 6.7, "Secondary (9-10) Girls": 4.9},
    "HIMACHAL PRADESH": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.6, "Upper Primary (6-8) Girls": 0.5, "Secondary (9-10) Boys": 2.0, "Secondary (9-10) Girls": 0.9},
    "JAMMU & KASHMIR": {"Primary (1 to 5) Boys": 3.9, "Primary (1 to 5) Girls": 4.1, "Upper Primary (6-8) Boys": 2.8, "Upper Primary (6-8) Girls": 3.2, "Secondary (9-10) Boys": 5.6, "Secondary (9-10) Girls": 6.3},
    "JHARKHAND": {"Primary (1 to 5) Boys": 2.4, "Primary (1 to 5) Girls": 1.1, "Upper Primary (6-8) Boys": 3.7, "Upper Primary (6-8) Girls": 4.0, "Secondary (9-10) Boys": 9.7, "Secondary (9-10) Girls": 8.9},
    "KARNATAKA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 1.1, "Upper Primary (6-8) Girls": 1.1, "Secondary (9-10) Boys": 16.2, "Secondary (9-10) Girls": 13.0},
    "KERALA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 6.9, "Secondary (9-10) Girls": 4.1},
    "LADAKH": {"Primary (1 to 5) Boys": 7.5, "Primary (1 to 5) Girls": 5.5, "Upper Primary (6-8) Boys": 2.2, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 4.0, "Secondary (9-10) Girls": 5.7},
    "LAKSHADWEEP": {"Primary (1 to 5) Boys": 0.5, "Primary (1 to 5) Girls": 0.4, "Upper Primary (6-8) Boys": 3.2, "Upper Primary (6-8) Girls": 1.9, "Secondary (9-10) Boys": 0.4, "Secondary (9-10) Girls": 0.0},
    "MADHYA PRADESH": {"Primary (1 to 5) Boys": 3.2, "Primary (1 to 5) Girls": 2.9, "Upper Primary (6-8) Boys": 8.6, "Upper Primary (6-8) Girls": 9.0, "Secondary (9-10) Boys": 10.6, "Secondary (9-10) Girls": 9.7},
    "MAHARASHTRA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 1.5, "Upper Primary (6-8) Girls": 1.6, "Secondary (9-10) Boys": 10.8, "Secondary (9-10) Girls": 10.6},
    "MANIPUR": {"Primary (1 to 5) Boys": 13.5, "Primary (1 to 5) Girls": 13.0, "Upper Primary (6-8) Boys": 6.0, "Upper Primary (6-8) Girls": 5.2, "Secondary (9-10) Boys": 1.4, "Secondary (9-10) Girls": 1.2},
    "MEGHALAYA": {"Primary (1 to 5) Boys": 11.1, "Primary (1 to 5) Girls": 8.6, "Upper Primary (6-8) Boys": 12.0, "Upper Primary (6-8) Girls": 9.4, "Secondary (9-10) Boys": 23.3, "Secondary (9-10) Girls": 20.4},
    "MIZORAM": {"Primary (1 to 5) Boys": 7.1, "Primary (1 to 5) Girls": 5.6, "Upper Primary (6-8) Boys": 3.8, "Upper Primary (6-8) Girls": 1.6, "Secondary (9-10) Boys": 13.1, "Secondary (9-10) Girls": 10.8},
    "NAGALAND": {"Primary (1 to 5) Boys": 5.6, "Primary (1 to 5) Girls": 4.5, "Upper Primary (6-8) Boys": 4.6, "Upper Primary (6-8) Girls": 3.4, "Secondary (9-10) Boys": 18.9, "Secondary (9-10) Girls": 16.2},
    "ODISHA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 8.0, "Upper Primary (6-8) Girls": 6.5, "Secondary (9-10) Boys": 29.2, "Secondary (9-10) Girls": 25.2},
    "PONDICHERRY": {"Primary (1 to 5) Boys": 3.7, "Primary (1 to 5) Girls": 3.6, "Upper Primary (6-8) Boys": 2.8, "Upper Primary (6-8) Girls": 2.1, "Secondary (9-10) Boys": 8.4, "Secondary (9-10) Girls": 4.1},
    "PUNJAB": {"Primary (1 to 5) Boys": 1.6, "Primary (1 to 5) Girls": 1.0, "Upper Primary (6-8) Boys": 8.7, "Upper Primary (6-8) Girls": 7.1, "Secondary (9-10) Boys": 18.3, "Secondary (9-10) Girls": 16.0},
    "RAJASTHAN": {"Primary (1 to 5) Boys": 3.8, "Primary (1 to 5) Girls": 3.3, "Upper Primary (6-8) Boys": 4.4, "Upper Primary (6-8) Girls": 4.2, "Secondary (9-10) Boys": 7.8, "Secondary (9-10) Girls": 7.5},
    "SIKKIM": {"Primary (1 to 5) Boys": 2.9, "Primary (1 to 5) Girls": 0.5, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 14.6, "Secondary (9-10) Girls": 9.5},
    "TAMIL NADU": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 0.0, "Upper Primary (6-8) Girls": 0.0, "Secondary (9-10) Boys": 6.3, "Secondary (9-10) Girls": 2.5},
    "TELANGANA": {"Primary (1 to 5) Boys": 0.0, "Primary (1 to 5) Girls": 0.0, "Upper Primary (6-8) Boys": 3.4, "Upper Primary (6-8) Girls": 2.9, "Secondary (9-10) Boys": 14.5, "Secondary (9-10) Girls": 12.9},
    "TRIPURA": {"Primary (1 to 5) Boys": 1.2, "Primary (1 to 5) Girls": 1.0, "Upper Primary (6-8) Boys": 4.8, "Upper Primary (6-8) Girls": 4.3, "Secondary (9-10) Boys": 8.5, "Secondary (9-10) Girls": 8.2},
    "UTTAR PRADESH": {"Primary (1 to 5) Boys": 2.4, "Primary (1 to 5) Girls": 3.0, "Upper Primary (6-8) Boys": 1.3, "Upper Primary (6-8) Girls": 4.7, "Secondary (9-10) Boys": 9.5, "Secondary (9-10) Girls": 10.0},
    "UTTARAKHAND": {"Primary (1 to 5) Boys": 1.0, "Primary (1 to 5) Girls": 0.5, "Upper Primary (6-8) Boys": 3.0, "Upper Primary (6-8) Girls": 2.4, "Secondary (9-10) Boys": 5.4, "Secondary (9-10) Girls": 4.6},
    "WEST BENGAL": {"Primary (1 to 5) Boys": 9.1, "Primary (1 to 5) Girls": 8.2, "Upper Primary (6-8) Boys": 10.9, "Upper Primary (6-8) Girls": 12.8, "Secondary (9-10) Boys": 18.4, "Secondary (9-10) Girls": 17.7},
}


# Define the state mapping dictionary
# state_mapping = {
# #     "Andaman and Nicobar Islands": "Andaman & Nicobar Islands",
#     "Dadra and Nagar Haveli & Daman and Diu": "Dadra and Nagar Haveli & Daman & Diu"
# }

# # Update state names in the data with dictionary keys
# for state_name, state_key in state_mapping.items():
#     data_uppercase[state_key] = data_uppercase.pop(state_name)

# Create DataFrame
df9 = pd.DataFrame(data_uppercase).transpose()
df10 = pd.read_csv('ProfessionallyTrained_new.csv')
Page3 = html.Div([


    # First section
        html.Div([
            html.H1("COMPARISON OF STATES", style=heading_style),
            html.Div(style=box_container_style, children=[
                html.A(html.Div(style={**button_style, 'background-color': 'red'}),href='/'),
                html.Div(style={**button_style, 'background-color': 'blue'}),
                html.Div(style={**button_style, 'background-color': 'green'}),
            ]),
        ], style={'background-color': 'black', 'padding': '20px'}),


    html.Div([
        dcc.Dropdown(
            id='state-dropdown1',
            options=[{'label': state, 'value': state} for state in states],
            value=states[2],  # Default value
            style={'display': 'inline-block', 'width': '45%', 'margin-right': '5px'}
        ),
        dcc.Dropdown(
            id='state-dropdown2',
            options=[{'label': state, 'value': state} for state in states],
            value=states[5],  # Default value
            style={'display': 'inline-block', 'width': '45%'}
        ),
    ]),
    dcc.RadioItems(
        id='column-radio',
        options=[
            {'label': 'Private School', 'value': 'ENRTOTP'},
            {'label': 'Government School', 'value': 'ENRTOTG'}
        ],
        value='ENRTOTP',  # Default value
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='grouped-bar-chart'),
    dcc.Graph(id="line-plot"),
    dcc.Graph(id='transition-rate-graph'),
    dcc.Graph(id='college-counts'),
    dcc.Graph(id='dropout-graph'),
    dcc.Dropdown(
            id='type-dropdown_new',
            options=[{'label': 'Government', 'value': 'G'}, {'label': 'Private', 'value': 'P'}],
            value='G',
            multi=False
        ),
    dcc.Graph(id='teacher-graph')
])
graph3= html.Div([
    html.H1('Education Spending and Annual Change Over Time'),
    html.Div([
        dcc.Graph(id='education-line-graph'),
        html.Div([
            html.Label('From Year:'),
            dcc.Dropdown(
                id='from-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in data2['Year'].unique()],
                value=data2['Year'].min(),
                clearable=False,
                style={'width': '100px', 'display': 'inline-block'}
            ),
            html.Label('To Year:'),
            dcc.Dropdown(
                id='to-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in data2['Year'].unique()],
                value=data2['Year'].max(),
                clearable=False,
                style={'width': '100px', 'display': 'inline-block'}
            ),
        ], style={'position': 'absolute', 'top': '10px', 'right': '10px', 'background-color': 'rgba(255, 255, 255, 0.5)', 'padding': '10px', 'border-radius': '5px'})
    ]),
    html.Div([
        dcc.Graph(id='annual-change-histogram'),
    ]),
    html.Div(style={'height': '50px'})  # Empty div for spacing
])
graph =   html.Div([

html.Div([
    html.Div([
        
        dcc.Dropdown(
            id='school-type-dropdown',
            options=[{'label': st, 'value': st} for st in school_types],
            value=school_types[0],  # Default value
            clearable=False,
            style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}
        ),
        dcc.RadioItems(
            id='medium-radio',
            options=[
                {'label': 'Hindi', 'value': 'Hindi'},
                {'label': 'English', 'value': 'English'}
            ],
            value='Hindi',  # Default value
            labelStyle={'display': 'inline-block','color':'white','fontSize':'200%'},
            style={'textAlign': 'center','width':'50%','margin':'auto','selector':'.dash-spreadsheet-container input','rule':'transform: scale(1.5)'},
        ),
    ], style={'textAlign': 'center','display':'flex', "margin-bottom":"7px"}),
    
    html.Div([
        dcc.Graph(
            id='school-count-graph',
            config={'displayModeBar': False},
            style={'height': '60vh', 'width': '40vw'}
        ),
        dcc.Graph(
            id='pie-chart',
            config={'displayModeBar': False},
            style={'height': '60vh', 'width': '40vw'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center', "background":"white"})
], style={"width":"90vw", "margin-top":"130px"})


], style={"display":"flex", "justify-content":"center"})
# Load CSV file into a pandas DataFrame
# Define colors for bars
boys_color = 'rgb(0, 0, 205)'  # Royal Blue
girls_color = 'rgba(255, 105, 180, 0.7)'  # Pink
graph1= html.Div([
    dcc.Graph(id='enrollment-pyramid',style={"height":"505px", "background":"white"})
],style={'left':'2%','height':'52%','width':'45%','flex':'50%','margin':'5%'})
# Read data from CSV
# Define custom color scale
# colors = ['rgb(26, 118, 255)', 'rgb(55, 83, 109)', 'rgb(190, 22, 144)', 'rgb(100, 200, 50)', 'rgb(255, 0, 0)', 
#           'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(255, 0, 255)', 'rgb(0, 255, 255)', 
#           'rgb(128, 0, 128)', 'rgb(128, 128, 0)', 'rgb(0, 128, 128)', 'rgb(128, 0, 0)', 'rgb(0, 128, 0)']

colors = [
    'rgb(0, 0, 139)',   # Dark Blue
    'rgb(16, 78, 139)', # Dark Slate Blue
    'rgb(0, 0, 205)',   # Medium Blue
    'rgb(65, 105, 225)',# Royal Blues
    'rgb(0, 191, 255)', # Deep Sky Blue
    'rgb(0, 206, 209)', # Dark Cyan
    'rgb(0, 255, 255)', # Cyan
    'rgb(255, 140, 0)', # Dark Orange
    'rgb(255, 165, 0)', # Orange
    'rgb(255, 218, 185)'# Peach
]


# Define layout of the app
graph2 = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in df2['YEAR'].unique()],
        value=df2['YEAR'].min(),  # Set default value to the minimum year
        clearable=False,
    ),
    dcc.RadioItems(
        id='facility-radio',
        options=[
            {'label': 'Total Electricity', 'value': 'Total_Elec'},
            {'label': 'Total Computers', 'value': 'Total_Comp'},
            {'label': 'Total Play Grounds', 'value': 'Total_PG'},
            {'label': 'Total Schools', 'value': 'Total_Schools'}
        ],
        value='Total_Elec',  # Set default value to 'Total Electricity'
        labelStyle={'display': 'inline-block','color':'white','fontSize':'15px'},
        inline=True
    ),
    dcc.Graph(id='radial-bar-chart', style={"background":"white"})
],style={'right':'2%','height':'35%','width':'40%','flex':'50%','margin':'5%'})
flexed_graphs=html.Div([graph1,graph2],style={'display':'flex' })
def point_in_polygon(point, polygon):
    """Check if a point is within a polygon"""
    from shapely.geometry import shape, Point
    polygon_shape = shape(polygon)
    # point = Point(point['coordinates'])
    return polygon_shape.contains(point)

def is_point_in(lat, lon, geojson=dev_borders):
    if not isinstance(geojson, dict) or 'features' not in geojson:
        raise ValueError("GeoJSON must be a dictionary with a 'features' key.")

    # Correct the order of lat and lon when creating the Point
    point = Point(lon, lat)  # Use (longitude, latitude)
    state_name=""
    # Create a GeoDataFrame from the GeoJSON features
    gdf = gpd.GeoDataFrame.from_features(geojson['features'])
    # Check if the point is within any of the geometries in the GeoDataFrame
    is_within = gdf.contains(point).any()
    if is_within:
        for feature in dev_borders['features']:
            polygon = feature['geometry']
            if point_in_polygon(point, polygon):
                state_name = feature['properties']['st_nm']
                # print(f"You clicked on {state_name}")
        # for i in range(36):
        #     gdf=gpd.GeoDataFrame(dev_borders['features'][i])
        #     if gdf.contains(point):
        #         state=print(dev_borders['features'][i]['properties']['st_nm'])
        #         break     
    return is_within,state_name
classes = [60,65,70,75,80,85,90,95]
colorscale = ['#6A040F','#9D0208','#D00000', '#FAA307','#FFBA08', '#D4D700', '#80B918', '#55A630']
# colorscale = ['#caf0f8','#90e0ef','#48cae4', '#00b4d8','#0096c7', '#0077b6', '#023e8a', '#03045e']

style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=20, position="bottomleft",style={'color':'white'})
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")
name="Literacy rate"
def get_info(feature=None):
    header = [html.H4("{}".format(name))]
    if not feature:
        return header + [html.P("Hover over a state")]
    return header + [html.B(feature["properties"]["st_nm"]), html.Br(),
                     "{} -  {:.3f} ".format(name,feature["properties"]["density"])] + [html.Div(id="result")]
def get_category(value):
    # global name
    header = [html.H4("{}".format(value))]
    return header
def get_state(feature=None):
    if not feature:
        return "Hover Over a State"
    return feature["properties"]["st_nm"]
def get_value(feature=None):
    if not feature:
        return "Hover Over a State"
    return "{:.3f} ".format(feature["properties"]["density"])
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10%", "left": "30px", "zIndex": "1000","color":"white"})
card = html.Div(className="hover-state",children=[dbc.Card(id="state_card",children=get_state(),className="mb-3")],style={'position':'absolute','top':'35%','right':'8%','zIndex':'1000','fillOpacity':'0.7','width':'40%','height':'10%','text-align': 'center'})
card1 = html.Div(className="hover-state",children=[dbc.Card(id="Category_Card",children=get_category("Literacy Rate"),className="mb-3")],style={'margin':'10px',"height": "50%", "width": "55%", "font-weight":"900"})
card2 = html.Div(className="hover-state",children=[dbc.Card(id="Value_card",children=get_value(),className="mb-3")],style={'margin':'10px',"height": "50%", "width": "55%", "font-weight":"900"})
Card=html.Div([card1,card2],style={'display':'flex','position':'absolute','top':'40%','right':'3%','zIndex':'1000','color':'blue','fillOpacity':'0.7','width':'40%','height':'50%','text-align': 'center','margin':'5%','justify-content': 'center'})
# card = html.Div(id="horizontal_card",children=[html.H1("State Name")],style={'position':'absolute','top':'5%','right':'5%','zIndex':'1000','color':'blue','background-color':'white','fillOpacity':'0.7','width':'20%'})
heading = html.Div([html.H1("INDIAN EDUCATION ANALYSIS"),html.Button('Compare',className="hover-state", id='State_Comp',style={"margin-top":"6%","height":"41px"})],style={'color':'white','position':'relative','left':'2%','font-size':'45px', "font-weight":"900",'text-align': 'center', "display":"flex", "justify-content":"space-evenly"})
# heading = html.Div([html.H1("Indian Education Analysis"),html.Button('Compare', id='State_Comp')],style={'display':'flex','color':'white','position':'relative','left':'40%','font-size':'20px','text-align': 'center'})
map_context = [
             dl.LayerGroup(id="layer"),
            dl.GeoJSON(
                data=dev_borders,  # Use the loaded GeoJSON data
                id="dev_layer",
                style=style_handle,
                hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),
                # Default style for the paths
                hoverStyle={"weight": 5, "color": "orange", "dashArray": ""},  # Style for hovered countries
            ),heading,colorbar,card,Card,
            # dl.LocateControl(
            #     locateOptions={'enableHighAccuracy': True, 'drawMarker': True, 'flyTo': True, 'showCompass': True}),
            # dl.EasyButton(icon="fa-globe", title="Map Switch", id="site_management_satellite_button"),
            dcc.RadioItems(id="radio_mirchi",options=[{'label':'Female Literacy Rate','value':'Female Literacy Rate'},{'label':'Male Literacy Rate','value':'Male Literacy Rate'},{'label':'Budget per capita','value':'Budget per capita'},{'label': 'Literacy Rate','value':'Literacy Rate'},{'label':'Transition Rate','value':'Transition Rate'}],className="radio-button" ,value='Literacy Rate',style={'position':'absolute','bottom':'10%','left': 0,'background-color':'#f0f0f0','height': '16%','width': '10%','font-size': '140%','margin-left':'1%'
})
        ]

new_center=[28,101]
app = dash.Dash(__name__,suppress_callback_exceptions=True)
literacy_rates = {"Andaman & Nicobar Island": 86.63,"Arunanchal Pradesh": 66.95,"Assam": 72.19,"Bihar": 61.80,"Chandigarh": 86.43,"Chhattisgarh": 71.04,"Dadara & Nagar Havelli": 77.65,"Daman & Diu":77.65,"Goa": 87.40,"Gujarat": 78.03,"Haryana": 76.64,
    "Himachal Pradesh": 83.78,"Jammu & Kashmir":67.16,"Jharkhand": 67.63,"Karnataka": 75.60,"Kerala": 94.00,"Lakshadweep": 91.85,
    "Madhya Pradesh": 70.63,"Maharashtra": 82.34,"Manipur": 79.85,"Meghalaya": 75.48,"Mizoram": 91.58,"Nagaland": 79.55,"Delhi": 86.21,
    "Puducherry": 86.55,"Punjab": 76.68,"Rajasthan": 66.11,"Sikkim": 81.42,"Tamil Nadu": 80.33,"Telangana": 66.50,"Tripura": 87.22,
    "Uttar Pradesh": 69.72,"Uttarakhand": 79.63,"West Bengal": 77.08,"Odisha": 72.87,"Andhra Pradesh": 67.0
}

Male_Literacy_Rate = {
    "Andaman & Nicobar Island": 90.11, "Andhra Pradesh": 75.56, "Arunanchal Pradesh": 73.69, "Assam": 78.81,
    "Bihar": 73.39, "Chandigarh": 90.54, "Chhattisgarh": 81.45, "Dadara & Nagar Havelli": 86.46,
    "Daman & Diu": 91.48, "Delhi": 91.03, "Goa": 92.81, "Gujarat": 87.23, "Haryana": 85.38, "Himachal Pradesh": 90.83,
    "Jammu & Kashmir": 78.26, "Jharkhand": 78.45, "Karnataka": 82.85, "Kerala": 96.02, "Lakshadweep": 96.11,
    "Madhya Pradesh": 80.53, "Maharashtra": 89.82, "Manipur": 86.49, "Meghalaya": 77.17, "Mizoram": 93.72,
    "Nagaland": 83.29, "Odisha": 82.4, "Puducherry": 92.12, "Punjab": 81.48, "Rajasthan": 80.51, "Sikkim": 87.29,
    "Tamil Nadu": 86.81, "Telangana": 74.95, "Tripura": 92.18, "Uttar Pradesh": 79.24, "Uttarakhand": 88.33,
    "West Bengal": 82.67
}

Female_Literacy_Rate = {
    "Andaman & Nicobar Island": 81.84, "Andhra Pradesh": 59.74, "Arunanchal Pradesh": 59.57, "Assam": 67.27,
    "Bihar": 53.33, "Chandigarh": 81.38, "Chhattisgarh": 60.59, "Dadara & Nagar Havelli": 65.93,
    "Daman & Diu": 79.59, "Delhi": 80.93, "Goa": 81.84, "Gujarat": 70.73, "Haryana": 66.77, "Himachal Pradesh": 76.6,
    "Jammu & Kashmir": 58.01, "Jharkhand": 56.21, "Karnataka": 68.13, "Kerala": 91.98, "Lakshadweep": 88.25,
    "Madhya Pradesh": 60.02, "Maharashtra": 75.48, "Manipur": 73.17, "Meghalaya": 73.78, "Mizoram": 89.4,
    "Nagaland": 76.69, "Odisha": 64.36, "Puducherry": 81.22, "Punjab": 71.34, "Rajasthan": 52.66, "Sikkim": 76.43,
    "Tamil Nadu": 73.86, "Telangana": 57.92, "Tripura": 83.15, "Uttar Pradesh": 59.26, "Uttarakhand": 70.7,
    "West Bengal": 71.16
}

Ratio = {'Andaman & Nicobar Island': 60.0, 'Andhra Pradesh': 73.64787300094889, 'Arunanchal Pradesh': 64.66927250399245, 
'Assam': 74.21009900438189, 'Bihar': 100.0, 'Chandigarh': 64.71537813549867, 'Chhattisgarh': 74.92901797698791, 
'Dadara & Nagar Havelli': 95.37952083846164, 'Daman & Diu': 74.86401827532343, 'Delhi': 70.55612034642884, 'Goa': 61.15998140901059, 
'Gujarat': 75.67769710679082, 'Haryana': 72.93996146328978, 'Himachal Pradesh': 65.27190462227168, 'Jammu & Kashmir': 66.18278472140587, 
'Jharkhand': 88.78162981776707, 'Karnataka': 76.12303924109813, 'Kerala': 69.06575876813936, 'Lakshadweep': 60.116880803967305, 
'Madhya Pradesh': 81.45485579341371, 'Maharashtra': 69.72360015109574, 'Manipur': 70.99963413815907, 'Meghalaya': 71.1422740066328, 
'Mizoram': 64.3376922378096, 'Nagaland': 71.91267884888266, 'Odisha': 79.62981189992598, 'Puducherry': 74.59037438160387, 
'Punjab': 77.98971681690328, 'Rajasthan': 78.02882135737099, 'Sikkim': 61.52741651158464, 'Tamil Nadu': 72.06762035851267, 
'Telangana': 77.98177277196672, 'Tripura': 69.63008891742487, 'Uttar Pradesh': 83.64400335563406, 'Uttarakhand': 68.13894743113346,
 'West Bengal': 81.16809965830025}
Transition_rates = {
    "Andaman & Nicobar Island": 98.36, "Andhra Pradesh": 95.92, "Arunanchal Pradesh": 98.04, "Assam": 93.15,
    "Bihar": 86.2, "Chandigarh": 98.6, "Chhattisgarh": 93.07, "Dadara & Nagar Havelli": 98.18, "Daman & Diu": 99.1,
    "Delhi": 99.5, "Goa": 97.8, "Gujarat": 97.81, "Haryana": 97.02, "Himachal Pradesh": 97.85, "Jammu & Kashmir": 93.25,
    "Jharkhand": 80.19, "Karnataka": 94.26, "Kerala": 0, "Lakshadweep": 97.01, "Madhya Pradesh": 87.43,
    "Maharashtra": 98.95, "Manipur": 87.7, "Meghalaya": 0, "Mizoram": 84.13, "Nagaland": 88, "Odisha": 88.76,
    "Puducherry": 0, "Punjab": 97.61, "Rajasthan": 88.67, "Sikkim": 94.89, "Tamil Nadu": 95.39, "Telangana": 95.92,
    "Tripura": 92.1, "Uttar Pradesh": 76.92, "Uttarakhand": 95.85, "West Bengal": 92.42
}
# print(len(literacy_rates))
app.layout = html.Div(id="Main_Div",children=[html.Div(children=[dl.Map(center=new_center,scrollWheelZoom=False,maxZoom=5,zoom=5,zoomSnap=0.25,zoomControl=False,children=map_context,id='map',style={'width': '100%', 'height': '100vh','background-color':'rgba(255,255,255,0)'}),graph,flexed_graphs],style={'background':"#23272E"})])
@app.callback(Output("Main_Div", "children"), [Input("map", "clickData"),Input("State_Comp","n_clicks")], prevent_initial_call=True)
def map_click(click_lat_lng,value):
    if value is not None:
        print("V")
        return Page3
    elif click_lat_lng is not None:
        print("M")
        coordinates = click_lat_lng['latlng']
        lat, lon = coordinates.values()
        point_in,st_nm=is_point_in(lat,lon,dev_borders)
        if point_in:
            global state_name 
            global df3
            global df4
            global df5
            global data1
            global max_values
            global school_types1
            state_name = st_nm
            df3 = pd.read_csv("stream.csv")
            df3=df3[df3['STATE']==state_name]
            # print(df3)
            df4 = pd.read_csv('StudentToTeacher.csv')
            # Filter data for specific state and year
            year = '2016-17'
            df4 = df4[df4['STATENAME'] == state_name]
            df5 = pd.read_csv('TeachersByQual.csv')
            data1=df5[df5['State']==state_name]
            for school_type in school_types1:
                qualifications = [f'TCHHS{school_type}', f'TCHGD{school_type}', f'TCHPG{school_type}', f'TCHMD{school_type}']
                max_values.append(data1[qualifications].values.max())
            return create_Page2_layout()
            # html.H1(state_name)
            # print("IGI I'm Going In")
            # Return a list of new elements to add to the 'layer' component
            # return dl.Marker(
            #         position=[lat, lon],
            #         children=dl.Tooltip("Chosen 🗺 Location: ({:.5f}, {:.5f})".format(lat, lon)),
            #         icon={'icon':'default',
            #               'iconRetinaUrl': 'assets/site_icon.png',
            #               'iconSize': [40, 40], 'iconAnchor': [12, 12], 'popupAnchor': [0, -12],
            #               'shadowUrl': None, 'shadowSize': None, 'shadowAnchor': None}
            #     )
        return dash.no_update
    else:print("click_lat_lang is None")

# @callback(Output("dev-layer","hoverStyle"),[Input("map","clickData")],prevent_intial_call=True)
# def map_hover(click_lat_lang):
#     if click_lat_lang is not None:
#         coordinates = click_lat_lang['latlng']
#         lat, lon = coordinates.values()
#         point_in,name=is_point_in(lat,lon,dev_borders)
#         if point_in:
#             return {"weight": 5, "color": "orange", "dashArray":""} #make the update dynamic to display state's name    
@app.callback(Output("Value_card","children"),Output("state_card","children"),Input("dev_layer", "hoverData"))
def info_hover(feature):
    return get_value(feature),get_state(feature)

# @callback(Output("result","children"),Input("radio_mirchi","value"))
# def radio_mirchi(value):
#     return value

@app.callback(Output("Category_Card","children"),Output("dev_layer","data"),
          Input("radio_mirchi","value"))
def radio_mirchi(value):
    print("radio_mirchi")
    global name
    if value == 'Literacy Rate':
        for i in range(36):
            dev_borders['features'][i]['properties']['density']=literacy_rates[dev_borders['features'][i]['properties']['st_nm']]
        name="Literacy Rate" #change the box to say Literacy rate
        # get_info()
    elif value == 'Transition Rate':
        for i in range(36):
            dev_borders['features'][i]['properties']['density']=Transition_rates[dev_borders['features'][i]['properties']['st_nm']]
        name="Transition Rate" #Change the box to say Transition Rate
        # info_hover()
    elif value == 'Budget per capita':
        for i in range(36):
            dev_borders['features'][i]['properties']['density']=Ratio[dev_borders['features'][i]['properties']['st_nm']]
        name="Budget Per Capita" #Change the box to say Transition Rate
    elif value == 'Male Literacy Rate':
        for i in range(36):
            dev_borders['features'][i]['properties']['density']=Male_Literacy_Rate[dev_borders['features'][i]['properties']['st_nm']]
        name="Male Literacy Rate" #Change the box to say Transition Rate
    elif value == 'Female Literacy Rate':
        for i in range(36):
            dev_borders['features'][i]['properties']['density']=Female_Literacy_Rate[dev_borders['features'][i]['properties']['st_nm']]
        name="Female Literacy Rate" #Change the box to say Transition Rate
    return get_category(value),dev_borders 
@app.callback(
    [Output('school-count-graph', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('school-type-dropdown', 'value'),
     Input('medium-radio', 'value'),
     Input('school-count-graph', 'clickData')]
)
def update_graph(selected_school_type, selected_medium, click_data):
    # Filter DataFrame based on selected school type
    filtered_df = df[df['School Type'] == selected_school_type]
    
    # Group by year and calculate sum of selected medium
    medium_df = filtered_df.groupby('Year')[selected_medium].sum().reset_index()
    
    # Create bar graph
    bar_fig = {
        # 'data': [{
        #     'x': medium_df['Year'],
        #     'y': medium_df[selected_medium],
        #     'type': 'bar',
        #     'marker': {'color': '#cc0033'}  # Set bar color
        # }],
        'data': [
            go.Bar(
                x=medium_df['Year'],
                y=medium_df[selected_medium],
                marker_color=custom_colors[1:]
            )],                   
        'layout': {
            'title': f'Number of {selected_medium} Medium Schools for {selected_school_type} Over Years',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': f'Number of {selected_medium} Medium Schools'},
            'plot_bgcolor': 'rgba(240, 240, 240, 1)',  # Set plot background color
            'paper_bgcolor': 'rgba(240, 240, 240, 1)',  # Set paper background color
            'bargap': 0.2,  # Set gap between bars
            'bargroupgap': 0.1,  # Set gap between groups of bars
            'barmode': 'overlay',  # Overlay bars to control width individually
            'width': 0.4  # Set width of each bar
        }
    }

    color_sequence = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # Create pie chart for selected year
    if click_data is not None:
        # print(click_data)
        selected_year = click_data['points'][0]['x']
    else:
        selected_year='2012-13'
    pie_df=df[df['Year']==selected_year]
    # print(pie_df)
    pie_counts = pie_df[selected_medium].tolist()
    pie_labels = pie_df['School Type'].tolist()
    pie_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_counts)])
    pie_fig.update_layout(title=f'School Type Distribution for {selected_medium} Medium in {selected_year}',plot_bgcolor='rgba(240, 240, 240, 0.7)',paper_bgcolor='rgba(240, 240, 240, 0.7)')
    pie_fig.update_traces(hole=0.6, marker=dict(colors=color_sequence))

    return bar_fig, pie_fig


# Define callback to update the graph
@app.callback(
    Output('enrollment-pyramid', 'figure'),
    [Input('enrollment-pyramid', 'id')]
)
def update_pyramid(_):
    # Create the pyramid plot
    data = [
        go.Bar(
            y=df1['State'],
            x=df1['ENRBTOT'],
            orientation='h',
            name='Boys Enrollment',
            marker=dict(color=boys_color),
            textposition='auto',
            width=0.8  # Increase width of bars
        ),
        go.Bar(
            y=df1['State'],
            x=-df1['ENRGTOT'],
            orientation='h',
            name='Girls Enrollment',
            marker=dict(color=girls_color),
            textposition='auto',
            width=0.8  # Increase width of bars
        )
    ]

    layout = go.Layout(
        barmode='relative',
        title='Enrollment by Gender and State',
        xaxis=dict(title='Enrollment', range=[-1.5 * max(df1['ENRGTOT']), 1.5 * max(df1['ENRBTOT'])]),
        yaxis=dict(title='State', autorange='reversed'),
        legend=dict(orientation='h', x=0.5, y=-0.1),
        plot_bgcolor='rgba(240, 240, 240, 0.7)',  # Set plot background color
        paper_bgcolor='rgba(240, 240, 240, 0.7)'  # Set paper background color
    )

    # layout['width'] = 800

    return {'data': data, 'layout': layout}


# Define callback to update radial bar chart
@app.callback(
    Output('radial-bar-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('facility-radio', 'value')]
)
def update_radial_chart(selected_year, selected_facility):
    # Filter data based on selected year and facility
    filtered_df = df2[(df2['YEAR'] == selected_year)]
    
    # Get top 15 states by selected facility
    top_15_states = filtered_df.groupby('STATNAME')[selected_facility].sum().nlargest(10)
    
    # Create radial bar chart
    fig = go.Figure()
    for state, value in top_15_states.items():
        # Modify color to make it slightly darker
        color = colors[top_15_states.index.get_loc(state) % len(colors)]
        color_dark = "rgb" + str(tuple([min(max(int(c * 0.8), 0), 255) for c in eval(color[3:])]))
        
        fig.add_trace(go.Barpolar(
            r=[value],
            theta=[state],
            marker_color=color_dark,  # Apply slightly darker color
            opacity=0.7,
            name='',
            hoverinfo='text',  # Show state name and value on hover
            hovertext=f'{state}: {value}',
            text=[state],
        ))
    
    fig.update_layout(
        title=f'Top 15 States by {selected_facility} in {selected_year}',
        font_size=16,
        polar=dict(
            bgcolor='white',
            radialaxis=dict(
                visible=True,
                showline=False,
                showticklabels=False,
                range=[0, top_15_states.max()]  # Adjust range as needed
            )),
        showlegend=False,  # Remove legend
        plot_bgcolor='rgba(240, 240, 240, 0.7)',  # Set plot background color
        paper_bgcolor='rgba(240, 240, 240, 0.7)'  # Set paper background color
    )
    
    return fig
@app.callback(
    Output('graphs-container', 'children'),
    [Input('class-selector', 'value')]
)
def update_graphs(selected_class):
    graphs = []
    max_11 = max([(df3['arts_c11_b'] + df3['arts_c11_g']).max(),(df3['com_c11_b'] + df3['com_c11_g']).max(),(df3['sci_c11_b'] + df3['sci_c11_g']).max()])
    max_12 = max([(df3['arts_c12_b'] + df3['arts_c12_g']).max(),(df3['com_c12_b'] + df3['com_c12_g']).max(),(df3['sci_c12_b'] + df3['sci_c12_g']).max()])
    if(selected_class=='11'):
        graphs.append(html.Div(create_bar_graph('Arts Stream', df3['arts_c11_b'] , df3['arts_c11_g'] , df3['YEAR'], '#8B0000', '#FF6347', show_yaxis_label=True, x_range=[0,max_11]), style={'width': '33%', 'display': 'inline-block'})),
        graphs.append(html.Div(create_bar_graph('Commerce Stream', df3['com_c11_b'] , df3['com_c11_g'] , df3['YEAR'], '#0000FF', '#87CEEB', x_range=[0,max_11]), style={'width': '33%', 'display': 'inline-block'})),
        graphs.append(html.Div(create_bar_graph('Science Stream', df3['sci_c11_b'] , df3['sci_c11_g'] , df3['YEAR'], '#008000', '#90EE90', x_range=[0,max_11]), style={'width': '33%', 'display': 'inline-block'}))
    if(selected_class=='12'):
        graphs.append(html.Div(create_bar_graph('Arts Stream', df3['arts_c12_b'] , df3['arts_c12_g'] , df3['YEAR'], '#8B0000', '#FF6347', show_yaxis_label=True, x_range=[0,max_12]), style={'width': '33%', 'display': 'inline-block'})),
        graphs.append(html.Div(create_bar_graph('Commerce Stream', df3['com_c12_b'] , df3['com_c12_g'] , df3['YEAR'], '#0000FF', '#87CEEB', x_range=[0,max_12]), style={'width': '33%', 'display': 'inline-block'})),
        graphs.append(html.Div(create_bar_graph('Science Stream', df3['sci_c12_b'] , df3['sci_c12_g'] , df3['YEAR'], '#008000', '#90EE90', x_range=[0,max_12]), style={'width': '33%', 'display': 'inline-block'}))
    return graphs

# *********************************************** From Graph 1 end   **************************************************************


# *********************************************** From Graph 2 start   **************************************************************

# Define callback to update line chart based on bar chart click
@app.callback(
    Output('line-chart', 'figure'),
    [Input('bar-chart', 'clickData')]
)
def update_line_chart(clickData):
    if clickData is None:
        school_data_teachers = df4['Total_T']
        school_data_enrollments = df4['Total_E']
        school_type = 'All_Schools'
    else:
        school_type = clickData['points'][0]['x']
        school_type_teachers = school_type.replace('_R', '_T')
        school_type_enrollments = school_type.replace('_R', '_E')
        # Filter data for selected school type
        school_data_teachers = df4[school_type_teachers]
        school_data_enrollments = df4[school_type_enrollments]
    # Create line chart
    line_chart = go.Figure()
    # Add trace for teachers
    line_chart.add_trace(go.Scatter(x=df4['YEAR'], y=school_data_teachers, mode='lines+markers', name='Teachers',
                                     yaxis='y1'))  # Assigning to yaxis='y1' for the first y-axis
    # Add trace for enrollments
    line_chart.add_trace(go.Scatter(x=df4['YEAR'], y=school_data_enrollments, mode='lines+markers', name='Enrollments',
                                     yaxis='y2'))  # Assigning to yaxis='y2' for the second y-axis

    line_chart.update_layout(title=f'Number of Teachers and Enrollments Over the Years for {school_type}',
                             xaxis_title='Year',
                             yaxis=dict(title='Number of Teachers', side='left'),  # Define properties for y-axis 1
                             yaxis2=dict(title='Number of Enrollments', side='right', overlaying='y'))  # Define properties for y-axis 2

    return line_chart

qualification_colors = {
    'TCHHS': 'red',
    'TCHGD': 'orange',
    'TCHPG': 'green',
    'TCHMD': 'green'
}
legend_names = {
    'TCHHS': 'Higher Sec.',
    'TCHGD': 'Grad.',
    'TCHPG': 'PG',
    'TCHMD': 'MD'
}
# Define callback to update the graph based on dropdown selection
@app.callback(
    Output('teacher-qualification-graph', 'figure'),
    [Input('school-type-dropdown_1', 'value')]
)
def update_graph(selected_school_type):
    hs_qualifications = [f'TCHHS{selected_school_type}', f'TCHGD{selected_school_type}',f'TCHPG{selected_school_type}', f'TCHMD{selected_school_type}']
    # print(hs_qualifications)
    hs_qualifications = sorted(hs_qualifications, key=lambda q: data1[q].iloc[0])[::-1]
    traces = []

    for qualification in hs_qualifications:
        trace = go.Scatter(
            # x=data1['Year'],
            x=['2011','2012','2013','2014','2015','2016'],
            y=data1[qualification],
            mode='lines+markers',
            fill='tozeroy',  # Fill area below the line
            name=legend_names[qualification[:-1]],
            line=dict(color=qualification_colors[qualification[:-1]])
        )
        traces.append(trace)
    max_value = max(max_values)
    layout = go.Layout(
        title=f'Teachers Qualification for {get_name[selected_school_type]}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Number of Teachers',range=[0, max_value + 10])
    )

    return {'data': traces, 'layout': layout}
@app.callback(
    [Output('education-line-graph', 'figure'),
     Output('annual-change-histogram', 'figure')],
    [Input('from-year-dropdown', 'value'),
     Input('to-year-dropdown', 'value')]
)
def update_graphs(from_year, to_year):
    filtered_data = data2[(data2['Year'] >= from_year) & (data2['Year'] <= to_year)]
    
    education_spending_graph = {
        'data2': [
            go.Scatter(
                x=filtered_data['Date'],
                y=filtered_data[' Education Spending (% of GDP)'],
                name='Education Spending (%)',
                mode='lines',
                marker_color='blue',
                opacity=0.7
            )
        ],
        'layout': go.Layout(
            title='Education Spending Over Time',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Education Spending (%)'},
            height=300
        )
    }
    
    annual_change_graph = {
        'data2': [
            go.Bar(
                x=filtered_data['Date'],
                y=filtered_data[' Annual Change'],
                name='Annual Change',
                marker_color='red',
                opacity=0.7
            )
        ],
        'layout': go.Layout(
            title='Annual Change Over Time',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Annual Change'},
            height=300,
            margin=dict(t=50),
            barmode='overlay'
        )
    }
    
    return education_spending_graph, annual_change_graph

@app.callback(
    Output('grouped-bar-chart', 'figure'),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value'),
     Input('column-radio', 'value')]
)
def update_grouped_bar_chart(state1, state2, column_name):
    # Filter data for the selected states
    df_filtered = df6[(df6['State'] == state1) | (df6['State'] == state2)]
    
    # Group data by year and state, summing up the column values
    grouped_data = df_filtered.groupby(['Year', 'State'])[column_name].sum().reset_index()
    
    # Create traces for each state
    traces = []
    for i, state in enumerate([state1, state2]):
        if i == 0:
            color = '#C21E17'  # Red color for the first bar
        else:
            color = '#E8635C'  # Lighter shade of red for the second bar
        trace = go.Bar(
            x=grouped_data[grouped_data['State'] == state]['Year'],
            y=grouped_data[grouped_data['State'] == state][column_name],
            name=state,
            marker=dict(color=color)
        )
        traces.append(trace)

    layout = go.Layout(
        barmode='group',
        title='Enrollment by Year for {} and {}'.format(state1, state2),
        xaxis=dict(title='Year'),
        yaxis=dict(title='Total Enrollment ({})'.format(column_name))
    )

    return {'data': traces, 'layout': layout}


@app.callback(
    Output("line-plot", "figure"),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value')]
)
def update_line_plot(state1, state2):
    trace1 = go.Scatter(
        x=df7.columns[1:],
        y=df7[df7["State"] == state1].values[0][1:],
        mode="lines+markers",
        name=state1
    )
    trace2 = go.Scatter(
        x=df7.columns[1:],
        y=df7[df7["State"] == state2].values[0][1:],
        mode="lines+markers",
        name=state2
    )
    return {
        "data": [trace1, trace2],
        "layout": go.Layout(
            title="Literacy Rate Over Time",
            xaxis={"title": "Year"},
            yaxis={"title": "Literacy Rate (%)"},
            legend={"x": 0, "y": 1},
            hovermode="closest"
        )
    }

@app.callback(
    Output('transition-rate-graph', 'figure'),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value')]
)
def update_graph(state1, state2):
    trace_state1 = go.Bar(
        x=['Total Students', 'Girls', 'Boys'],
        y=[state_totals[state1]['transition_rate'], state_totals[state1]['transition_rate_girls'], state_totals[state1]['transition_rate_boys']],
        name=state1
    )
    trace_state2 = go.Bar(
        x=['Total Students', 'Girls', 'Boys'],
        y=[state_totals[state2]['transition_rate'], state_totals[state2]['transition_rate_girls'], state_totals[state2]['transition_rate_boys']],
        name=state2
    )

    return {
        'data': [trace_state1, trace_state2], 
        'layout': go.Layout(title='Transition Rate Comparison',  
                            barmode='group')
    }


@app.callback(
    dash.dependencies.Output('college-counts', 'figure'),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value')]
)
def update_graph(state1, state2):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df8.columns[1:], y=df8[df8['State/UT'] == state1].values.tolist()[0][1:],
                         name=state1))
    fig.add_trace(go.Bar(x=df8.columns[1:], y=df8[df8['State/UT'] == state2].values.tolist()[0][1:],
                         name=state2))
    fig.update_layout(barmode='stack',
                      title='College Count Comparison',
                      xaxis_title='Year',
                      yaxis_title='College Count')
    return fig

@app.callback(
    Output('dropout-graph', 'figure'),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value')]
)
def update_graph(state1, state2):
    trace1 = go.Bar(
        x=df9.columns,
        y=df9.loc[state1],
        name=state1,
        width=0.4 

    )
    trace2 = go.Bar(
        x=df9.columns,
        y=df9.loc[state2],
        name=state2,
        width=0.4 
    )

    return {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title='Average Annual Dropout Rate by Level of Education and Gender',
                barmode='group'
            )
        }

@app.callback(
    Output('teacher-graph', 'figure'),
    [Input('state-dropdown1', 'value'),
     Input('state-dropdown2', 'value'),
     Input('type-dropdown_new', 'value')]
)
def update_graph(state1,state2,selected_type):
        traces = []
        trace_male1 = go.Scatter(
            x=df10[df10['State'] == state1]['Year'],
            y=df10[df10['State'] == state1][f'PTM{selected_type}'],  # Selecting PTMG or PTMP based on selected type
            mode='lines+markers',
            name=f'{state1} - Male'
        )
        trace_male2 = go.Scatter(
            x=df10[df10['State'] == state2]['Year'],
            y=df10[df10['State'] == state2][f'PTM{selected_type}'],  # Selecting PTMG or PTMP based on selected type
            mode='lines+markers',
            name=f'{state2} - Male'
        )
        trace_female1 = go.Scatter(
            x=df10[df10['State'] == state1]['Year'],
            y=df10[df10['State'] == state1][f'PTF{selected_type}'],  # Selecting PTFG or PTFP based on selected type
            mode='lines+markers',
            name=f'{state1} - Female'
        )
        trace_female2 = go.Scatter(
            x=df10[df10['State'] == state2]['Year'],
            y=df10[df10['State'] == state2][f'PTF{selected_type}'],  # Selecting PTFG or PTFP based on selected type
            mode='lines+markers',
            name=f'{state2} - Female'
        )
        traces.append(trace_male1)
        traces.append(trace_female1)
        traces.append(trace_male2)
        traces.append(trace_female2)
    
        layout = go.Layout(
            title=f'Professionally Trained Teacher Data - {"Government" if selected_type == "G" else "Private"} Teachers',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Number of Teachers')
        )
    
        return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True,port=8052)