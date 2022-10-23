import datetime

import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriver:

    """Created Singleton for Selenium WebDriver"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.driver = webdriver.Chrome("/home/igor/chromedriver")


def cookies_click(new_driver) -> None:

    """This function click cookies and click button
    "new search" when response start page"""

    try:
        cookies = new_driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies.click()
        time.sleep(0.2)

        new_search = new_driver.find_element(By.CLASS_NAME, "ts-session-expire--link")
        new_search.click()
        time.sleep(0.2)

    except selenium.common.exceptions.NoSuchElementException:
        pass


def parse_one_flight_tickets(new_driver):

    """Get one ticket for list tickets"""

    times = new_driver.find_element(By.CLASS_NAME, "ts-fip__fie").text.split("\n")[4]
    price = new_driver.find_element(By.CLASS_NAME, "ts-ifl-row__footer-price").text
    print({"flight time": times, "flight cost": price})


def refactored_date_fly(date: list) -> str:

    """Change the month in the date according to the calendar"""

    date[1] = str(int(date[1]) - 1)
    return "-".join(date)


def get_date_from_calendar(departure_date: str, new_driver) -> None:

    """Set date fly in calendar"""

    departure_date_list = departure_date.split("-")
    date_int = datetime.datetime(
        int(departure_date_list[-1]),
        int(departure_date_list[1]),
        int(departure_date_list[0])
    )
    month_year = " ".join(date_int.strftime("%d %B %Y").split()[1:])

    calendar = new_driver.find_element(By.CSS_SELECTOR, "#ctl00_c_CtWNW_dvDepartDate > label")

    for _ in range(7):
        calendar.click()

    month_first = new_driver.find_element(By.CSS_SELECTOR, "#monthLeft")
    month_second = new_driver.find_element(By.CSS_SELECTOR, "#monthRight")
    next_month = new_driver.find_element(By.CSS_SELECTOR, "#nextMonth")

    while True:
        if month_first.text == month_year or month_second == month_year:
            new_driver.find_element(By.ID, f"day-{refactored_date_fly(departure_date_list)}").click()
            break
        else:
            next_month.click()
            time.sleep(0.2)
    pass


def flight_selection(
        new_driver,
        point_of_departure: str,
        point_of_arrival: str,
        departure_date: str) -> list:

    """Set place of departure, place of arrival,
    departure date in form on page, and get list tickets"""

    new_driver.get("https://fly2.emirates.com/CAB/IBE/SearchAvailability.aspx")
    time.sleep(0.3)

    cookies_click(new_driver)
    time.sleep(0.3)

    one_way = new_driver.find_element(By.ID, "dvRadioOneway")
    one_way.click()

    start = new_driver.find_element(By.ID, "ctl00_c_CtWNW_ddlFrom-suggest")
    start.click()
    start.send_keys(point_of_departure)

    end = new_driver.find_element(By.ID, "ctl00_c_CtWNW_ddlTo-suggest")
    end.click()
    end.send_keys(point_of_arrival)

    get_date_from_calendar(departure_date, new_driver)

    button_search = new_driver.find_element(By.ID, "ctl00_c_IBE_PB_FF")
    button_search.click()

    if new_driver.find_elements(By.CSS_SELECTOR, "#ctl00_c_errorPnl"):
        print(new_driver.find_element(By.CSS_SELECTOR, "#ctl00_c_errorPnl").text.split("\n")[1])

    tickets = new_driver.find_elements(By.CLASS_NAME, "ts-ifl-row")

    return [parse_one_flight_tickets(ticket) for ticket in tickets]


def searches_for_flights(new_driver) -> list:

    """User inputs the start city, destination city,
    day departure and receives list tickets"""

    point_of_departure = input("Enter the point of departure(ex. East London (ELS), London (LON)): ")
    point_of_arrival = input("Enter the point of arrival( ex. Colima Airport (CLQ), Santander (SDR)): ")
    departure_date = input("Enter the departure date(e.g. 2-12-2022): ")

    return flight_selection(new_driver,
                            point_of_departure,
                            point_of_arrival,
                            departure_date
                            )


def get_all_result():

    """Create webdriver and does parsing
    the page data and returns the required result"""

    with WebDriver().driver as new_driver:
        searches_for_flights(new_driver)


if __name__ == "__main__":
    get_all_result()

