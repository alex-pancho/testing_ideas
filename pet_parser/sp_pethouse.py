import requests
from lxml import html
from pre_and_post_proc import parse_product_name,  get_names, write_prices


BASE_URL = "https://pethouse.ua/ua/api/searchengine/"


def get_query_data(given_name):
    lookup_name, ratio = parse_product_name(given_name)
    return lookup_name, ratio

def get_items(url:str, query:dict = {}):
    r = requests.post(url, data=query)
    # print(r.content, r.request.headers, r.request.url)
    if r.status_code == 403:
        return {}
    return r.text

def get_query_params(lookup_name):
    lookup_name = "+".join(lookup_name.split())
    return {"search_value": lookup_name
         }


def analytycs_html(items:str):

    tree = html.fromstring(items)
    # Витягування посилання
    link = tree.xpath("//a/@href")
    url = link[0] if link else "not found"
    # Витягування тексту з class="itm-price"
    name = tree.xpath("//span[@class='itm-name']/text()")
    name = str(name[0]).encode("utf-8").decode("utf-8").strip() if name else "not found"
    price = tree.xpath("//span[@class='itm-price']/text()")
    if price:
        pre_price = price[0].replace("Ціна від ", "").replace(" грн", "").replace("Ціна  ", "").replace(",", ".").strip()
        price = float(pre_price)
    else:
        price = "not found"
    return {"name":name, "price":price, "url": url}


def get_item_price(item:dict, lookup_name:str):
    name = item.get('name' , "not found")
    price = item.get('price', "not found")
    url = item.get('url', "not found")
    return {lookup_name: [name, price, url]}


def crawl_by_name(given_name:str = ""):
    lookup_name, ratio = get_query_data(given_name)
    query = get_query_params(lookup_name)
    return lookup_name, query, ratio


if __name__ == "__main__":
    names = get_names()
    prices = []
    for given_name in names:
        lookup_name, query, ratio = crawl_by_name(given_name)
        items = get_items(BASE_URL, query)
        #print(items)
        item_0 = analytycs_html(items)
        price = get_item_price(item_0, lookup_name)
        print(price)
        prices.append(price)
    write_prices(prices, "test-pethouse.csv")
