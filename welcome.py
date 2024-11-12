import streamlit as st

st.write("# Project Overview: Bus Information Dashboard")

st.write("## Purpose")
st.write("""
The purpose of this Streamlit application is to provide users with dynamic bus information based on various criteria such as state, route, price range, star rating, and bus type. Users can select different options to filter and view bus details fetched from a MySQL database.
""", unsafe_allow_html=True)

st.write("## Functionality")
st.write("""
### Selections and Filtering:
- Users can choose a state and select a specific route within that state.
- Price range, star rating, and bus type can be further filtered to narrow down search results.

### Database Connectivity:
- The application connects to a MySQL database (REDBUS) using credentials (username, password).

### Data Fetching:
- **States and Routes:** 11 Available states and corresponding routes are fetched dynamically from the database.
- **Bus Information:** Queries are executed based on user selections to fetch relevant bus details matching the criteria.

### Display and Interaction:
- Results are displayed in a tabular format showing bus ID, route name, bus name, type, departure time, duration, reaching time, star rating, price, and available seats.
- A count of buses found is shown at the bottom right corner aligned to the right.

### Error Handling:
- Errors related to database queries or fetching are displayed as error messages to the user.
""", unsafe_allow_html=True)

st.write("## Technologies Used")
st.write("""
- **Python Libraries:** Pandas for data manipulation, Streamlit for building interactive web applications.
- **Database:** MySQL database for storing and retrieving bus-related data.
- **Web Framework:** Streamlit for creating a user-friendly dashboard interface.
- **Selenium:** To fetch the data from website.
""", unsafe_allow_html=True)

st.write("## Future Enhancements")
st.write("""
- Implementing additional features such as sorting columns in the bus information table.
- Improving error handling and user feedback.
""", unsafe_allow_html=True)
