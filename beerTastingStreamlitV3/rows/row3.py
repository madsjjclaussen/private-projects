import streamlit as st
import plotly.graph_objects as go


@st.cache_data
def bar_chart(df):
    df = (
        df.groupby(["tastingItemName", "userName", "userColor", "tastingItemOrder"])
        .sum()
        .reset_index()
    )
    df = df.sort_values(by="tastingItemOrder", ascending=True)

    # Normalized
    fig = go.Figure()
    for i in df["tastingItemName"].unique():
        df_normalized = df[df["tastingItemName"] == i].copy()
        df_normalized["normalized"] = (
            100 * df_normalized["rating"] / df_normalized["rating"].sum()
        )
        df_normalized["normalizedText"] = (
            df_normalized["normalized"].round(1).astype(str) + "% (" + df_normalized["rating"].astype(str) + ")"
        )

        marker_color = df_normalized["userColor"]
        marker_color = [i[:-2] for i in marker_color]
        y = df_normalized["tastingItemName"]
        x = df_normalized["normalized"]
        normalizedText = df_normalized["normalizedText"]

        fig.add_trace(
            go.Bar(
                showlegend=False,
                orientation="h",
                x=x,
                y=y,
                marker_color=marker_color,
                text=normalizedText,
                textposition="inside",
            )
        )

    fig.update_traces(opacity=0.7)

    fig.update_layout(
        margin=dict(t=20, b=1, l=1, r=1),
        showlegend=False,
        title="Percent distribution of ratings per item",
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showline=False,
            zeroline=False,
        ),
        barmode="stack",
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def main(df):
    try:
        bar_chart(df)
    except Exception as e:
        st.exception(e)
