import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


@st.cache_data
def bar_chart(df):
    df = (
        df.groupby(["userName", "userColor", "mainType"])
        .sum()
        .reset_index()
    )

    df['percent'] = ((df['rating'] / df.groupby('userName')['rating'].transform('sum')) * 100).round(2)

    fig = go.Figure()
    for i in df["userName"].unique():
        dff = df[df["userName"] == i].copy()
        dff["text"] = dff["percent"].astype(str) + "% (" + dff["rating"].astype(str) + ")"
        marker_color = dff["userColor"]
        marker_color = [i[:-2] for i in marker_color]
        x = dff["mainType"].unique()
        y = dff["percent"]
        text = dff["text"]
        name = dff["userName"].values[0]

        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                name=name,
                marker_color=marker_color,
                text=text,
                textposition="inside",
                textfont=dict(
                    size=12,
                ),
                opacity=0.8,
                base=0
            )
        )

# Mean per item
    for i in df["tastingItemName"].unique():
        dff = df[df["tastingItemName"] == i].copy()
        x = dff["mainType"].unique()
        mean = dff["percent"].mean().round(1)
        text = f" {mean}%"
        fig.add_trace(
            go.Scatter(
                mode="markers+text",
                y=[mean],
                x=x,
                marker_symbol="line-ew-open",
                marker_size=20,
                marker_color="black",
                text=text,
                textposition="middle right",
                textfont=dict(size=15, weight="bold", color="black"),
            )
        )


    fig.update_layout(
        title="Percent distribution of ratings per type & user",
        margin=dict(t=20, b=1, l=1, r=1),
        showlegend=False,
        xaxis=dict(
            zeroline=False,
            tickangle=-15
        ),
        yaxis=dict(
            zeroline=False,
        ),
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def main(df):
    try:
        bar_chart(df)
    except Exception as e:
        st.exception(e)
