"""
Archivos con las clases para trabajar con carpetas.
"""
import shutil
from typing import List, Tuple
import os
import logging


class Folder:
    """
    Clase con los métodos para trabajar con carpetas.
    """

    @staticmethod
    def all_files(folder: str, recursive: bool = True) -> List[str]:
        """
        Método para obtener todos los archivos de una carpeta.

        :param folder: Carpeta que listar.
        :param recursive: Flag para hacer la búsqueda recursiva.
        :return: Lista con todos los paths de los archivos.
        """

        logging.debug('Explorando carpeta "%s"', folder)

        # Lista con todos los archivos.
        all_files: List[str] = []

        # Se recorren todos los ficheros o directorios
        for file_or_dir in os.listdir(folder):

            # Se crea al path completo.
            full_path = os.path.join(folder, file_or_dir)

            # Si es un archivo, se añade a la lista.
            if os.path.isfile(full_path):
                all_files.append(full_path)
                logging.debug('Añadido archivo "%s"', full_path)

            # Si es una carpeta y hay recursividad, se investiga.
            elif recursive and os.path.isdir(full_path):
                all_files += Folder.all_files(full_path)

            # Cualquier otro caso, se ignora.
            else:
                logging.info('Ignorando path: "%s"', full_path)

        return all_files

    @staticmethod
    def move_files(files: List[Tuple[str, str]]) -> None:
        """
        Método para mover archivos a la carpeta correspondiente.

        :param files: Lista con los archivos que mover en forma de tupla
        (path_de_origen, path_de_la_carpeta_destino)
        """

        # Se extraen todas las carpetas únicas y se crean.
        all_folders = list(map(lambda a: a[1], files))
        for folder in set(all_folders):
            os.makedirs(folder, exist_ok=True)

        # Se mueven todos los archivos a su nueva path
        for old_path, new_folder in files:
            file_name = os.path.basename(old_path)
            new_path = os.path.join(new_folder, file_name)
            shutil.copyfile(old_path, new_path)
