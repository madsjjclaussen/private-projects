import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression


def get_scatter_chart(df):
    fig = go.Figure()

    for i in df["userName"].unique():
        color = df["userColor"][df["userName"] == i].values[0][:-2]
        text = f'{df["rating"][df["userName"] == i].values[0]} ({df["alcohol"][df["userName"] == i].values[0]}%)'
        x = df["alcohol"][df["userName"] == i]
        y = df["rating"][df["userName"] == i]

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=df["userName"][df["userName"] == i].values[0],
                line_color=color,
                mode="markers+text",
                opacity=1,
                text=text,
                textposition="bottom center",
                textfont=dict(size=12, weight="bold", color="black"),
            )
        )

        # Tendline per user
        regr = LinearRegression()
        _ = regr.fit(np.array(x).reshape(-1, 1), np.array(y))
        fit = regr.predict(np.array(x).reshape(-1, 1))
        fig.add_trace(
            go.Scatter(
                x=x,
                y=fit,
                mode="lines",
                name=df["userName"][df["userName"] == i].values[0],
                line_color=color,
                opacity=0.3,
            )
        )

    # Trendline for all users
    x =  df["alcohol"]
    y = df["rating"]
    all_regr = LinearRegression()
    _ = all_regr.fit(np.array(x).reshape(-1, 1), np.array(y))
    all_fit = all_regr.predict(np.array(x).reshape(-1, 1))
    fig.add_trace(
        go.Scatter(
            x= x,
            y=all_fit,
            mode="lines",
            name="All users",
            line_color="black",
            line_dash="dash",
            opacity=0.6,
        )
    )

    fig.update_layout(
        margin=dict(t=50, b=1, l=1, r=1),
        showlegend=True,
        title="Ratings compared to alcohol",
        yaxis=dict(dtick=1, title="Rating"),
        xaxis=dict(dtick=0.2, title="Alcohol", ticksuffix="%"),
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)



def main(df):
    try:
        get_scatter_chart(df)

    except Exception as e:
        st.exception(e)
