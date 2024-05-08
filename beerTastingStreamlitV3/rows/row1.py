import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


@st.cache_data
def bar_chart(df):
    df = (
        df.groupby(["tastingItemName", "userName", "userColor", "tastingItemOrder"])
        .sum()
        .reset_index()
    )
    dfs = df.groupby("tastingItemName").sum().reset_index()
    df = df.merge(
        dfs[["tastingItemName", "rating"]],
        on="tastingItemName",
        suffixes=("", "_total"),
    )
    df = df.sort_values(by="rating_total", ascending=True)

    fig = go.Figure()
    for i in df["tastingItemName"].unique():
        dff = df[df["tastingItemName"] == i].copy()
        dff["text"] = dff["rating"].astype(str) + " (" + dff["userName"] + ")"
        marker_color = dff["userColor"]
        marker_color = [i[:-2] for i in marker_color]
        y = dff["tastingItemName"]
        x = dff["rating"]
        text = dff["text"]

        fig.add_trace(
            go.Bar(
                showlegend=False,
                orientation="h",
                x=x,
                y=y,
                marker_color=marker_color,
                text=text,
                textposition="inside",
                textfont=dict(
                    size=12,
                ),
                opacity=0.7,
            )
        )

        # Mean per item
        mean = dff["rating"].mean().round(1)
        fig.add_trace(
            go.Scatter(
                mode="markers+text",
                x=[mean],
                y=y,
                marker_symbol="line-ns-open",
                marker_size=20,
                marker_color="black",
                text=[mean],
                textposition="top center",
                textfont=dict(size=15, weight="bold", color="black"),
            )
        )

    # Total Numbers
    fig.add_trace(
        go.Scatter(
            orientation="h",
            y=dfs["tastingItemName"],
            x=dfs["rating"] + 0.15,
            text=dfs["rating"],
            mode="text",
            textposition="middle right",
            textfont=dict(
                size=20,
                weight="bold",
            ),
            showlegend=False,
        )
    )

    # Mean Total
    totalMean = dfs["rating"].mean()
    fig.add_vline(
        x=totalMean,
        opacity=0.2,
        line=dict(color="darkgreen", width=6, dash="solid"),
        annotation=dict(font_size=20),
        annotation_text=f" Mean: " + str(totalMean),
        annotation_position="bottom right",
    )

    fig.update_layout(
        margin=dict(t=20, b=1, l=1, r=1),
        showlegend=False,
        xaxis=dict(
            zeroline=False,
        ),
        yaxis=dict(
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
