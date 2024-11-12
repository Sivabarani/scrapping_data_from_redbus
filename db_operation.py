import mysql.connector as db

def create_table(bus_details):
    db_details = {
        'user': 'root',
        'password': 'admin123',
        'host': '127.0.0.1',
        'database': 'REDBUS'
    }

    conn = db.connect(**db_details)
    c = conn.cursor()

    add_table = '''CREATE TABLE IF NOT EXISTS bus_routes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date_of_journey VARCHAR(20) NOT NULL,
                    state VARCHAR(100) NOT NULL,
                    route_name VARCHAR(100) NOT NULL,
                    route_link VARCHAR(1000) NOT NULL,
                    bus_name VARCHAR(1000) NOT NULL,
                    bus_type VARCHAR(1000) NOT NULL,
                    departing_time TIME,
                    duration VARCHAR(30),
                    reaching_time TIME,
                    star_rating FLOAT,
                    price DECIMAL(10, 2),
                    available_seats INT
                )'''

    try:
        c.execute(add_table)
        print("Table 'bus_routes' created successfully!")

        for bus in bus_details:
            if 'price' in bus and bus['price']:
                price_str = bus['price'].split()[1]  
                bus['price'] = float(price_str.replace(',', ''))  

            insert_query = '''INSERT INTO bus_routes
                        (date_of_journey, state, route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time,
                        star_rating, price, available_seats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            insert_data = (bus['date'], bus['state'], bus['route'], bus['route_link'], bus['bus_name'], bus['bus_type'],
                           bus['departing_time'], bus['duration'], bus['reaching_time'],
                           bus['star_rating'], bus['price'], bus['available_seats'])
            print(insert_data)
            c.execute(insert_query, insert_data)
            conn.commit()
            
        print("Data inserted successfully!")
    except db.Error as e:
        print(f"Error creating table or inserting data: {e}")
    finally:
        c.close()
        conn.close()
        print("Database connection closed.")