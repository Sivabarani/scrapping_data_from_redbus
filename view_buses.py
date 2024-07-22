import pandas as pd
import streamlit as st
import mysql.connector as db
import datetime

db_details = {
    'user': 'root',
    'password': 'admin123',
    'host': '127.0.0.1',
    'database': 'MDT36'
}

conn = db.connect(**db_details)
c = conn.cursor()

def get_result(results):
    data = []
    for bus in results:
        departing_time_str = str(bus[7])
        reaching_time_str = str(bus[9])

        try:
            departing_time = datetime.datetime.strptime(departing_time_str, '%H:%M:%S').strftime('%I:%M %p')
            reaching_time = datetime.datetime.strptime(reaching_time_str, '%H:%M:%S').strftime('%I:%M %p')
        except ValueError as e:
            st.error(f"Error parsing time: {e}")
            continue

        row = {
            'Bus Id': bus[0],
            'Route Name': bus[3],
            'Bus Name': bus[5],
            'Bus Type': bus[6],
            'Departing Time': departing_time,
            'Duration': bus[8],
            'Reaching Time': reaching_time,
            'Star Rating': bus[10],
            'Price': bus[11],
            'Available Seats': bus[12]
        }
        data.append(row)
    data =  pd.DataFrame(data, index=[i for i in range(1, len(data)+1)]) # Give index for dataframe
    return data

def get_states_list():
    try:
        get_states_query = 'SELECT state, count(state) as count FROM bus_routes GROUP BY state ORDER BY state ASC;'
        c.execute(get_states_query)
        states_list = c.fetchall() # it returns state, and count of buses in this state
        states = [bus[0] for bus in states_list] # get only states
        return states
    except db.Error as e:
        st.error(f"Error fetching states: {e}")
        return []

def get_routes_list(state):
    try:
        route_list_query = f'SELECT route_name from bus_routes where state="{state}"'
        c.execute(route_list_query)
        routes_list = c.fetchall()
        routes = [bus[0] for bus in routes_list] # get routes only on particular state
        return list(set(routes))
    except db.Error as e:
        st.error(f"Error fetching routes: {e}")
        return []

def get_bus_data_from_db(state, route, min_price, max_price, min_rating, max_rating, bus_type):
    try:
        get_bus_list_query = f'SELECT * FROM bus_routes WHERE state = "{state}" and route_name = "{route}"'

        # For price range
        if min_price is not None and max_price is not None:
            get_bus_list_query += f' AND price BETWEEN {min_price} AND {max_price}'
        elif min_price is not None:
            get_bus_list_query += f' AND price <= {min_price}'
        elif max_price is not None:
            get_bus_list_query += f' AND price >= {max_price}'

        # For star rating range
        if min_rating is not None and max_rating is not None:
            get_bus_list_query += f' AND `star_rating` BETWEEN {min_rating} AND {max_rating}'
        elif min_rating is not None:
            get_bus_list_query += f' AND `star_rating` <= {min_rating}'
        elif max_rating is not None:
            get_bus_list_query += f' AND `star_rating` >= {max_rating}'

        # For bus route
        if bus_type != 'Select Type':
            if bus_type.upper() == 'A/C':
                get_bus_list_query += ' AND (`bus_type` LIKE "%AC%" OR `bus_type` LIKE "%A/C%")'
                get_bus_list_query += ' AND (`bus_type` NOT LIKE "%NON AC%" AND `bus_type` NOT LIKE "%NON A/C%")'
            elif bus_type.upper() == 'NON A/C':
                get_bus_list_query += ' AND (`bus_type` LIKE "%NON AC%" OR `bus_type` LIKE "%NON A/C%")'
            else:
                get_bus_list_query += f' AND (`bus_type` LIKE "%{bus_type}%")'

        c.execute(get_bus_list_query)
        get_bus_list = c.fetchall()
        buses = get_result(get_bus_list)
        return buses
    except db.Error as e:
        st.error(f"Error fetching bus data: {e}")
        return []

def get_min_max_value(value):
    if 'Above' in value:
        actual_value = value.split()[1]
        return None, actual_value
    elif 'Below' in value:
        actual_value = value.split()[1]
        return actual_value,None
    elif '-' in value:
        actual_value = value.split('-')
        return actual_value[0], actual_value[1]
    else:
        return None, None

def main():
    st.title('Bus Information')

    state_list = get_states_list()
    option_state = st.selectbox("Which state do you want to see bus information for?", state_list)

    route_list = get_routes_list(option_state)
    option_route = st.selectbox("Select a route:", route_list)

    prices_list = ['Select Prices', 'Below 100', '100-200', '200-400', '400-600', '600-800', '800-1000', 'Above 1000']
    option_price = st.selectbox("Select a Price:", prices_list)
    min_price, max_price = get_min_max_value(option_price)

    star_rating_list = ['Select star rating', 'Below 1.0', '1.0-2.0', '2.0-3.0', 'Above 4.0']
    option_star_rating = st.selectbox("Select star rating:", star_rating_list)
    min_rating, max_rating = get_min_max_value(option_star_rating)

    bus_type_list = ['Select Type', 'A/C', 'NON A/C', 'Sleeper', 'Seater']
    option_bus_type = st.selectbox("Select bus type:", bus_type_list)

    st.write(f"Bus Information for {option_state} - Route: {option_route}:")
    buses = get_bus_data_from_db(option_state, option_route, min_price, max_price, min_rating, max_rating, option_bus_type)

    st.markdown(f'<p style="text-align:right">{len(buses)} buses found</p>', unsafe_allow_html=True)
    st.write("Please use scroll to view full content")
    if len(buses) == 0:
        st.error("No Bus Found")
    else:
        st.dataframe(buses)
    conn.close()
main()
