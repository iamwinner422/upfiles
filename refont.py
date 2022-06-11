import os
import pathlib
import time
import glob
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path


class FileWatcher:
    
    def __init__(self, folder:Path) -> None:
        self.updated_files = []
        self.deleted_files = []
        self.created_files = []
        self.moved_files = []
        self.folder = folder

        patterns = ['*.php', '*.html', '*.css', '*.js', '*.txt']
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True

        self.my_observer = Observer()
        self.my_event_handler = PatternMatchingEventHandler(
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive)

        self._bindings()

        pass

    


    

    def on_created(self, event):
        print(f"Le fichier {event.src_path} a été crée!\n")
        if event.src_path not in self.created_files:
            self.created_files.append(event.src_path)

    def on_deleted(self, event):
        print(f"Le fichier {event.src_path}! a été supprimé!\n")
        if event.src_path not in self.deleted_files:
            self.deleted_files.append(event.src_path)

    def on_modified(self, event):
        print(f"Le fichier {event.src_path} a été modifié!\n")
        if event.src_path not in self.updated_files:
            self.updated_files.append(event.src_path)

    def on_moved(self, event):
        print(f"Le fichier {event.src_path} a été déplacé ou renommé en/vers {event.dest_path}\n")
        if event.src_path not in self.moved_files:
            self.moved_files.append(event.dest_path)


    def _bindings(self):
        self.my_event_handler.on_created = self.on_created
        self.my_event_handler.on_deleted = self.on_deleted
        self.my_event_handler.on_modified = self.on_modified
        self.my_event_handler.on_moved = self.on_moved
        return None
        

    def run(self):
        self.my_observer.start()
        while 1:
            self.my_observer.schedule(self.my_event_handler, self.folder, recursive=True)
        return None
    ...




class Reporter:
    logfile = Path.home() / "Documents/Upfiles/file.txt"
    def __init__(self, filewatcher:FileWatcher) -> None:
        Reporter.logfile.parent.mkdir(exist_ok=True)
        Reporter.logfile.touch(exist_ok=True)
        self.filewatcher = filewatcher

        self.make_reports()
        pass


    def make_reports(self):

        log_stream = Reporter.logfile.open(mode="a")
            # RECAP DES FICHIERS CREES
        if len(self.filewatcher.created_files) == 0:
            print("Aucun fichier crée pour l'instant.\n")
        elif len(self.filewatcher.created_files) == 1:
            print("Un fichier crée.")
            print(self.filewatcher.created_files[0] + "\n")
            log_stream.write("-(01) FICHIER CREE\n")
            log_stream.write("\t"+self.filewatcher.created_files[0] + "\n")
            log_stream.write("\n")

        else:
            print(f"{len(self.filewatcher.created_files)} fichiers crées.")
            log_stream.write("-(" + repr(len(self.filewatcher.created_files)) + ") FICHIERS CREES\n")
            for i in range(len(self.filewatcher.created_files)):
                print(f"{i}- {self.filewatcher.created_files[i]}")
                log_stream.write("\t"+self.filewatcher.created_files[i] + "\n")
                log_stream.write("\n")
            print(' ')

        # RECAP DES FICHIERS MODIFIES
        if len(self.filewatcher.updated_files) == 0:
            print("Aucun fichier modifié pour l'instant.\n")
        elif len(self.filewatcher.updated_files) == 1:
            print("Un fichier modifié.")
            print(self.filewatcher.updated_files[0] + "\n")
            log_stream.write("-(01) FICHIER MODIFIE\n")
            log_stream.write("\t"+self.filewatcher.updated_files[0] + "\n")
            log_stream.write("\n")
        else:
            print(f"{len(self.filewatcher.updated_files)} fichiers modifiés.")
            log_stream.write("-(" + repr(len(self.filewatcher.updated_files)) + ") FICHIERS MODIFIES\n")
            for i in range(len(self.filewatcher.updated_files)):
                print(f"{i}- {self.filewatcher.updated_files[i]}")
                log_stream.write("\t"+self.filewatcher.updated_files[i] + "\n")
                log_stream.write("\n")
            print(' ')

        # RECAP DES FICHIERS SUPPRIMES
        if len(self.filewatcher.deleted_files) == 0:
            print("Aucun fichier supprimé pour l'instant.\n")
        elif len(self.filewatcher.deleted_files) == 1:
            print("Un fichier supprimé.")
            print(self.filewatcher.deleted_files[0] + "\n")
            log_stream.write("-(01) FICHIER SUPPRIME\n")
            log_stream.write("\t"+self.filewatcher.deleted_files[0] + "\n")
            log_stream.write("\n")
        else:
            print(f"{len(self.filewatcher.deleted_files)} fichiers supprimés.")
            log_stream.write("-(" + repr(len(self.filewatcher.deleted_files)) + ") FICHIERS SUPPRIMES\n")
            for i in range(len(self.filewatcher.deleted_files)):
                print(f"{i}- {self.filewatcher.deleted_files[i]}")
                log_stream.write("\t"+self.filewatcher.deleted_files[i] + "\n")
                log_stream.write("\n")
            print(' ')

        # RECAP DES FICHIERS RENOMMES
        if len(self.filewatcher.moved_files) == 0:
            print("Aucun fichier déplacé ou renommé pour l'instant.\n")
        elif len(self.filewatcher.moved_files) == 1:
            print("Un fichier déplacé ou renommé.")
            print(self.filewatcher.moved_files[0] + "\n")
            log_stream.write("-(01) FICHIERS DEPLACE OU RENOMME\n")
            log_stream.write("\t"+self.filewatcher.moved_files[0] + "\n")
            log_stream.write("\n")
        else:
            print(f"{len(self.filewatcher.moved_files)} déplacés ou renommés.")
            log_stream.write("-(" + repr(len(self.filewatcher.moved_files)) + ") FICHIERS DEPLACES OU RENOMMES\n")
            for i in range(len(self.filewatcher.moved_files)):
                print(f"{i}- {self.filewatcher.moved_files[i]}")
                log_stream.write("\t"+self.filewatcher.moved_files[i] + "\n")
                log_stream.write("\n")
            print(' ')







def main():
    watcher = FileWatcher("d://")
    reporter = Reporter(watcher)
    watcher.run()
    return None



if __name__ ==  "__main__":
    main()