from dash import Dash, html, dash_table, dcc, callback, Output, Input 
import pandas as pd 
import plotly.graph_objects as po 
import numpy as np
import glob 
import re
from scipy.spatial.distance import cdist



# jk = glob.glob('*')
with open('names.txt','r') as f:
    jk = [i.rstrip() for i in f]

op = [re.sub('.*\\\\', '', i) for i in jk]
# aa = re.sub( '_..csv','',op[0])
oppo = [re.sub('_..csv','',i) for i in op]
index_list = []
for i in range(len(oppo)):
    for j in range(i+1, len(oppo)):
        if oppo[i] == oppo[j]:
            index_list.append((i,j))

# print(index_list)


app = Dash( ) 
server = app.server
app.layout = [
    
    html.Div(children = 'Visualization'),
    html.Hr(),
    dcc.RadioItems(options = [0,1,2,3,4,5], value = 1, id = 'radio-item-controls'),
    dcc.Graph(figure = {}, id = 'figure-output-control')
]

@callback(
    Output(component_id = 'figure-output-control', component_property = 'figure'),
    Input(component_id = 'radio-item-controls', component_property = 'value')
)
def update_graph(protein_pair_index):
    # print(index_list)
    a = pd.read_csv(jk[index_list[protein_pair_index][0]])
    b = pd.read_csv(jk[index_list[protein_pair_index][1]])
    pos_A = a[['x','y','z']]
    pos_B = b[['x','y','z']]
    fig = po.Figure()
    euclidean_dist = cdist(pos_A, pos_B, metric= 'euclidean')
    minimum_dist = np.min(euclidean_dist)
    maximum_dist = np.max(euclidean_dist)
    for i in range(2,60,1):
        oo = np.where(euclidean_dist < i)
        fig.add_trace(po.Scatter3d(   x = np.asarray(a['x']), y = np.asarray(a['y']), z = np.asarray(a['z']), mode = 'markers',showlegend=False))

        fig.add_trace(po.Scatter3d(   x = np.asarray(b['x']), y = np.asarray(b['y']), z = np.asarray(b['z']), mode='markers',showlegend=False))

        fig.add_trace(po.Scatter3d(   x = np.asarray(a.iloc[oo[0]]['x']), y = np.asarray(a.iloc[oo[0]]['y']), z = np.asarray(a.iloc[ oo[0]]['z']), mode = 'markers',marker = dict(color='yellow'),showlegend=False))

        fig.add_trace(po.Scatter3d(   x = np.asarray(b.iloc[oo[1]]['x']), y = np.asarray(b.iloc[oo[1]]['y']), z = np.asarray(b.iloc[oo[1]]['z']), mode = 'markers',name = f'cutoff {i}'))

    fig.data[0].visible = True
    # fig.data[1].visible = True
    # fig.data[2].visible = True
    # fig.data[3].visible = True

    steps = []

    for i in range(0,len(fig.data),4):
        step = dict(
            method = 'update',
            args = [{'visible': [False]*len(fig.data)},
                    ]
        )
        step["args"][0]['visible'][i] = True 
        step["args"][0]['visible'][i+1] = True 
        step["args"][0]['visible'][i+2] = True 
        step["args"][0]['visible'][i+3] = True 
        steps.append(step)
        
        
        sliders = [dict(active = 5,
                        steps = steps)]

    fig.update_layout(title =f'proteins- min {minimum_dist}, max {maximum_dist}',sliders = sliders,
        scene=dict(
                        xaxis_title='X Axis',
                        yaxis_title='Y Axis',
                        zaxis_title='Z Axis'),
                    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)