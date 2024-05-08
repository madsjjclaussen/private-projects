import streamlit as st
import configs
df = configs.run_config(title="Dashboard")
from rows import row1, row2, row3, row4, row5, row6, row7, row8

row1.main(df)
st.divider()
row2.main(df)
st.divider()
row3.main(df)
st.divider()
row4.main(df)
st.divider()
row5.main(df)
st.divider()
row6.main(df)
st.divider()
row7.main(df)
st.divider()
row8.main(df)
