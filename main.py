import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import mysql.connector as db
import states_link as states
import datetime
import db_operation as db
import pandas as pd
import os

class RedBus:
    def __init__(self, url, state):
        self.routes_details = []
        self.bus_details = []

        self.get_routes(url)
        print("route", len(self.routes_details))

        for link in self.routes_details:
            self.get_bus_details(state, link['route_link'], link['route_name'])

        print("Before remove duplicate", len(self.bus_details))
        self.bus_details = self.remove_duplicate(state, self.bus_details)
        print("After remove duplicate", len(self.bus_details))

        db.create_table(self.bus_details)

    def remove_duplicate(self, state, data):
        data_frame = pd.DataFrame(data)
        remove_duplicate_data = data_frame.drop_duplicates()

        current_directory = os.getcwd()
        csv_file_name = f'{state}_scarpped_data.csv'
        csv_file_path = os.path.join(current_directory, csv_file_name)
        remove_duplicate_data.to_csv(csv_file_path, index=False)

        current_data = remove_duplicate_data.to_dict('records')
        return current_data

    def get_routes(self, state):
        try:
            driver.get(state)

            current_window_state = driver.execute_script("return document.visibilityState")
            if current_window_state != 'visible':
                driver.maximize_window()

            pagination_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.DC_117_paginationTable .DC_117_pageTabs'))
            )

            for i in range(len(pagination_elements)):
                next_page_element = pagination_elements[i]
                actions = ActionChains(driver)
                actions.move_to_element(next_page_element).click().perform()
                time.sleep(5)

                routes = driver.find_elements(By.CLASS_NAME, 'route')
                for route in routes:
                    route_details = {
                        'route_name': route.text,
                        'route_link': route.get_attribute('href')
                    }
                    self.routes_details.append(route_details)
        except Exception as e:
            print("Error finding the route link", e)

    def get_today_date(self):
        current_date = datetime.date.today()

        day = current_date.day
        month = current_date.strftime("%b")
        date = str(day) + " " + month
        return date

    def get_bus_details(self, state, url, route):
        driver.get(url)
        print("Current Working Route", route)
        current_window_state = driver.execute_script("return document.visibilityState")
        if current_window_state != 'visible':
            driver.maximize_window()

        try:
            date = driver.find_element(By.CLASS_NAME, 'searchDate')
            date_value = date.get_attribute('value')
            print(f"Date on page: {date_value}")
            current_date = self.get_today_date()
            print(f"Current date: {current_date}")

            bus_flag = False
            no_bus = None

            try:
                no_bus = driver.find_element(By.CLASS_NAME, 'oops-wrapper')
            except NoSuchElementException:
                pass

            if no_bus:
                print(f"No buses found for {date_value}. Checking next 3 dates.")
                for i in range(1, 4):
                    move_date = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="fixer"]/div/div/div[1]/span[3]/i'))
                    )
                    move_date.click()
                    time.sleep(2)

                    next_date = driver.find_element(By.CLASS_NAME, 'searchDate')
                    next_date_value = next_date.get_attribute('value')
                    print(f"Date on page: {next_date_value}")

                    try:
                        no_bus = driver.find_element(By.CLASS_NAME, 'oops-wrapper')
                    except NoSuchElementException:
                        no_bus = None

                    if no_bus:
                        print(f"No buses found for {next_date_value}")
                    else:
                        print(f"Buses found for {next_date_value}")
                        date_value = next_date_value
                        bus_flag = True
                        break

                if not bus_flag:
                    print(f"Skipping route {route} because no buses found for any date.")
                    return
            else:
                bus_flag = True

            if bus_flag:
                self.click_view_buses()
                self.scroll_to_bottom()
                self.extract_bus_details(state, url, route, date_value)

        except NoSuchElementException as e:
            print(f"Element not found: {e}")

    def click_view_buses(self):
        try:
            view_buses = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'i.p-left-10.icon.icon-down'))
            )
            view_bus_count = len(view_buses)
            print("Number of Government Buses found:", view_bus_count)

            for index, view_bus in enumerate(view_buses, start=1):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                                          view_bus)
                    time.sleep(1)

                    driver.execute_script("arguments[0].click();", view_bus)
                    print(f"Clicked on View Bus {index}")
                except Exception as e:
                    print(f"Error clicking on view bus {index}: {e}")

        except Exception as e:
            print("Error finding view government bus ", e)

    def extract_bus_details(self, state, url, route, current_date):
        try:
            buses = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.clearfix.bus-item-details')))

            print("Total Buses Found:", len(buses))

            for bus in buses:
                try:
                    travel_name = bus.find_element(By.CSS_SELECTOR, '.travels.lh-24.f-bold.d-color').text.strip()
                except NoSuchElementException:
                    travel_name = 'N/A'

                try:
                    bus_type = bus.find_element(By.CSS_SELECTOR, '.bus-type').text.strip()
                except NoSuchElementException:
                    bus_type = 'N/A'

                try:
                    departing_time = bus.find_element(By.CSS_SELECTOR, '.dp-time').text.strip()
                except NoSuchElementException:
                    departing_time = 'N/A'

                try:
                    duration = bus.find_element(By.CSS_SELECTOR, '.dur').text.strip()
                except NoSuchElementException:
                    duration = 'N/A'

                try:
                    reaching_time = bus.find_element(By.CSS_SELECTOR, '.bp-time').text.strip()
                except NoSuchElementException:
                    reaching_time = 'N/A'

                try:
                    rating_element = bus.find_element(By.CSS_SELECTOR, '.rating-sec .rating span')
                    star_rating = rating_element.text.strip()
                except NoSuchElementException:
                    star_rating = "0"

                try:
                    available_seats = bus.find_element(By.CSS_SELECTOR, '.seat-left').text.strip().split()[0]
                except NoSuchElementException:
                    available_seats = "0"

                try:
                    price = bus.find_element(By.CSS_SELECTOR, '.seat-fare .fare').text.strip()
                except NoSuchElementException:
                    price = 'N/A'

                private_bus_details = {
                    'date': current_date,
                    'state': state,
                    'route': route,
                    'route_link': url,
                    'bus_name': travel_name,
                    'bus_type': bus_type,
                    'departing_time': departing_time,
                    'duration': duration,
                    'reaching_time': reaching_time,
                    'star_rating': star_rating,
                    'available_seats': available_seats,
                    'price': price if 'INR' in price else 'INR ' + price
                }
                print(private_bus_details)
                self.bus_details.append(private_bus_details)
        except Exception as e:
            print("Error finding extracting bus", e)

    def scroll_to_bottom(self):
        scrolling = True
        while scrolling:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

            old_scroll_position = driver.execute_script('return window.pageYOffset;')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            new_scroll_position = driver.execute_script('return window.pageYOffset;')

            if new_scroll_position == old_scroll_position:
                scrolling = False


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    redbus_url = 'https://www.redbus.in/'

    available_state = [
        'Kadamba Transport Corporation Limited (KTCL)',
        'KSRTC (Kerala)',
        'Bihar State Road Transport Corporation (BSRTC)',
        'South Bengal State Transport Corporation (SBSTC)',
        'NORTH BENGAL STATE TRANSPORT CORPORATION',
        'PEPSU (Punjab)',
        'RSRTC',
        'HRTC',
        'UPSRTC',
        'KAAC TRANSPORT',
        'Assam State Transport Corporation (ASTC)'
    ]

    state_info = states.get_states(redbus_url, driver)

    unique_states = {state['state']: state for state in state_info}.values()
    state_info = list(unique_states)
    available_state_set = set(available_state)

    for state in state_info:
        for state_name in available_state_set:
            if state_name in state['state']:
                if 'Kadamba' in state_name:
                    state_name = 'Kadamba'
                elif 'KSRTC' in state_name:
                    state_name = 'Kerala'
                elif 'Bihar' in state_name:
                    state_name = 'Bihar'
                elif 'South Bengal' in state_name:
                    state_name = 'South Bengal'
                elif 'NORTH BENGAL' in state_name:
                    state_name = 'North Bengal'
                elif 'PEPSU (Punjab)' in state_name:
                    state_name = 'Punjab'
                elif 'RSRTC' in state_name:
                    state_name = 'Rajasthan'
                elif 'HRTC' in state_name:
                    state_name = 'Himachal'
                elif 'UPSRTC' in state_name:
                    state_name = 'Uttar Pradesh'
                elif 'KAAC' in state_name:
                    state_name = 'Karbi'
                elif 'Assam' in state_name:
                    state_name = 'Assam'
                print(f"State: {state_name}, Link: {state['state_link']}")
                x = RedBus(state['state_link'], state_name)
