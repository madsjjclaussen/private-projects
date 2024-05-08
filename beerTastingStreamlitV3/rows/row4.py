import plotly.graph_objects as go
import streamlit as st


def get_violin_chart(df):
    fig = go.Figure()
    for i in df['userName'].unique():
        color = df['userColor'][df['userName'] == i].values[0][:-2]
        textFormatted = df['tastingItemName'][df['userName'] == i].astype(str) + "<br>" + "Rating: " + df['rating'][df['userName'] == i].astype(str) + "<br>"
        fig.add_trace(go.Violin(x=df['userName'][df['userName'] == i],
                                y=df['rating'][df['userName'] == i],
                                name=df['userName'][df['userName'] == i].values[0],
                                line_color=color,
                                hovertext=textFormatted,
                                points='all')
                )
        fig.update_traces(box_visible=True, meanline_visible=True)
        fig.update_layout(margin=dict(t=20, b=1, l=1, r=1), showlegend=False, title="Distribution of ratings per user", yaxis_title="Rating")

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)




def main(df):
    try:
        get_violin_chart(df)

    except Exception as e:
        st.exception(e)

