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
            writer.write(
                f"Параметр event({event}) содержит пробелы, уберите их.")
        event = event.replace(" ", "")

        schema = get_right_schema(event, writer)
        if schema is None:
            continue

        if check_required(schema, json_data["data"], "data", writer) == -1:
            continue

        for key, item in json_data["data"].items():
            if item is None:
                continue

            if type(item) is list:
                if not item:
                    writer.write(f"Список {key} пуст.")
                for i in item:
                    if type(i) is dict:
                        try:
                            check_required(
                                schema["properties"][key]["items"], i, key, writer)
                            for k, ii, in i.items():
                                check_type(
                                    k, ii, schema["properties"][key]["items"], writer)
                        except KeyError:
                            pass

            check_type(key, item, schema, writer)

    writer.close()


def check_required(schema, json_data, obj, writer):
    for item in schema["required"]:
        if json_data is None:
            writer.write("Параметр data пуст, пожалуйста проверьте его.")
            return -1

        if item not in json_data.keys():
            writer.write(
                f"Не хватает зависимости {item}, пожалуйста добавте {item} в {obj}.")


def check_type(key, json_item, schema, writer):
    try:
        right_type = schema["properties"][key]["type"]

        item_type = type(json_item)

        if type(right_type) is list:
            for t in right_type:
                check_result = convert_checker(t, item_type)
        else:
            check_result = convert_checker(right_type, item_type)

        if not check_result:
            writer.write(
                f"Параметр {key} типа {item_type}, хотя ожидалось {right_type}.")
    except KeyError:
        # writer.write(f"{key} является лишним, избавтесь от него.")
        return


def convert_checker(right_type, item_type):
    if right_type == "string":
        return True if item_type is str else False
    elif right_type == "integer" or right_type == "number":
        return True if item_type is int or item_type is float else False
    elif right_type == "array":
        return True if item_type is list else False
    elif right_type == "object":
        return True if item_type is dict else False
    elif right_type == "null":
        return True if item_type is type(None) else False
    elif right_type == "boolean":
        return True if item_type is bool else False
    return


def get_right_schema(event, writer):
    if event.find("label") != -1:
        if event != "label_selected":
            writer.write(
                "Пожалуйста исправте параметр event на label_selected")

        schema = get_schema("schema/label_selected.schema")
    elif event.find("sleep") != -1:
        if event != "sleep_created":
            writer.write("Пожалуйста исправте параметр event на sleep_created")

        schema = get_schema("schema/sleep_created.schema")
    elif event.find("meditation") != -1:
        if event != "meditation_created":
            writer.write(
                "Пожалуйста исправте параметр event на meditation_created")

        schema = get_schema("schema/workout_created.schema")
    elif event.find("cmarker") != -1:
        if event != "cmarker_created":
            writer.write(
                "Пожалуйста исправте параметр event на cmarker_created")

        schema = get_schema("schema/cmarker_created.schema")
    else:
        print("Нужной схемы не было найдено.")
        schema = None

    return schema


def get_schema(file_name):
    with open(file_name, 'r') as schema_file:
        return json.load(schema_file)


if __name__ == "__main__":
    main()
