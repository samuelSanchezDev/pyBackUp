"""
Archivos con las clases para trabajar con archivos.
"""
from typing import List, Tuple, Dict, Union
import hashlib
import pathlib


class File:
    """
    Clase con los métodos para trabajar con archivos.
    """

    @staticmethod
    def unique_files(files: List[str],
                     func: str = "sha1") -> Tuple[List[str],
                                                  List[Tuple[str, ...]]]:
        """
        Función para filtrar los archivos con mismo hash.

        :param files: Lista con los path de todos los archivos.
        :param func: Nombre del hash de hashlib con la que calcular el digest.
        Por defecto es sha1.
        :return: Los listas, la primera con los path de archivos únicos, y la
        segunda con tuplas con los archivos con el mismo digest.
        """

        # Se añaden todos los archivos a un diccionario por su digest.
        all_digest: Dict[bytes, Tuple[str, ...]] = {}

        # Se comprueba cada archivo.
        for file in files:
            # Se instancia la función hash.
            my_hash = hashlib.new(func)

            # Se obtiene el digest
            with open(file, 'rb') as f:
                my_hash.update(f.read())
                digest = my_hash.digest()

            # Se añade al diccionario.
            if digest in all_digest:
                all_digest[digest] += (file,)
            else:
                all_digest[digest] = (file,)

        # Se filtran los archivos únicos y repetidos.
        unique_files = list(filter(lambda a: len(a) == 1, all_digest.values()))
        dup_files = list(filter(lambda a: len(a) != 1, all_digest.values()))

        # Los archivos únicos se mapean para eliminar las tuplas
        unique_files = list(map(lambda a: a[0], unique_files))

        return unique_files, dup_files


class Picture:
    """
    Clase con los métodos para trabajar con archivos que son fotos.
    """

    extensions: List[str] = [
        '.JPEG', '.JPG',  # JPEG/JPG
        '.GIF',  # GIF
        '.PNG',  # PNG
        '.WEBP',  # WebP
        '.RAW'  # RAW
    ]

    @staticmethod
    def filter(files: List[str],
               ext: Union[List[str], None] = None) -> List[str]:
        """
        Método para filtrar todos los archivos que sean imágenes.

        :param files: Lista con todos los archivos.
        :param ext: Lista con todas las extensiones que corresponden a
        imágenes. Por defecto consideran: JPEG/JPG, GIF, PNG, WebP y RAW.
        :return: Lista con los archivos que son imágenes.
        """

        # Si no hay extensiones, se usan las por defecto.
        if ext is None:
            ext = Picture.extensions

        # Función para comprobar si un archivo es una foto.
        def check_extension(file: str) -> bool:
            file_extension = pathlib.Path(file).suffix
            return file_extension.upper() in ext

        return list(filter(check_extension, files))
