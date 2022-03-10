import os
import pathlib
import glob


# POUR INTERAGIR AVEC LE SYSTEME

# Fonction pour changer de répertoire au lancement
def change_directory(directory):
    os.chdir(directory)
    return True


def print_directory():
    print(os.getcwd())


def check_directory():
    user_directory = input("Entrez le chemin du dossier: ")
    while not os.path.exists(user_directory) and not os.path.isdir(user_directory):
        print("Le chemin d'accès au dossier n'existe pas ou est incorrect!\n")
        user_directory = input("Entrez le chemin du dossier: ")
    else:
        return user_directory


def get_files(directory):
    all_files = []  # TABLEAU DE TOUS LES FICHIERS DANS LE REPERTOIRE
    extensions = ['php', 'html', 'css', 'js', 'txt']  # LISTE DES EXTENSIONS

    for ext in extensions:
        fileExt_ = r"**\*.{}"
        fileExt = fileExt_.format(ext)
        lalist = list(pathlib.Path(directory).glob(fileExt))
        for file in lalist:
            all_files.append(file)

    print(all_files)

dir__ = check_directory()  # RECEVOIR L'ENTREE ET LE VERIFIER
changed = change_directory(dir__)  # CHANGEMENT DU REPERTOIRE
if changed:
    print('Dossier changé!\n')
    print_directory()
    get_files(dir__)
    # filesList = [f for f in os.listdir(dir__) if os.path.isfile(os.path.join(dir__, f))]
    '''for path, subdirs, files in os.walk(dir__):
        for name in files:
            print(os.path.join(path, name))'''
    #fileExt = r".txt .php .html"
    #filesList = [f for f in os.listdir(dir__) if f.endswith(fileExt)]
    #print(filesList)
