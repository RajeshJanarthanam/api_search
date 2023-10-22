import json
from datetime import datetime
import os

class SearchItem:
    def __init__(self, searchitem, scope, line_number):        
        self.scope = scope
        self.searchitem = searchitem
        self.line_number = line_number
        self.id = self.generate_unique_id()

    def generate_unique_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = None
        
        if self.scope == 'books':
            unique_id = f"bks{timestamp}{self.line_number}"
        elif self.scope == 'timeswire':
            unique_id = f"twr{timestamp}{self.line_number}"
        return unique_id

    def to_json(self):
        return {"id": self.id, "scope": self.scope, "searchitem": self.searchitem}

    def create_json_file(self, output_dir):
        output_file_path = os.path.join(output_dir, f"{self.scope}_search_{self.id}.json")
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(self.to_json(), json_file, ensure_ascii=False)

    def read_input_from_file(file_path):
        inputs = []
        with open(file_path, 'r') as file:
            for line in file:
                inputs.append(line.strip())
        return inputs

    # def build_search_items_json(input_filename, scope, output_dir):
    #     # Lecture des mots-clés à partir du fichier
    #     search_items = SearchItem.read_input_from_file(input_filename)

    #     for line_number, item_text in enumerate(search_items, start=1):
    #         search_item = SearchItem(item_text, scope, line_number)
    #         search_item.create_json_file(output_dir)

    def build_search_items_json(input_filename, scope, output_dir):
        search_items = SearchItem.read_input_from_file(input_filename)

        # Liste pour stocker les résultats
        results = []

        for line_number, item_text in enumerate(search_items, start=1):
            search_item = SearchItem(item_text, scope, line_number)
            results.append(search_item.to_json())

        # Écrire la liste complète dans un seul fichier JSON
        output_file_path = os.path.join(output_dir, f"{scope}_search_inputs.json")
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False)
