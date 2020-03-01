import requests
from selenium import webdriver


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
            describe = prod['describe']
            # 商品價格
            price = prod['price']

            with webdriver.Chrome('./chromedriver') as driver:
                # with webdriver.Chrome('chromedriver.exe') as driver:
                driver.get("https://mall.pchome.com.tw/prod/" + id)  # 前往這個網址
                gifts = []
                for data in driver.find_elements_by_css_selector("a[class='giftlink']"):
                    gifts.append(data.text)

            machine = {"name": name, "describe": describe,
                       "price": price, "gift": ",".join(gifts)}
            machines.update({id: machine})
            # print(machine)
        return machines

    else:
        print("請求失敗！")
        return ("請求失敗！")
