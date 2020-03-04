import requests
from selenium import webdriver
import os
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# UA
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"')
# 關閉GPU
chrome_options.add_argument('--disable-gpu')
# 隱藏滾動條
chrome_options.add_argument('--hide-scrollbars')
# 無頭
chrome_options.add_argument("--headless")
# 不加載圖片
# chrome_options.add_argument('blink-settings=imagesEnabled=false')
# 最高權限運行
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# Now you can start using Selenium


def scrapy(search_id):
    # search_id = "FX505DD-0051B3750H"
    # " X571GT-0241K9300H"
    page = "1"
    sort = "sale/dc"
    pchome_params = {'q': search_id, 'page': page, 'sort': sort}
    res = requests.get(
        'https://ecshweb.pchome.com.tw/search/v3.3/all/results', params=pchome_params)

    # url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=UX430UN-0291D8250U&page=1&sort=sale/dc"

    # 1.如果響應狀態碼是200，說明請求成功！
    if res.status_code == 200:
        print("成功請求響應！")
        # json格式
        data = res.json()
        # print(data)
        # 商品資料
        prods = data['prods']
        machines = {}

        for prod in prods:
            # 商品ID
            id = prod['Id']
            # 商品名稱
            name = prod['name']
            # 商品描述
            describe = re.findall(
                r"(?<=買就送|大爆送)[.\s\S\w\W\D\d ]*", prod['describe'])
            # 商品價格
            price = prod['price']

            print("搜尋:" + id)
            driver.implicitly_wait(10)
            driver.get("https://mall.pchome.com.tw/prod/" + id)
            # 前往這個網址
            print("網頁資源:" + driver.page_source)
            gifts = []
            for data in driver.find_elements_by_css_selector("a[class='giftlink']"):
                gifts.append(data.text)

            list_gift = ",".join(gifts)
            print("列印禮物連結:" + list_gift)
            machine = {"name": name, "describe": ",".join(describe),
                       "price": price, "gift": list_gift}
            machines.update({id: machine})
            # print(machine)

        driver.close()
        return machines

    else:
        print("請求失敗！")
        return -1
