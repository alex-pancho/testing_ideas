import pandas as pd
from pathlib import Path
import logging
import xml.etree.ElementTree as ET
import json
import os

file_csv_1 = "work_with_csv/random.csv"
file_csv_2 = "work_with_csv/r-m-c.csv"
result_file = "Lesson_13/result_karnaukh.csv"

df1=pd.read_csv(file_csv_1)
df2=pd.read_csv(file_csv_2)

df_combined = pd.concat([df1, df2])
df_cleaned = df_combined.drop_duplicates()

df_cleaned.to_csv(result_file, index=False)
print(f"Файл збережено як {result_file}")



folder_with_json = "work_with_json"
log_file_json = "Lesson_13/json_karnaukh.log" 
with open(log_file_json, "w") as log:
    for file_name in os.listdir(folder_with_json):
        file_path = os.path.join(folder_with_json, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f) 
            print(f"{file_name} - Валідний JSON")
        except json.JSONDecodeError as e:
            log.write(f"Помилка в файлі {file_name}: {e}\n")
            print(f"{file_name} - Не валідний JSON, помилка записана в Лог")
print(f"Лог збережено в {log_file_json}")




logging.basicConfig(
    filename = "Lesson_13/xml_karnaukh.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    encoding = "utf-8"
)
def find_incoming(file_path, group_number):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for group in root.findall('group'):
        number = group.find('number')
        if number is not None and number.text == group_number:
            incoming = group.find("timingExbytes/incoming")
            if incoming is not None:
                logging.info(f"Incoming: {incoming.text}")
                return incoming.text
    logging.info("Group not found")

file_path = "work_with_xml/groups.xml"
group_number = '2'
find_incoming(file_path, group_number)
print(f"Лог збережено в Lesson_13/xml_karnaukh.log")
