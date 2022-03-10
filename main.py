import os
from os import stat
import pathlib
import glob
from stat import ST_MTIME
from time import localtime, asctime


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


# RECUPERE LES FICHIERS DANS LE DOSSIER
def get_files(directory):
    all_files = []  # TABLEAU DE TOUS LES FICHIERS DANS LE REPERTOIRE
    extensions = ['php', 'html', 'css', 'js', 'txt']  # LISTE DES EXTENSIONS

    for ext in extensions:
        fileExt_ = r"**\*.{}"
        fileExt = fileExt_.format(ext)
        lalist = [str(f) for f in pathlib.Path(directory).glob(fileExt)]
        # RECHERCHE DANS LES DOSSIERS ET SOUS DOSSIERS PAR EXTENSION
        for file in lalist:
            all_files.append(file)

    return all_files


dir__ = check_directory()  # RECEVOIR L'ENTREE ET LE VERIFIER
changed = change_directory(dir__)  # CHANGEMENT DU REPERTOIRE
files = []
if changed:
    print('Dossier changé!\n')
    print_directory()  # AFFICHAGE DU DOSSIER
    files = get_files(dir__)

    for f in files:
        infos = stat(f)
        print(infos)
