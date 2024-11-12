import streamlit as st

dashboard = st.Page("welcome.py", title="Dashboard", icon=":material/dashboard:", default=True)
buses = st.Page("view_buses.py", title="Bus Information", icon=":material/info:")

pg = st.navigation(
    {
        "DashBoard": [dashboard],
        "Bus":[buses]
    }
)
pg.run()