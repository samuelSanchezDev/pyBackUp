"""
Archivos con las clases para trabajar con carpetas.
"""
from typing import List, Tuple, Set, Dict
import os
import logging

class Folder:
    """
    Clase con los métodos para trabajar con archivos.
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
                logging.info(f'Ignorando path: {full_path}')

        return all_files