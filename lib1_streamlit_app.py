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
    return df[df['triangle_id'] == id]

@st.cache_data
def pivot(df):
    return df.pivot_table(values='res act', index = 'pep2', columns= 'pep1', sort=False)



cmap = px.colors.sequential.PuRd_r

st.title('Library 1 screening results')

col1, space, col2 = st.columns((1,0.2,1))

with col1:
    option = st.selectbox('Select triangle ID',([i for i in range(1,65)]))

    t = select_triangle(option)
    data = pivot(t)

    im = px.imshow(data, zmin=30, zmax = 100, color_continuous_scale= cmap)

    scat = im.add_trace(go.Scatter(mode ='markers', x = t['pep1'], y = t['pep2'], marker=dict(opacity=0)))

    im.update_layout(height = 500)

    event = st.plotly_chart(im, on_select="rerun", use_container_width = True)
    selected_points = event.selection.points
    # st.write(selected_points)


if len(selected_points) != 0:
    # st.write(selected_points)
    x1 = selected_points[0]['x']
    y1 = selected_points[0]['y']
    hoversrc = df[(df['pep1'] == x1) & (df['pep2'] == y1)]
    if len(hoversrc) != 0:  
        with col2:
            st.header('Raw Data')
            st.write(hoversrc[['pep1', 'pep2', 'assayplate_well', 'time0', 'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'slopes', 'rvalue', 'res act']].set_index(['pep1', 'pep2']))
            st.header('Monomers')
            col3, col4 = st.columns((1,1))


        with col3:
            st.image("./mols/" + str(hoversrc['pep1_lib2id'].values[0]) + '.png',
            caption=hoversrc['pep1'].values[0])
        with col4:
            st.image("./mols/" + str(hoversrc['pep2_lib2id'].values[0]) + '.png',
            caption=hoversrc['pep2'].values[0])