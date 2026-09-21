import json

def load_bookmarks_file(filename):
    with open(filename, "r", encoding="utf-8") as json_data:
        return json.load(json_data)

def write_to_file(filename, output):
    with open(filename, "w", encoding="utf-8") as out:
        out.write(output)
