from datetime import datetime
from pre_and_post_proc import parse_product_name, get_items, get_names, write_prices


BASE_URL = "https://api.multisearch.io/"


def get_query_data(given_name):
    lookup_name, ratio = parse_product_name(given_name, False)
    return lookup_name, ratio


def get_query_params(lookup_name):
    return {"id": 11790,
            "lang": "uk",
            "q": "lhsine",
            #"m": str(int(datetime.timestamp(datetime.now())))+"225",
            "query": lookup_name,
            "s": "large",
            "uid": "281f2da8-8bb8-4cf5-81c4-1f1c1413c812",
        }


def analytycs_json(items:dict, ratio:str = ""):
    try:
        item = items.get('results', {})
        item = item.get("item_groups", [])
        if len(item):
            item = item[0].get('items', [[]])
    except AttributeError:
        return {"not found": "not found"}
    item = item[0] if item != [] else {}
    if item != [] :
        # print("!!>", item)
        return item[0] if isinstance(item, list) else item
    else:
        # print("not found>", item)
        return {"not found": "not found"}


def get_item_price(item:dict, lookup_name:str):
    name = item.get('name' , "not found")
    price = item.get('price', "not found")
    url = item.get('url', "not found")
    if "?q=" in url:
        url = url[:url.find("?q=")]
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
        #print(lookup_name, query, ratio)
        url = "https://masterzoo.ua"
        headers = {"Origin": url,
                   "Referer": url,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
                   }
        items = get_items(BASE_URL, query, headers)
        print(items)
        item_0 = analytycs_json(items, ratio)
        price = get_item_price(item_0, lookup_name)
        print(price)
        prices.append(price)
    write_prices(prices, "test-master-zoo.csv")