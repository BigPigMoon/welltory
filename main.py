import json
import os

from writer import Writer


def main():
    writer = Writer("output.txt")
    
    for file_path in os.listdir("event"):
        with open("event/" + file_path, 'r', encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            writer.new_test_file(file_path)
        
        if json_data is None or json_data == {}:
            writer.write("Файл пустой")
            continue
        
        event = json_data["event"]
        
        if event.find(" ", 0, -1) != -1:
            writer.write(f"Параметр event({event}) содержит пробелы, уберите их.")
        event = event.replace(" ", "")
        
        if event.find("label") != -1:
            if event != "label_selected":
                writer.write("Пожалуйста исправте параметр event на label_selected")
            
            schema = get_schema("schema/label_selected.schema")
            
        elif event.find("sleep") != -1:
            if event != "sleep_created":
                writer.write("Пожалуйста исправте параметр event на sleep_created")
            
            schema = get_schema("schema/sleep_created.schema")
            
        elif event.find("meditation") != -1:
            if event != "meditation_created":
                writer.write("Пожалуйста исправте параметр event на meditation_created")
            
            schema = get_schema("schema/workout_created.schema")
        
        elif event.find("cmarker") != -1:
            if event != "cmarker_created":
                writer.write("Пожалуйста исправте параметр event на cmarker_created")
            
            schema = get_schema("schema/cmarker_created.schema")
        
        else:
            print("Нужной схемы не было найдено.")
            continue
        
        check_required(schema, json_data, writer)
        
    writer.close()


def get_schema(file_name):
    with open(file_name, 'r') as schema_file:
        return json.load(schema_file)


def check_required(schema, json_data, writer):
    for item in schema["required"]:
        if json_data["data"] is None:
            writer.write("Параметр data пуст, пожалуйста проверьте его.")
            break
        
        if item not in json_data["data"].keys():
            writer.write(f"Не хватает зависимости {item}, пожалуйста добавте {item} в data.")


if __name__ == "__main__":
    main()