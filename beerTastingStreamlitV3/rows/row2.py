import streamlit as st
import altair as alt
import plotly.graph_objects as go





@st.cache_data
def get_dataframe(df):
    df = df.sort_values(by="tastingItemOrder", ascending=True)

    df = (
        df.groupby(["userName"])
        .agg(total=("rating", "sum"), mean=("rating", "mean"), std=("rating", "std"), hist=("rating", list))
        .reset_index()
    )
    df.rename(columns={"total": "Total", "mean": "Mean", "std": "Standard deviation"}, inplace=True)
    st.dataframe(
        df.style.format(precision=2).background_gradient(axis=0, subset=['Total', 'Mean', 'Standard deviation'], cmap='Blues', ),
        column_config={
            "hist": st.column_config.LineChartColumn(
                "Rating history",
            ),
            "userName": "User",
        },
        hide_index=True,
        use_container_width=True,
        # height=200
    )


@st.cache_data
def get_radial_chart_varity(df):
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df['userName'],
        values=df['rating'],
        )
    )
    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent+value', texttemplate = "%{label}: %{value} <br>(%{percent})", hovertemplate = "%{label}: %{value} <br>(%{percent})", textposition='inside',
                  marker=dict(colors=df['userColor'], line=dict(color='#000000', width=0.1)))

    fig.update_layout(
        margin=dict(t=20, b=1, l=1, r=1),
        showlegend=False,
        height=200,
        title="Total ratings",
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def main(df):
    try:
        # Row3
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            get_dataframe(df)
        with c2:
            get_radial_chart_varity(df)

    except Exception as e:
        st.exception(e)

