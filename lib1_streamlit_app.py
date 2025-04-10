import streamlit as st

import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('lib1_data.csv')
df = load_data()

@st.cache_data
def select_triangle(id):
    return df[df['triangleid'] == id]

@st.cache_data
def pivot(df):
    return df.pivot_table(values='res act', index = 'pep_y', columns= 'pep_x', sort=False)



cmap = px.colors.sequential.PuRd_r

st.title('Library 1 screening results')

col1, space, col2 = st.columns((1,0.2,1))

with col1:
    option = st.selectbox('Select triangle ID',([i for i in range(1,65)]))

    t = select_triangle(option)
    data = pivot(t)

    im = px.imshow(data, zmin=30, zmax = 100, color_continuous_scale= cmap)

    scat = im.add_trace(go.Scatter(mode ='markers', x = t['pep_x'], y = t['pep_y'], marker=dict(opacity=0)))

    im.update_layout(height = 500)

    event = st.plotly_chart(im, on_select="rerun", use_container_width = True)
    selected_points = event.selection.points
    # st.write(selected_points)
with col2:
    st.header('Instructions')
    st.write('Navigate and zoom heatmap using panel in the top right corner of the heatmap')
    st.write('Click on square in heatmap for monomer structures and raw data')

if len(selected_points) != 0:
    # st.write(selected_points)
    x1 = selected_points[0]['x']
    y1 = selected_points[0]['y']
    hoversrc = df[(df['pep_x'] == x1) & (df['pep_y'] == y1)]
    if len(hoversrc) != 0:  
        with col2:
            st.header('Monomers')
            col3, space3, col4, space4 = st.columns((1,0.2,1,1.2))


        with col3:
            st.image("./mols/" + str(hoversrc['lib2pepid_x'].values[0]) + '.png',
            caption=hoversrc['pep_x'].values[0])
        with col4:
            st.image("./mols/" + str(hoversrc['lib2pepid_y'].values[0]) + '.png',
            caption=hoversrc['pep_y'].values[0])
        with col2:
            st.header('Raw Data')
            st.write(hoversrc[['pep_x', 'pep_y', 'assayplate_well', 'time0', 'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'slopes', 'rvalue', 'res act']].set_index(['pep_x', 'pep_y']))
