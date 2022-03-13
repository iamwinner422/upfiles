import os
import pathlib
import time
import glob
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path


'''from stat import ST_MTIME
from time import localtime, asctime'''


# POUR INTERAGIR AVEC LE SYSTEME

# Fonction pour changer de répertoire au lancement
def change_directory(directory_):
    os.chdir(directory_)
    return True


def print_directory():
    print(os.getcwd())
    time.sleep(1)
    print("En attente...")
    print("")


def check_directory():
    user_directory = input("Entrez le chemin du dossier dans lequel vous travaillez: ")
    while not os.path.exists(user_directory) and not os.path.isdir(user_directory):
        print("Le chemin d'accès au dossier n'existe pas ou est incorrect!\n")
        user_directory = input("Entrez le chemin du dossier: ")
    else:
        return user_directory


def make_base_directory():

    directory_ = 'Upfiles'
    documents_folder_ = os.path.expanduser('~/Documents')
    #full_path = ''

    full_path_ = os.path.join(documents_folder_, directory_)
    try:
        os.mkdir(full_path_)
        print("Le chemin de sauvegarde par défaut est: " + str(full_path_) + "\n")
    except OSError as error:
        print(error)

    return full_path_

def check_base_directory():
    directory_ = 'Upfiles'
    documents_folder_ = os.path.expanduser('~/Documents')
    full_path_ = os.path.join(documents_folder_, directory_)
    if not os.path.exists(full_path_) and not os.path.isdir(full_path_):
        return True
    else:
        return False

def listing(full_path_):
    file_name = time.strftime("%Y%m%d")+".txt"
    updated_files = []
    deleted_files = []
    created_files = []
    moved_files = []

    patterns = ['*.php', '*.html', '*.css', '*.js', '*.txt']
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_created(event):
        print(f"Le fichier {event.src_path} a été crée!\n")
        if event.src_path not in created_files:
            created_files.append(event.src_path)

    def on_deleted(event):
        print(f"Le fichier {event.src_path}! a été supprimé!\n")
        if event.src_path not in deleted_files:
            deleted_files.append(event.src_path)

    def on_modified(event):
        print(f"Le fichier {event.src_path} a été modifié!\n")
        if event.src_path not in updated_files:
            updated_files.append(event.src_path)

    def on_moved(event):
        print(f"Le fichier {event.src_path} a été déplacé ou renommé en/vers {event.dest_path}\n")
        if event.src_path not in moved_files:
            moved_files.append(event.dest_path)


    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    dir__ = check_directory()  # RECEVOIR L'ENTREE ET LE VERIFIER
    changed = change_directory(dir__)  # CHANGEMENT DU REPERTOIRE

    if changed:

        print('Dossier changé!\n')

        print_directory()  # AFFICHAGE DU DOSSIER
        # AFFICHAGE DU DOSSIER

        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, dir__, recursive=go_recursively)

        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

        changed = change_directory(full_path_)  #CHANGEMENT DE DOSSIER::DOSSIER DE SAUVEGARDE

        if changed:
            backup = open(file_name, "a+")
            # RECAP DES FICHIERS CREES
            if len(created_files) == 0:
                print("Aucun fichier crée pour l'instant.\n")
            elif len(created_files) == 1:
                print("Un fichier crée.")
                print(created_files[0] + "\n")
                backup.write("-(01) FICHIER CREE\n")
                backup.write("\t"+created_files[0] + "\n")
                backup.write("\n")

            else:
                print(f"{len(created_files)} fichiers crées.")
                backup.write("-(" + repr(len(created_files)) + ") FICHIERS CREES\n")
                for i in range(len(created_files)):
                    print(f"{i}- {created_files[i]}")
                    backup.write("\t"+created_files[i] + "\n")
                    backup.write("\n")
                print(' ')

            # RECAP DES FICHIERS MODIFIES
            if len(updated_files) == 0:
                print("Aucun fichier modifié pour l'instant.\n")
            elif len(updated_files) == 1:
                print("Un fichier modifié.")
                print(updated_files[0] + "\n")
                backup.write("-(01) FICHIER MODIFIE\n")
                backup.write("\t"+updated_files[0] + "\n")
                backup.write("\n")
            else:
                print(f"{len(updated_files)} fichiers modifiés.")
                backup.write("-(" + repr(len(updated_files)) + ") FICHIERS MODIFIES\n")
                for i in range(len(updated_files)):
                    print(f"{i}- {updated_files[i]}")
                    backup.write("\t"+updated_files[i] + "\n")
                    backup.write("\n")
                print(' ')

            # RECAP DES FICHIERS SUPPRIMES
            if len(deleted_files) == 0:
                print("Aucun fichier supprimé pour l'instant.\n")
            elif len(deleted_files) == 1:
                print("Un fichier supprimé.")
                print(deleted_files[0] + "\n")
                backup.write("-(01) FICHIER SUPPRIME\n")
                backup.write("\t"+deleted_files[0] + "\n")
                backup.write("\n")
            else:
                print(f"{len(deleted_files)} fichiers supprimés.")
                backup.write("-(" + repr(len(deleted_files)) + ") FICHIERS SUPPRIMES\n")
                for i in range(len(deleted_files)):
                    print(f"{i}- {deleted_files[i]}")
                    backup.write("\t"+deleted_files[i] + "\n")
                    backup.write("\n")
                print(' ')

            # RECAP DES FICHIERS RENOMMES
            if len(moved_files) == 0:
                print("Aucun fichier déplacé ou renommé pour l'instant.\n")
            elif len(moved_files) == 1:
                print("Un fichier déplacé ou renommé.")
                print(moved_files[0] + "\n")
                backup.write("-(01) FICHIERS DEPLACE OU RENOMME\n")
                backup.write("\t"+moved_files[0] + "\n")
                backup.write("\n")
            else:
                print(f"{len(moved_files)} déplacés ou renommés.")
                backup.write("-(" + repr(len(moved_files)) + ") FICHIERS DEPLACES OU RENOMMES\n")
                for i in range(len(moved_files)):
                    print(f"{i}- {moved_files[i]}")
                    backup.write("\t"+moved_files[i] + "\n")
                    backup.write("\n")
                print(' ')

            backup.close()
            print(f"Votre travail a été sauvegardé dans {str(os.path.join(full_path_, file_name))} .\n")



if __name__ == "__main__":
    directory = 'Upfiles'
    documents_folder = os.path.expanduser('~\Documents')
    full_path = os.path.join(documents_folder, directory)

    if not os.path.exists(full_path) and not os.path.isdir(full_path):
        full_path = make_base_directory()
        listing(full_path)
    else:
        listing(full_path)
