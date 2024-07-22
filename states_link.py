from selenium.webdriver.common.by import By

state_info = []

def get_states(url, driver):
    driver.get(url)
    buses = driver.find_element(By.XPATH, '//*[@id="homeV2-root"]/div[3]/div[1]/div[2]/a')
    buses_link = buses.get_attribute('href')
    print("Buses link:", buses_link)
    states_details = get_state_website(buses_link,driver)
    return states_details

def get_state_website(url,driver):
    driver.get(url)
    states = driver.find_elements(By.CLASS_NAME, 'D113_link')
    for state in states:
        state_details = {
            'state': state.text,
            'state_link': state.get_attribute('href')
        }
        state_info.append(state_details)
    return state_info
