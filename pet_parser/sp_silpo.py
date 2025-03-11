from pre_and_post_proc import parse_product_name, get_items, get_names, write_prices


BASE_URL = "https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/quick-search"


def get_query_data(given_name):
    lookup_name, ratio = parse_product_name(given_name)
    return lookup_name, ratio


def get_query_params(lookup_name):
    return {"limit": 5, 
         "search": lookup_name,
         "sortBy": "productsList",
         "sortDirection": "desc"
         }


def analytycs_json(items:dict, ratio:str = ""):
    item = items.get('items', [[]])
    item = item[0] if item != [] else {}
    if item != []:
        if ratio in item.get("displayRatio", ""):
            return item 
        else:
            print("ratio not found!")
            return item
    else:
        # print("not found>", item)
        return {"not found": "not found"}



def get_item_price(item:dict, lookup_name:str):
    name = item.get('title' , "not found")
    # if not is_similar(name, lookup_name):
    #     # raise error here ?
    #     return {lookup_name: ["not found", "not found", "not found"]}
    price = item.get('price', "not found")
    url = item.get('slug', "not found")
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
        item_0 = analytycs_json(items, ratio)
        price = get_item_price(item_0, lookup_name)
        print(price)
        prices.append(price)
    write_prices(prices, "test-silpo.csv")
