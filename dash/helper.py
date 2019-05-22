import plotly.graph_objs as go
import pandas as pd
import numpy as np


pca_explain_var_dic = {
    'hyperbolic': [40.2, 22.67, 10.1],
    'word2vec': [ 37.4, 16.3, 9.1]
}


def get_plot_3d(pca_df, embedding):
    pca_explain_vars = pca_explain_var_dic[embedding]

    data = []

    pca_df['sample_id_display'] = pca_df['sample_id'].apply(lambda x: 'sample_id: {0}'.format(x))
    
    for label in ['feces', 'saliva', 'sebum']:
        adf = pca_df[pca_df.label == label]
        sample_ids = adf['sample_id']
        x = adf['PCA1']
        y = adf['PCA2']
        z = adf['PCA3']
        env_material = pca_df['label']
        
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
                title= 'PCA1 ({0} %)'.format(pca_explain_vars[0])
            ),
            yaxis=dict(
                title='PCA2 ({0} %)'.format(pca_explain_vars[1])
            ),
            zaxis=dict(
                title='PCA3 ({0} %)'.format(pca_explain_vars[2])
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #print(fig)
    return fig


def get_plot_2d(pca_df, embedding):
    pca_explain_vars = pca_explain_var_dic[embedding]

    data = []
    
    pca_df['sample_id_display'] = pca_df['sample_id'].apply(lambda x: 'sample_id: {0}'.format(x))

    for label in ['feces', 'saliva', 'sebum']:
        adf = pca_df[pca_df.label == label]
        sample_ids = adf['sample_id']
        x = adf['PCA1']
        y = adf['PCA2']
        env_material = pca_df['label']
        
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
            title= 'PCA1 ({0} %)'.format(pca_explain_vars[0])
        ),
        yaxis=dict(
            title='PCA2 ({0} %)'.format(pca_explain_vars[1])
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #print(fig)
    return fig