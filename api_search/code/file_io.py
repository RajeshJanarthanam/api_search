import json
import os
import shutil
import time

def read_keywords_from_file(file_path):
    """
    Lit les mots-clés de recherche à partir d'un fichier texte et les renvoie sous forme de liste.
    """
    keywords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            keywords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'existe pas.")
    return keywords


def write_json_to_file(data, file_path):
    """
    Écrit des données JSON dans un fichier.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Données écrites dans {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans {file_path}: {str(e)}")

def delete_files_in_directories(directories):
    """
    Supprime tous les fichiers d'un répertoire.
    """

    for directory in directories:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'Deleted {file_path}')
            except Exception as e:
                print(f'Failed to delete {file_path}: {e}')

def copy_files_for_logstash(source_dir, target_dir):
    """
    copie les fichiers json dans les répertoires dédiés pour logstash
    """
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        shutil.copy(source_file, target_file)
        time.sleep(1)
        print(f'Copied {source_file} to {target_file}')

def read_files_and_create_json(input_path, output_path):
    """
    Lie le contenu d'un fichier en entrée et crée des fichiers json en sortie
    """
    books_search_list = []
    timeswire_search_list = []

    for filename in os.listdir(input_path):
        if filename.startswith('books_search'):
            with open(os.path.join(input_path, filename), 'r') as file:
                content = json.load(file)
                books_search_list.append(content)
        elif filename.startswith('timeswire_search'):
            with open(os.path.join(input_path, filename), 'r') as file:
                content = json.load(file)
                timeswire_search_list.append(content)

    # Écriture des fichiers JSON pour les deux tables
    with open(os.path.join(output_path, 'books_search_list.json'), 'w') as output_file:
        json.dump(books_search_list, output_file)
        output_file.write('\n')  # Ajout d'un saut de ligne à la fin

    with open(os.path.join(output_path, 'timeswire_search_list.json'), 'w') as output_file:
        json.dump(timeswire_search_list, output_file)
        output_file.write('\n')  # Ajout d'un saut de ligne à la fin

def document_directory(directory_path, indent=0):
    """
    Pour des besoins de documentation affiche l'arborescence d'un repertoire avec des identations
    """
    # Obtenir le nom du répertoire actuel
    base_name = os.path.basename(directory_path)

    # Afficher le nom du répertoire avec l'indentation appropriée
    print(' ' * indent + '- ' + base_name + '/')

    # Parcourir les fichiers et sous-répertoires
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            # Si c'est un répertoire, appeler récursivement la fonction pour ce répertoire
            document_directory(item_path, indent + 2)
        else:
            # Si c'est un fichier, afficher le nom du fichier avec l'indentation appropriée
            print(' ' * (indent + 2) + '- ' + item)