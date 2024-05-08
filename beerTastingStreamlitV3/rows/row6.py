import streamlit as st
import pandas as pd


def get_table(df):
    df = df.sort_values(by="tastingItemOrder", ascending=True)

    df = df[['userName', 'rating', 'tastingItemName', 'tastingItemOrder']]
    df = pd.pivot_table(df, values='rating', index=['tastingItemName', 'tastingItemOrder'], columns='userName').reset_index()
    df = df.sort_values(by='tastingItemOrder', ascending=False).drop(columns=['tastingItemOrder']).set_index('tastingItemName')
    ratingCols = df.columns

    df['Total Score'] = df[ratingCols].sum(axis=1)
    df['Placing'] = df['Total Score'].rank(ascending=False, method='min').astype(int)

    df['Standard Deviation'] = df[ratingCols].std(axis=1)
    df['Difference (min - max)'] = df[ratingCols].max(axis=1) - df[ratingCols].min(axis=1)
    st.dataframe(
        df.style.format(precision=0).background_gradient(axis=0, subset=['Difference (min - max)', 'Standard Deviation'], cmap='bone', ),
        hide_index=False,
        use_container_width=True,
    )


def main(df):
    try:
        st.markdown("###### <b>Agreement comparison</b>", unsafe_allow_html=True)
        get_table(df)

    except Exception as e:
        st.exception(e)
