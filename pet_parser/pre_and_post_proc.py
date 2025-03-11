import csv
from pathlib import Path
import re
import requests

from difflib import SequenceMatcher


def parse_product_name(product_name, use_replace:bool = True):
    """
    Розбиває назву товару на складові: тип товару, бренд, назва, фасування.
    """
    #pattern = r"(?P<type>^[^,]+),(?P<brand>[^\s]+)\s+(?P<name>.+?)\s+(?P<packaging>\d+[лгшкз]*)$"
    #match = re.match(pattern, product_name)
    item_count = ["г", "шт", "уп", "л", "з/бан", "бан"]
    name = product_name.strip()
    name = re.sub(r"\s*\d+$", "", name).strip()
    for i in item_count:
        name = name.replace(i, "")
    name = name.replace("  ", " ").split(" ")
    main_name = " ".join(name[:-1])
    if use_replace:
        main_name = main_name.replace("Клуб 4 Лапи", "Club 4 Paws")
    for i in item_count:
        if i in name[-1]:
            return [main_name, name[-1]]
    else:
        return [main_name, " "]


def get_items(url:str, query:dict = {}, headers:dict = {}):
    r = requests.get(url, params=query, headers=headers)
    # print(r.content, r.request.headers, r.request.url)
    if r.status_code == 403:
        return {}
    return r.json()


def is_similar(name, lookup_name):
    count = SequenceMatcher(None, name, lookup_name).ratio()
    if count >= 0.5:
        return True
    else:
        return False


def get_names():
    input_file = Path(__file__).parent / "test-19.csv" # CSV файл з назвами товарів і штрихкодами
    names = []
    # Читаємо дані з CSV файлу
    with open(input_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            given_name = row['Назва Товару']
            names.append(given_name)
    return names


def write_prices(prices:dict, filename:str):
    output_file = Path(__file__).parent / filename
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for unit in prices:
            for original_name, values in unit.items():
                fetched_name, price, url = values
                writer.writerow([original_name, price, url])
