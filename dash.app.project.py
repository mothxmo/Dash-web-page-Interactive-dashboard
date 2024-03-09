import pandas as pd 
import dash
from dash import html, dcc 
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)
print('Data read into a pandas dataframe!')
year_list = list (df['Year'].unique())
# Assuming you have initialized your Dash app like this
app = dash.Dash(__name__)

# Sample list of years (replace it with your actual data)

# Define the layout of the web page
app.layout = html.Div(
    children=[
        # H1 header for the title of the dashboard
        html.H1('Automobile Sales Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
        
        # Div containing a Dropdown component for selecting report types
        html.Div([
            dcc.Dropdown(
                id='dropdown-statistics', 
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type'
            ),
        ]),

        # Div containing a Dropdown component for selecting the year
        html.Div([
            dcc.Dropdown(
                id='select-year', 
                options=[{'label': i, 'value': i} for i in year_list],
                placeholder='Select a year',
                disabled=False  # Initial value of the disabled property
            ),
        ]),

        # Placeholder for the chart output
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ]
)

# Callback to update the disabled property of the 'Select Year' dropdown
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

def update_input_container(selected_value):
    if selected_value =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(dropdown, selected_year):
    if dropdown == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title='Sales Fluctuation Over Recession Period'))

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        bar_graph_data = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(bar_graph_data, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type'))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Expenditure Share by Vehicle Type during Recessions'))

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_data = recession_data.groupby('Vehicle_Type')[['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemployment_data, x='Vehicle_Type', y='Automobile_Sales', title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
        html.Div(className='chart-item', children=[
            html.Div(children=[R_chart1]),
            html.Div(children=[R_chart2])]),
        html.Div(className='chart-item', children=[
            html.Div(children=[R_chart3]),
            html.Div(children=[R_chart4])])]

    elif dropdown == 'Yearly Statistics':
        yearly_data = df[df['Year'] == selected_year]

    # Plot 1: Yearly Automobile sales using line chart for the whole period.
        Y_chart1 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales', title='Yearly Automobile Sales'))

    # Plot 2: Total Monthly Automobile sales using line chart.
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

    # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type'))

    # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure'))

        return [
        html.Div(className='chart-item', children=[
            html.Div(children=[Y_chart1]),
            html.Div(children=[Y_chart2])]),
        html.Div(className='chart-item', children=[
            html.Div(children=[Y_chart3]),
            html.Div(children=[Y_chart4])])]



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
