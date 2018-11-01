#! /usr/bin/env python
#
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common import exceptions

import datetime, json, time, re, sys


class UdiDriver(object):
    def __init__(self, conf):
        self.conf = conf
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(0)
        
    def run(self):
        driver = self.driver
        driver.get("https://selfservice.udi.no/?epslanguage=en-GB")
        driver.find_element_by_id(
            "ctl00_BodyRegion_PageRegion_MainRegion_ctl00_heading").click()
        username_elt = driver.find_element_by_id(
            "ctl00_BodyRegion_LoginResponiveBox_txtUsername")
        username_elt.clear()
        username_elt.send_keys(self.conf["username"])
        password_elt = driver.find_element_by_id("ctl00_BodyRegion_LoginResponiveBox_txtPassword")
        password_elt.clear()
        password_elt.send_keys(self.conf["password"])
        driver.find_element_by_id(
            "ctl00_BodyRegion_LoginResponiveBox_btnLocalLogin").click()
        driver.find_element_by_id("ctl00_BodyRegion_PageRegion_MainRegion_IconNavigationTile2_heading").click()
        driver.find_element_by_id("ctl00_BodyRegion_PageRegion_MainRegion_ApplicationOverview_applicationOverviewListView_ctrl0_btnBookAppointment").click()
        driver.find_element_by_id("ctl00_PageRegion_MainContentRegion_ViewControl_spnReceiptAndBooking_BookingSummaryInfo_btnChangeBooking").click()
    
        # We should be on the calendar page. Check this.
        try:
            driver.find_element_by_id("ctl00_BodyRegion_PageRegion_MainRegion_appointmentReservation_bookingHeader_lblTitle")
            # print("We're at the calendar page!")
        except exceptions.NoSuchElementException:
            print('Not on the calendar page! Bombing out after a minute!')
            time.sleep(60)
            return False

        # Keep looking for an open appointment till we find one.
        while True:
            try:
                first_apt = driver.find_element_by_xpath("//td[@class='bookingCalendarBookedDay' or @class='bookingCalendarHalfBookedDay']/span[@class='dayNumber']")
                day = int(first_apt.text)
                month_year = driver.find_element_by_xpath('//*[@id="ctl00_BodyRegion_PageRegion_MainRegion_appointmentReservation_appointmentCalendar_pnlCalendarTop"]/div/div[3]/h2').text
                found_date = datetime.datetime.strptime("%d %s" % (day, month_year), "%d %B %Y")
                print found_date.strftime("%Y-%m-%d")
                return found_date < self.conf["wait_if_earlier_than"]
            except exceptions.NoSuchElementException:
                print 'No appointment found: moving on'
                driver.find_element_by_id('ctl00_BodyRegion_PageRegion_MainRegion_appointmentReservation_appointmentCalendar_btnNext').click()


    def __del__(self):
        self.driver.quit()


def main(driver=None, cfg_file=None):
    if not driver:
        driver = UdiDriver
    if not cfg_file:
        cfg_file = open(sys.argv[1])
    with cfg_file as fd:
        config = json.load(fd)
    latest = datetime.datetime.strptime(
        config["wait_if_earlier_than"], "%Y-%m-%d")
    config["wait_if_earlier_than"] = latest
    u = driver(config)
    found_better_appt = u.run()
    if found_better_appt:
        time.sleep(3600)  # Wait for the user to book it
        sys.exit(0)
    else:
        sys.exit(255)


if __name__ == "__main__":
    main()
