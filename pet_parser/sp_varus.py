from pre_and_post_proc import parse_product_name, get_items, get_names, write_prices


BASE_URL = "https://api.multisearch.io/"


def get_query_data(given_name):
    lookup_name, ratio = parse_product_name(given_name, use_replace=False)
    return lookup_name, ratio


def get_query_params(lookup_name):
    return {"id": 12138,
         "query": lookup_name,
         "uid": "guest",
         "lang": "uk",
         "autocomplete": "true"
        }


def analytycs_json(items:dict, ratio:str = ""):
    item = items.get('results', {}).get('items', [[]])
    item = item[0] if item != [] else {}
    # print(item)
    if item != []:
        return item
    else:
        # print("not found>", item)
        return {"not found": "not found"}


def get_item_price(item:dict, lookup_name:str):
    name = item.get('name' , "not found")
    price = item.get('price', "not found")
    url = item.get('url', "not found")
    if "?search=" in url:
        url = url[:url.find("?search=")]
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
        # print(lookup_name, query, ratio)
        items = get_items(BASE_URL, query)
        # print(items)
        item_0 = analytycs_json(items, ratio)
        price = get_item_price(item_0, lookup_name)
        print(price)
        prices.append(price)
    write_prices(prices, "test-varus.csv")