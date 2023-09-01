import networkx as nx
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt


st.set_page_config(page_title='Graph Theory', layout='wide', initial_sidebar_state='expanded')
primary = st.get_option("theme.primaryColor")
s = f"""
<style>
div.stButton > button:first-child {{ border: 5px solid {primary}; border-radius: 10px;}}
"""
st.markdown(s, unsafe_allow_html=True)

@st.cache_data
def load_data(file: str, min: int, max: int) -> pd.DataFrame:
    data = pd.read_csv(file)
    
    data = data.drop_duplicates().reset_index(drop=True)
    cities = data.iloc[min:max]
    data_limited = data.iloc[min:max]
    return data_limited

df = load_data('2008.csv', 0, 1000)

graph = nx.from_pandas_edgelist(df, source='Origin', target='Dest', edge_attr=True)

plt.figure(figsize=(12,8))
nx.draw_networkx(graph, with_labels=True)
pos = nx.spring_layout(graph, seed=200)

shortest_path_distance = nx.dijkstra_path(graph, source='HOU', target='PHL', weight='Distance')
path_edges = list(zip(shortest_path_distance, shortest_path_distance[1:]))
nx.draw_networkx_nodes(graph, pos, nodelist=shortest_path_distance, node_color='r')
nx.draw_networkx_edges(graph, pos, edgelist=path_edges, width=5)
plt.axis('equal')

st.title('title')