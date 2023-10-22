import os
import requests
import json
import time

class NYAPISearch:
    def __init__(self, api_key):
        self.base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
        self.api_key = api_key

    def fetch_articles(self, input_file_path, output_dir):

        with open(input_file_path, 'r') as f:
            searchitem_list = json.load(f)

        count = 0
        for searchitem_data in searchitem_list:                
            # Obtient l'ID du mot-clé à partir du fichier JSON
            searchitem_id = searchitem_data.get('id', '')  
            #print(searchitem_id)
            # Obtient l'ID du mot-clé à partir du fichier JSON
            searchitem_scope = searchitem_data.get('scope', '')  
            #print(searchitem_id)                            
            # Récupère le mot-clé à rechercher                
            searchitem_text = searchitem_data.get('searchitem', '')
            #print('Check:',searchitem_text)

            # Remplace l'espace par '%20' dans le mot-clé si nécessaire
            searchitem_text = searchitem_text.replace(" ", "%20")
            #print(searchitem_text)
            
            # Effectue la requête API en utilisant le mot-clé
            api_url = f"{self.base_url}q={searchitem_text}&api-key={self.api_key}"
            #print(api_url)
            if count==5:
                time.sleep(60)
                count = 0

            page = requests.get(api_url)
            response = page.json()

            count+=1
            # Enregistre les résultats de la recherche dans un fichier de sortie
            output_filename = f"{searchitem_scope}_api_response_{searchitem_id}.json"
            output_file_path = os.path.join(output_dir, output_filename)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(response, output_file, ensure_ascii=False, indent=4)
