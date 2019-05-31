import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pickle
import json
import helper as h

from dash_sunburst import Sunburst


app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
app.config['suppress_callback_exceptions']=True


#df = pd.read_csv('../data/clean_viz_project_data.csv')
df = pd.read_csv('../data/all_body_4.16.agp_only_meta.csv', low_memory=False)
drug_df = pd.read_csv('../data/2.21.drug_data_dense.csv')
alpha_df = pd.read_csv('../data/alpha_div_all_body_sites_clean.csv')

basic_df = pd.read_csv('../data/5.30.pca.data/5_30_basic_pca.csv')
w2v_df = pd.read_csv('../data/5.30.pca.data/5_30_w2vec_pca.csv')
hyper_df = pd.read_csv('../data/5.30.pca.data/5_30_hyper_pca.csv')
pcoa_df = pd.read_csv('../data/5.30.pca.data/5_30_beta_pcoa_3000sample.csv')


embed_dic = {
    'no_embedding': basic_df, 
    'pcoa': pcoa_df,
    'hyperbolic': hyper_df, 
    'word2vec': w2v_df
}


tax_df = pd.read_csv('../data/sampleid_to_tax.csv')
tax_df = tax_df.dropna(how='any', axis=0)
# cast sample id as int
tax_df['sample_id'] = tax_df['sample_id'].apply(lambda x: int(x))


sample_id_options = [{'label': sample_id,
                        'value': sample_id}
                       for sample_id in sorted(tax_df.sample_id.unique())]


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


EMBEDDDING_TYPES = ['no_embedding', 'pcoa', 'hyperbolic', 'word2vec']

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
            ),
            html.Div(
                [
                    html.P('Select Sample ID:', style={'margin-bottom': '1px'}),
                    dcc.Dropdown(
                        id='sample-dropdown',
                        options=sample_id_options,
                        #value=''
                    ),
                ],
                className='two columns'
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
                className='six columns',
                style={'margin-top': '5px'}
            ),
            html.Div(
                [
                    Sunburst(id='sunburst', data=h.get_blah_data())
                ],
                className='six columns',
                style={'margin-top': '0px'}
            ),
            html.Div([
                    outer_profile_div
                ],
                className='five columns',
                style={'margin-top': '20px', 'margin-left': '50px', 'margin-bottom': '20px', 'backgroundColor': 'rgb(240, 240, 240)', 'border': 'solid grey 1px'}
            ),
        ]
    )


def get_profile_div(sample_id=None):
    print(sample_id)
    if sample_id:
        adf = df[df.sample_id == sample_id]
        #print(adf.shape)
        body_site = adf.env_material.iloc[0]
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
            html.P('Body Site: {0}'.format(body_site)),
            html.P('Faith PD Alpha Diversity: {:.2f}'.format(faith_pd)),
            html.P('BMI: {0}'.format(bmi)),
            html.P('Age: {0}'.format(age)),
            html.P('Country: {0}'.format(country)),
            html.P('Lat, Lon: {0}, {1}'.format(lat, lon)),
            html.P('Antibiotics: {0}'.format(anti)),
            html.P('Supplements: {0}'.format(supp)),
            html.P('Medications: {0}'.format(med)),
        ], id='profile-div', style={'margin-left': '5px', 'height': '392px'})
    else:
        return html.Div([
            html.P('Sample ID:'),
            html.P('Body Site:'),
            html.P('Faith PD Alpha Diversity: '),
            html.P('BMI: '),
            html.P('Age: '),
            html.P('Country: '),
            html.P('Lat, Lon: '),
            html.P('Antibiotics: '),
            html.P('Supplements: '),
            html.P('Medications: '),
        ], id='profile-div', style={'margin-left': '5px', 'height': '392px'})


def get_help_tab():
    return html.Div(
        [
            html.Div(
                [
                    html.P('Help')
                ],
                className='six columns',
                style={'margin-top': '20px'}
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
              [Input('sample-dropdown', 'value')])
def update_profile_div(sample_id):
    if sample_id:
        print('sample_id')
        profile_div = get_profile_div(sample_id)
    else:
        profile_div = get_profile_div()
    return html.Div(profile_div)


@app.callback(
    dash.dependencies.Output('scatter3d-plot', 'figure'),
    [dash.dependencies.Input('metric-dropdown-1', 'value'),
     dash.dependencies.Input('sample-dropdown', 'value'),
     dash.dependencies.Input('scatter-radio', 'value')])
def update_scatter3d_plot(metric, sample_id, scatter_type):
    print(scatter_type)
    print(metric)
    embed_df = embed_dic[metric]
    if scatter_type == '3D':
        fig = h.get_plot_3d(embed_df, metric, sample_id)
    else:
        fig = h.get_plot_2d(embed_df, metric, sample_id)
    return fig


@app.callback(
    dash.dependencies.Output('sunburst', 'data'),
    [dash.dependencies.Input('sample-dropdown', 'value')])
def update_sunburst_plot(sample_id):
    return h.get_blah_data()

if __name__ == '__main__':
    app.run_server(debug=True)