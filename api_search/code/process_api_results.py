import os
import json

class Article:
    def __init__(self, article_data, search_id):
        self.id = article_data.get("_id", "")
        self.search_id = search_id
        self.abstract = article_data.get("abstract", "")
        self.lead_paragraph = article_data.get("lead_paragraph", "")
        self.pub_date = article_data.get("pub_date", "")
        self.document_type = article_data.get("document_type", "")
        self.news_desk = article_data.get("news_desk", "")
        self.section_name = article_data.get("section_name", "")
        self.subsection_name = article_data.get("subsection_name", "")
        self.type_of_material = article_data.get("type_of_material", "")
        self.word_count = article_data.get("word_count", 0)

        byline = article_data.get("byline", {})
        self.byline_original = byline.get("original", "")

        headline = article_data.get("headline", {})
        self.headline_main = headline.get("main", "")

    def to_dict(self):
        return {
            "id": self.id,
            "search_id": self.search_id,
            "abstract": self.abstract,
            "lead_paragraph": self.lead_paragraph,
            "pub_date": self.pub_date,
            "document_type": self.document_type,
            "news_desk": self.news_desk,
            "section_name": self.section_name,
            "subsection_name": self.subsection_name,
            "type_of_material": self.type_of_material,
            "word_count": self.word_count,
            "byline_original": self.byline_original,
            "headline_main": self.headline_main
        }

    def build_articles_json(input_dir, output_dir):
        with open('api_search/data/result/books_search_inputs.json', 'r') as input_file:
            input_data = json.load(input_file)

         # List to store all processed articles
        all_articles = []

        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                input_file_path = os.path.join(input_dir, filename)
                with open(input_file_path, 'r') as f:
                    article_data = json.load(f)
                    search_id = filename.split('_')[3].split('.')[0]  # Extract the search ID

                    for item in input_data:
                        #print(item)
                        if item['id'] == search_id:
                            scope = item['scope']
                            searchitem = item['searchitem']
                            break
                    else:
                        # Si aucune correspondance trouvée, définir des valeurs par défaut
                        scope = ''
                        searchitem = ''

                    # List to store processed articles
                    #articles = []

                    for article in article_data.get("response", {}).get("docs", []):
                        article_obj = Article(article, search_id)

                        # Ajout de scope et searchitem dans le dictionnaire de l'article
                        article_dict = article_obj.to_dict()
                        article_dict['scope'] = scope
                        article_dict['searchitem'] = searchitem

                        all_articles.append(article_dict)

                    # Write the articles to an output file
                    output_file_path = os.path.join(output_dir, "books_articles.json")
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        json.dump(all_articles, output_file, ensure_ascii=False)
                        # Ajouter un saut de ligne à la fin
                        output_file.write('\n')
