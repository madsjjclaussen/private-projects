import streamlit as st
import os
import pandas as pd
import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv(override=True)


def get_client():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    return supabase

def clear_cache():
    """Clears cached data if Refresh button is clicked."""
    get_data.clear()


@st.cache_data(show_spinner=True)
def get_data():
    tastingUid = '323ff5e4-6e04-4499-9be1-f1ae430f41ce'
    supabase = get_client()
    data, _ = (
        supabase.table("tastingRatings")
        .select("*, users(name, color), tastingItems(name, order, details)")
        .eq("tastingUid", tastingUid)
        .execute()
    )
    
    df = pd.json_normalize(data[1])
    renames = {'users.name': 'userName', 'users.color': 'userColor', 'tastingItems.name': 'tastingItemName', 'tastingItems.order': 'tastingItemOrder', 'tastingItems.details.alcohol': 'alcohol', 'tastingItems.details.type': 'mainType'}
    df = df.rename(columns=renames)
    df['tastingItemOrder'] = df['tastingItemOrder'].astype(int)
    df['rating'] = df['rating'].astype(int)
    df['alcohol'] = df['alcohol'].str.replace('%', '').replace('Unknown', np.nan).astype(float)

    df = df.sort_values(by="tastingItemOrder", ascending=True)
    return df


def filter_options(df):
    if st.button("Refresh data", on_click=clear_cache, help="Click to refresh data"):
        st.rerun()

    # "userName" filter
    st.sidebar.markdown("#### User")
    userNameOptions = df["userName"].unique()
    selected = st.multiselect("Select users here...", userNameOptions, label_visibility="collapsed")
    if len(selected):
        df = df[df["userName"].isin(selected)]

    # "tastingItemName" filter
    st.sidebar.markdown("#### Item")
    tastingItemoptions = df["tastingItemName"].unique()
    selected = st.multiselect("Select item here...", tastingItemoptions, label_visibility="collapsed")
    if len(selected):
        df = df[df["tastingItemName"].isin(selected)]

    # "tastingMainType" filter
    st.sidebar.markdown("#### Type")
    tastingMainType = df["mainType"].unique()
    selected = st.multiselect("Select type here...", tastingMainType, label_visibility="collapsed")
    if len(selected):
        df = df[df["mainType"].isin(selected)]
    
    # Slider - User Ratings
    st.sidebar.markdown("#### User Ratings")
    min_rating= df["rating"].min()
    max_rating = df["rating"].max()
    if min_rating == max_rating:
        st.warning("No user rating data available")
    else:
        ratings = st.slider("Select user ratings here...", min_rating, max_rating, (min_rating, max_rating), label_visibility="collapsed")
        if ratings[0] != min_rating or ratings[1] != max_rating:
            df = df[(df["rating"] >= ratings[0]) & (df["rating"] <= ratings[1])]

    # Slider - Alcohol percent
    st.sidebar.markdown("#### Alcohol Percentage")
    min_alcohol = df["alcohol"].min()
    max_alcohol = df["alcohol"].max()
    if min_alcohol == max_alcohol or np.isnan(min_alcohol):
        st.warning("No alcohol percentage data available")
    else:
        alcohol = st.slider("Select alcohol percentage here...", min_alcohol, max_alcohol, (min_alcohol, max_alcohol), label_visibility="collapsed")
        if alcohol[0] != min_alcohol or alcohol[1] != max_alcohol:
            df = df[(df["alcohol"] >= alcohol[0]) & (df["alcohol"] <= alcohol[1])]
    
    df = df.sort_values(by="tastingItemOrder", ascending=True)
    return df



def run_config(title: str):
    # Set page config
    TITLE = title
    ICON = "📊"
    st.set_page_config(page_title=TITLE, page_icon=ICON, layout="wide", initial_sidebar_state="expanded")

    # Get unfiltered data
    source = get_data()

   # Filter options in sidebar
    with st.sidebar:
        df = filter_options(source)
    return df
        