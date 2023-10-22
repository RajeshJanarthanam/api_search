import os
from dotenv import load_dotenv
from api_search.code.file_io import delete_files_in_directories, copy_files_for_logstash
from api_search.code.process_input_items import SearchItem  
from api_search.code.get_data_from_api import NYAPISearch
from api_search.code.process_api_results import Article  

if __name__ == "__main__":
    load_dotenv()

    directories = ['api_search/data/result','api_search/data/result/from_api_search','api_search/data/result/for_elk','elasticsearch/logstash_ingest_data']
    delete_files_in_directories(directories)

    # Récupérer les chemins des fichiers depuis les variables d'environnement
    input_filename = os.getenv('INPUT_FILENAME')
    output_dir = os.getenv('OUTPUT_DIR')
    

    # Portée des recherches
    scope = 'books'

    # 1. préparation des éléments de recherche
    SearchItem.build_search_items_json(input_filename, scope, output_dir)

    # 2. Recherche des articles dans NY API Search et sortie JSON
    api_key = os.getenv('API_KEY')
    input_file = 'api_search/data/result/books_search_inputs.json'
    output_dir_api = 'api_search/data/result/from_api_search'  
    
    ny_api = NYAPISearch(api_key)
    ny_api.fetch_articles(input_file, output_dir_api)

    # 3. traitement des données de l'API search
    input_dir_api_results = output_dir_api
    output_dir_processed = 'api_search/data/result/for_elk'
    Article.build_articles_json(input_dir_api_results, output_dir_processed)

    # 4. Dépôt des fichiers json pour logstash qui va le transférer dans ELK

    source_data_directory = "api_search/data/result/for_elk"
    target_data_directory = "elasticsearch/logstash_ingest_data"
    
    copy_files_for_logstash(source_data_directory, target_data_directory)