import plotly.graph_objs as go
import pandas as pd
import numpy as np


pca_explain_var_dic = {
    'no_embedding': [40.2, 5.1, 4.4],
    'pcoa': [18.4, 9.4, 4.4],
    'hyperbolic':  [40.1, 22.8, 9.4],
    'word2vec': [65.9, 12.8, 4.2]
}


def get_plot_3d(pca_df, embedding, sample_id=None):
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
                opacity=0.7
            )
        )

        data.append(trace)

    if sample_id:
        # add new trace single point
        sdf = pca_df[pca_df.sample_id == sample_id]
        print(sdf.shape)
        sample_ids = sdf['sample_id']
        x = sdf['PCA1']
        y = sdf['PCA2']       
        z = adf['PCA3']  
        sample_trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text=adf['sample_id_display'],
            name='sample_id: {0}'.format(sample_id),
            mode='markers',
            marker=dict(
                size=10,
                opacity=1,
                color='red',
                symbol='x'
            )
        )
        data.append(sample_trace)
        
    layout = go.Layout(
        width=700,
        height=700,
       # autosize=False,
       margin=dict(
            l=50,
            r=50,
            b=50,
            t=50
        ),
        legend=dict(
            y=0.7,
            x=0.95
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
            ),
            camera = dict(
                #up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #print(fig)
    return fig


def get_plot_2d(pca_df, embedding, sample_id=None):
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

    if sample_id:
        # add new trace single point
        sdf = pca_df[pca_df.sample_id == sample_id]
        print(sdf.shape)
        sample_ids = sdf['sample_id']
        x = sdf['PCA1']
        y = sdf['PCA2']       
        
        sample_trace = go.Scattergl(
            x=x,
            y=y,
            text=adf['sample_id_display'],
            name='sample_id: {0}'.format(sample_id),
            mode='markers',
            marker=dict(
                size=10,
                opacity=1,
                color='red',
                symbol='star'
            )
        )
        data.append(sample_trace)
        
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


def get_sunburst_plot(df, sample_id):
    # example sample ID
    df_sample = df[['phylum', 'class', 'weight']][df['sample_id'] == int(sample_id)]

    # double group by
    df_sample = df_sample.groupby(['phylum', 'class']).sum()
    df_sample.reset_index(inplace=True)

    # define hierarchy for sunburst plot
    tax_labels = list(df_sample['class'])
    tax_parents = list(df_sample['phylum'])

    # values
    values = df_sample['weight'].tolist()

    # add kingdom to pylum relationship
    for phyla in list(df_sample['phylum'].unique()):
        tax_labels.append(phyla)
        tax_parents.append('Bacteria')
        values.append(1)

    # add kingdom as center of sunburst
    tax_labels.append('Bacteria')
    tax_parents.append("")

    # plot sunbust
    trace = go.Sunburst(
        labels=tax_labels,
        parents=tax_parents,
        values=values,
        outsidetextfont={"size": 20, "color": "#377eb8"},
        marker={"line": {"width": 2}})

    layout = go.Layout(margin=go.layout.Margin(t=0, l=0, r=0, b=0))
    fig = go.Figure([trace], layout)
    return fig


def get_blah_data():
    return {
        'name': 'Bacteria',
        'children': [
            {
                'name': 'Proteobacteria',
                'children': [
                    {'name': 'Alphaproteobacteria', 'size': 2.48},
                    {'name': 'Betaproteobacteria', 'size': 4.16},
                    {'name': 'Deltaproteobacteria', 'size': 0.69},
                    {'name': 'Gammaproteobacteria', 'size': 28.47},
                ]
            },
            {
                'name': 'Firmicutes',
                'children': [
                    {'name': 'Bacilli', 'size': 1.38},
                    {'name': 'Clostridia', 'size': 14.58},
                    {'name': 'Erysipelotrichi', 'size': 1.79},
                ]
            }
        ]
    }