import plotly.graph_objects as go
import streamlit as st


def get_line_chart(df):
    df = df.sort_values(by="tastingItemOrder", ascending=True)
    fig = go.Figure()

    for i in df["userName"].unique():
        color = df["userColor"][df["userName"] == i].values[0][:-2]

        fig.add_trace(
            go.Scatter(
                x=df["tastingItemName"][df["userName"] == i],
                y=df["rating"][df["userName"] == i],
                name=df["userName"][df["userName"] == i].values[0],
                line_color=color,
                mode="lines+markers+text",
                opacity=0.7,
                text=df["rating"][df["userName"] == i],
                textposition="bottom center",
                textfont=dict(size=12, weight="bold", color="black"),
            )
        )

    # Mean
    df = (
        df.groupby(["tastingItemName", "tastingItemOrder"])["rating"]
        .mean()
        .reset_index()
    )
    df['rating'] = df['rating'].round(1)
    df = df.sort_values(by="tastingItemOrder", ascending=True)
    fig.add_trace(
        go.Scatter(
            mode="lines+markers+text",
            x=df["tastingItemName"],
            y=df["rating"],
            name="mean",
            opacity=0.7,
            text=df["rating"],
            textposition="bottom center",
            textfont=dict(size=12, weight="bold", color="black"),
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )

    fig.update_layout(
        margin=dict(t=50, b=1, l=1, r=1),
        showlegend=True,
        legend=dict(
            yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(0,0,0,0)"
        ),
        title="Ratings over time",
        yaxis_title="Rating",
        xaxis=dict(tickangle=-15),
        yaxis=dict(range=[0, 10], dtick=1),
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def main(df):
    try:
        get_line_chart(df)

    except Exception as e:
        st.exception(e)
