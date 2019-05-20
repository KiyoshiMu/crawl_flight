import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sim_driver import get_info
import json
from log_parse import parse_log

start_date = datetime.date(2019, 7, 20)
end_date = datetime.date(2019, 9, 1)
step = datetime.timedelta(days=1)

def day_range(start_date, end_date, step):
    while start_date <= end_date:
        yield start_date
        start_date += step

def make_url(date_isoformat, route='oneway-ctu-yto', people=1):
    url = "\
https://flights.ctrip.com/international/search/\
{}?depdate={}&cabin=y_s&adult={}\
&child=0&infant=0&containstax=1\
".format(route, date_isoformat, people)
    return url

def base_writer(info_dict):
    with open('temp.txt', 'a', encoding='utf-8') as writer:
        writer.write(str(info_dict))
        writer.write('\n')

def collect(driver, route='oneway-ctu-yto'):
    recode = {}
    for date in day_range(start_date, end_date, step):
        date_isoformat = date.isoformat()
        url = make_url(date_isoformat, route=route)
        try:
            recode[date_isoformat] = get_info(url, driver=driver)
        except KeyError:
            break
    return recode

def gen_airport():
    with open('airport.json', 'r') as port:
        iatas = json.load(port).values()
    for iata in iatas:
        yield iata.lower()

def txt_log(line):
    with open('log.txt', 'a') as log:
        log.write(f'{datetime.datetime.now()} {line}\n')

if __name__ == "__main__":
    driverOption = Options()
    driverOption.add_argument('blink-settings=imagesEnabled=false')
    
    driver = webdriver.Chrome(options=driverOption)
    dones = parse_log()
    print(dones)
    for airport in gen_airport():
        if airport in dones:
            continue
        route = f'oneway-{airport}-yto'
        
        recode = collect(driver, route=route)
        if len(recode) == 0:
            txt_log(f'{airport} nothing')
            continue
        base_writer(recode)
        txt_log(f'{airport} done')
    driver.close()