create database REDBUS;
use REDBUS;
show tables;
select * from bus_routes;
SELECT state, count(state) as count FROM bus_routes GROUP BY state ORDER BY state ASC;
SELECT route_name from bus_routes where state='Assam';
SELECT route_name from bus_routes where state='Kerala';
SELECT route_name from bus_routes where state='Karbi';
SELECT * FROM bus_routes WHERE state = "Kerala" and route_name = "Bangalore to Kozhikode";
SELECT * FROM bus_routes WHERE state = "Kerala" and route_name = "Bangalore to Kozhikode" AND price >= 1000;
SELECT * FROM bus_routes WHERE state = "Kerala" and route_name = "Bangalore to Kozhikode" AND price BETWEEN 400 AND 600 AND star_rating >= 4.0;
SELECT * FROM bus_routes WHERE state = "Karbi" and route_name = "Guwahati to Diphu" AND (bus_type LIKE "%AC%" OR bus_type LIKE "%A/C%");
SELECT * FROM bus_routes WHERE state = "Assam" and route_name = "Jorhat to North Lakhimpur" AND (bus_type LIKE "%Seater%");
SELECT * FROM bus_routes WHERE state = "Kadamba" and route_name = "Pune to Goa" AND (bus_type LIKE "%NON AC%" OR bus_type LIKE "%Non A/C%");
SELECT * FROM bus_routes WHERE state = "Himachal" and route_name = "Manali to Delhi" AND (bus_type LIKE "%Sleeper%");
SELECT * FROM bus_routes WHERE state = "Kerala" and route_name = "Bangalore to Kozhikode" AND star_rating >= 4.0;

