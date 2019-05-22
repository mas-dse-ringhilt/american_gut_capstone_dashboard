import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pickle
import json
import helper as h


app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
app.config['suppress_callback_exceptions']=True


#df = pd.read_csv('../data/clean_viz_project_data.csv')
df = pd.read_csv('../data/all_body_4.16.agp_only_meta.csv', low_memory=False)
drug_df = pd.read_csv('../data/2.21.drug_data_dense.csv')
alpha_df = pd.read_csv('../data/alpha_div_all_body_sites_clean.csv')

w2v_df = pd.read_csv('../data/w2vec_pca.csv')
hyper_df = pd.read_csv('../data/hyperbolic_bodysite_pca.csv')


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


EMBEDDDING_TYPES = sorted(['hyperbolic', 'word2vec'])

embedding_options = [{'label': metric,
                        'value': metric}
                       for metric in EMBEDDDING_TYPES]


def get_tab_one_div1():
    return html.Div(
        [
            html.Div(
                [
                    html.P('Select Embedding Type:', style={'margin-bottom': '1px'}),
                    dcc.Dropdown(
                        id='metric-dropdown-1',
                        options=embedding_options,
                        value=embedding_options[0]['value']
                    ),
                ],
                className='three columns'
            ),
            html.Div(
                [
                    html.Br(),
                    dcc.RadioItems(
                        id='scatter-radio',
                        options=[
                            {'label': '2d scatterplot', 'value': '2D'},
                            {'label': '3d scatterplot', 'value': '3D'},
    
                        ],
                        value='2D',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                className='three columns'
            )
        ],
        className='row', style={'margin-top': '15px'}
    )


def get_tab_one_div2():
    outer_profile_div = html.Div(get_profile_div(), id='outer-profile-div1')
    return html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='scatter3d-plot')
                ],
                className='eight columns',
                style={'margin-top': '5'}
            ),

            html.Div([
                    outer_profile_div
                ],
                className='three columns',
                style={'margin-top': '20', 'margin-left': '60', 'backgroundColor': 'rgb(240, 240, 240)', 'border': 'solid grey 1px'}
            ),
        ]
    )


def get_profile_div(sample_id=None):
    print(sample_id)
    if sample_id:
        adf = df[df.sample_id == sample_id]
        #print(adf.shape)
        bmi = adf.bmi_corrected.iloc[0]
        age = adf.age_corrected.iloc[0]
        country = adf.country.iloc[0]
        lat = adf.latitude.iloc[0]
        lon = adf.longitude.iloc[0]

        alpha_df1 = alpha_df[alpha_df.sample_id == sample_id]
        faith_pd = 'N/A'
        if len(alpha_df1 != 0):
            faith_pd = alpha_df1.faith_pd.iloc[0]

        adrug_df = drug_df[drug_df.sample_id == sample_id]
        anti = 'N/A'
        supp = 'N/A'
        med = 'N/A'
        if len(adrug_df != 0):
            anti_df = adrug_df[adrug_df.question_shortname == 'ANTIBIOTIC_MED']
            supp_df = adrug_df[adrug_df.question_shortname == 'SUPPLEMENTS']
            med_df = adrug_df[adrug_df.question_shortname == 'MEDICATION_LIST']
            if len(anti_df != 0):
                anti = anti_df.response.iloc[0]
            if len(supp_df != 0):
                supp = supp_df.response.iloc[0]
            if len(med_df != 0):
                med = med_df.response.iloc[0]


        return html.Div([
            html.P('Sample ID: {0}'.format(sample_id)),
            html.P('Faith PD Alpha Diversity: {:.2f}'.format(faith_pd)),
            html.P('BMI: {0}'.format(bmi)),
            html.P('Age: {0}'.format(age)),
            html.P('Country: {0}'.format(country)),
            html.P('Latitude: {0}'.format(lat)),
            html.P('Longitude: {0}'.format(lon)),
            html.P('Antibiotics: {0}'.format(anti)),
            html.P('Supplements: {0}'.format(supp)),
            html.P('Medications: {0}'.format(med)),
        ], id='profile-div', style={'margin-left': '5', 'height': '392px'})
    else:
        return html.Div([
            html.P('Sample ID:'),
            html.P('Faith PD Alpha Diversity: '),
            html.P('BMI: '),
            html.P('Age: '),
            html.P('Country: '),
            html.P('Latitude: '),
            html.P('Longitude: '),
            html.P('Antibiotics: '),
            html.P('Supplements: '),
            html.P('Medications: '),
        ], id='profile-div', style={'margin-left': '5', 'height': '392px'})


def get_help_tab():
    return html.Div(
        [
            html.Div(
                [
                    html.P('Help')
                ],
                className='six columns',
                style={'margin-top': '20'}
            ),
        ],
        className='row'
    )

app.layout = html.Div(
    [
        html.Div(
            [
                html.H3(
                    'The American Gut Project - Body Site Classification',
                    className='eight columns',
                ),
                html.Img(
                    src="http://humanfoodproject.com/wp-content/uploads/2012/06/AG_finallogo215.jpg",
                    className='one columns',
                    style={
                        'height': '50',
                        'width': '120',
                        'float': 'right',
                        'position': 'relative',
                    },
                ),
            ],
            className='row',
            style={'margin-bottom': '5px', 'borderBottom': 'thin lightgrey solid'}
        ),


        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='Body Site Classification', children=[
                get_tab_one_div1(),
                get_tab_one_div2(),
            ], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Help', children=[
                get_help_tab()
            ], style=tab_style, selected_style=tab_selected_style),

        ], style=tabs_styles),
    ],
    className='ten columns offset-by-one'
)


@app.callback(Output('outer-profile-div1', 'children'),
              [Input('metric-dropdown-1', 'value'),
               Input('scatter3d-plot', 'hoverData')])
def update_profile_div(metric, hoverData):
    #print('inside update profile div')
    #print(json.dumps(hoverData, indent=2))
    if hoverData:
        sample_id = json.dumps(hoverData['points'][0]['text'].split()[1])
        sample_id = int(sample_id.strip('"'))
        #print(sample_id)
        profile_div = get_profile_div(sample_id)
    else:
        profile_div = get_profile_div()
    return html.Div(profile_div)


@app.callback(
    dash.dependencies.Output('scatter3d-plot', 'figure'),
    [dash.dependencies.Input('metric-dropdown-1', 'value'),
     dash.dependencies.Input('scatter-radio', 'value')])
def update_scatter3d_plot(metric, scatter_type):
    print(scatter_type)
    print(metric)
    if scatter_type == '3D':
        print('scatter type is 3D')
        if metric == 'hyperbolic':
            fig = h.get_plot_3d(hyper_df, 'hyperbolic')
        else:
            fig = h.get_plot_3d(w2v_df, 'word2vec')
    else:
        if metric == 'hyperbolic':
            fig = h.get_plot_2d(hyper_df, 'hyperbolic')
        else:
            fig = h.get_plot_2d(w2v_df, 'word2vec')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)