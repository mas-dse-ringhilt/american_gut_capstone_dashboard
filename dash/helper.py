import plotly.graph_objs as go
import pandas as pd
import numpy as np


def get_bar_plot(height=600):
    data = []

    trace = go.Bar(
        name='test',
        x=[1, 2, 3],
        y=[4, 5, 6],
    )
    data.append(trace)

    layout = go.Layout(
        showlegend=True,
        #paper_bgcolor='rgb(243, 243, 243)',
        #plot_bgcolor='rgb(243, 243, 243)',
        height=height,
        margin=go.layout.Margin(l=50, r=10, t=10, b=30)
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def get_hyper_plot_3d():
    data= []
    
    hyper_df = pd.read_csv('../data/hyperbolic_bodysite_pca.csv')

    hyper_df['sample_id_display'] = hyper_df['sample_id'].apply(lambda x: 'sample_id: {0}'.format(x))
    
    for label in ['feces', 'saliva', 'sebum']:
        adf = hyper_df[hyper_df.label == label]
        sample_ids = adf['sample_id']
        x=adf['PCA1']
        y=adf['PCA2']
        z=adf['PCA3']
        env_material = hyper_df['label']
        
        trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text=adf['sample_id_display'],
            name=adf['label'].iloc[0],
            mode='markers',
            marker=dict(
                opacity=0.8
            )
        )

        data.append(trace)
        
    layout = go.Layout(
        width=600,
        height=600,
       # autosize=False,
       margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        legend=dict(
            y=0.7,
            x=0.8
        ),
        
        clickmode='event+select',
        hovermode='closest',
        scene = dict(
            aspectmode='cube',
            xaxis=dict(
                title= 'PCA1 (40.2 %)'
            ),
            yaxis=dict(
                title='PCA2 (22.67 %)'
            ),
            zaxis=dict(
                title='PCA3 (? %)'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #print(fig)
    return fig


def get_hyper_plot_2d():
    data= []
    
    hyper_df = pd.read_csv('../data/hyperbolic_bodysite_pca.csv')
    
    hyper_df['sample_id_display'] = hyper_df['sample_id'].apply(lambda x: 'sample_id: {0}'.format(x))

    for label in ['feces', 'saliva', 'sebum']:
        adf = hyper_df[hyper_df.label == label]
        sample_ids = adf['sample_id']
        x=adf['PCA1']
        y=adf['PCA2']
        env_material = hyper_df['label']
        
        trace = go.Scattergl(
            x=x,
            y=y,
            text=adf['sample_id_display'],
            name=adf['label'].iloc[0],
            mode='markers',
            marker=dict(
                opacity=0.8
            )
        )

        data.append(trace)
        
    layout = go.Layout(
        height=600,
        width=600,
        clickmode='event+select',
        hovermode='closest',
        xaxis=dict(
            title= 'PCA1 (40.2 %)'
        ),
        yaxis=dict(
            title='PCA2 (22.67 %)'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #print(fig)
    return fig