import time
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict

def parse_info(driver):
    try:
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        base = bs.find('div', {'id':'app'})
        plane = base.find('div', {'class':'plane'}).get_text()
        depart = base.find('div', {'class':'depart-box'})
        arrive = base.find('div', {'class':'arrive-box'})
        depart_time = depart.find('div', {'class':'time'}).get_text()
        depart_loc = depart.find('div', {'class':'airport'}).get_text()
        arrive_time = arrive.find('div', {'class':'time'}).get_text()
        arrive_loc = arrive.find('div', {'class':'airport'}).get_text()
        trans = base.find('div', {'class':'arrow-box'}).get_text()
        price = base.find('div', {'class':'price-box'}).get_text()
        ret = (plane, depart_time, depart_loc, arrive_loc, arrive_time, trans, price)
        return ret
    except AttributeError:
        return None

def get_info(url, driver=None):
    """
    "return plane, depart_time, depart_loc, arrive_loc, arrive_time, trans, price" in turn
    """
    if driver is None:
        driver = webdriver.Chrome()
    for _ in range(5):
        driver.get(url)
        time.sleep(4)
        try:
            ele = driver.find_element_by_xpath("//div[@class='sort-box']/span[7]")
            ele.click()
        except:
            continue
        # time.sleep(2)
        info = parse_info(driver)
        if info is not None:
            # print(info)
            break
    else:
        raise KeyError
    return info

if __name__ == "__main__":
    print(get_info('https://flights.ctrip.com/international/search/oneway-ctu-yto?depdate=2019-08-15&cabin=y_s&adult=1&child=0&infant=0&containstax=1'))