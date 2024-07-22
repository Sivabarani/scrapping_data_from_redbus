# scrapping_data_from_redbus
To fetch the data from redbus website and store the Mysql database. Finally, fetch the mysql data and display the streamlit application. This application allows to filtering the displayed data

**Redbus Data Integration and Streamlit Application**
This project involves fetching data from the Redbus website, storing it in a MySQL database, and creating a Streamlit application to display and filter this data.

**Project Overview**
The goal of this project is to automate the retrieval of bus route information from Redbus, store it in a MySQL database named MDT36, and develop a Streamlit application for users to filter and view this data based on various criteria.

**Components**
**Data Collection and Storage:**

Data is scraped or fetched in real-time from Redbus using web scraping techniques.
The retrieved data includes information such as bus routes, timings, prices, ratings, and seat availability.
This data is stored in a MySQL database named MDT36.

**Streamlit Application:**

A Streamlit web application is developed to visualize and filter the bus route data stored in MySQL.
Users can select a state, route, price range, star rating, and bus type to filter the displayed data.
The application dynamically queries the MySQL database based on user inputs and displays the filtered results.

**Technologies Used**
Python: Programming language used for web scraping, data manipulation, and Streamlit application development.
MySQL: Database management system used for storing and querying bus route data.
Streamlit: Python library used for building interactive web applications for data visualization.

**How to Run**
**To run the Streamlit application:**
**Setup MySQL Database:**
Ensure you have MySQL installed and running.
Create a database named MDT36.
Update db_details in the Python scripts with your MySQL credentials (user, password, host, database).

**Install Python Dependencies:**
pip install selenium
pip install pandas 
pip install streamlit 
pip install mysql-connector-python

**Run the Streamlit Application:**
streamlit run app.py
Replace app.py with the name of your main Streamlit application file.

**Access the Application:**
Open your web browser and go to http://localhost:8501 (or the URL provided by Streamlit).
Select the state, route, price range, star rating, and bus type to filter and view the bus route data.
