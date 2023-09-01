import networkx as nx
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

min = 0
max = 200
file = '2008 top 5000.csv'
default_option = 'Select'
seed = 1

# Load data and create graph
@st.cache_data
def load_csv() -> pd.DataFrame:
    data = pd.read_csv(file)
    data = data.drop_duplicates().reset_index(drop=True)
    return data

@st.cache_data
def load_data() -> pd.DataFrame:
    data = load_csv()
    data_limited = data.iloc[min:max]
    return data_limited

@st.cache_data
def load_cities() -> pd.DataFrame:
    data = load_csv()
    temp = data.iloc[min:max]
    origin = np.insert(temp["Origin"].astype(str).unique(), 0, default_option)
    dest = np.insert(temp["Dest"].astype(str).unique(), 0, default_option)
    return origin, dest

@st.cache_data
def load_graph() -> pd.DataFrame:
    data = load_data()
    graph = nx.from_pandas_edgelist(data, source='Origin', target='Dest', edge_attr=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw_networkx(graph, with_labels=True, ax=ax)
    pos = nx.spring_layout(graph, seed=seed)

    return graph, fig, ax, pos

def main():
    st.set_page_config(page_title='Graph Theory', layout='wide', initial_sidebar_state='expanded')
    primary = st.get_option("theme.primaryColor")
    s = f"""
    <style>
    div.stButton > button:first-child {{ border: 5px solid {primary}; border-radius: 10px;}}
    </style>
    """
    st.markdown(s, unsafe_allow_html=True)

    st.title('Graph Theory')

    cities = load_cities()
    
    source = st.sidebar.selectbox("Origin", (cities[0]), index=0)
    target = st.sidebar.selectbox("Destination", (cities[1]), index=0)
    weight = st.sidebar.selectbox("Weight", (default_option, 'Distance', 'AirTime'), index=0)

    if source == default_option or target == default_option or weight == default_option:
        st.warning('Select Origin, Destination and Weight to find the shortest path')

    items = load_graph()
    graph = items[0]
    fig = items[1]
    ax = items[2]
    pos = items[3]
    
    if source != default_option and target != default_option and weight != default_option:

        shortest_path_distance = nx.dijkstra_path(graph, source=source, target=target, weight=weight)
        path_edges = list(zip(shortest_path_distance, shortest_path_distance[1:]))
        nx.draw_networkx_nodes(graph, pos, nodelist=shortest_path_distance, node_color='r', ax=ax)
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, width=5, ax=ax)
        ax.axis('equal')

    st.pyplot(fig)

if __name__ == '__main__':
    main()
