"""
Archivos con las clases para trabajar con archivos.
"""
import datetime
import logging
import os
import re
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
            logging.debug('Estudiando archivo "%s"', file)

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

    @staticmethod
    def unique_names(files: List[str]) -> Tuple[List[str],
                                                List[Tuple[str, ...]]]:
        """
        Función para filtrar los archivos con mismo nombre.

        :param files: Lista con los path de todos los archivos.
        :return: Los listas, la primera con los path de archivos únicos, y la
        segunda con tuplas con los archivos con el mismo nombre.
        """

        # Se añaden todos los archivos a un diccionario por su digest.
        all_names: Dict[str, Tuple[str, ...]] = {}

        # Se comprueba cada archivo.
        for file in files:
            logging.debug('Estudiando archivo "%s"', file)
            name = os.path.basename(file)
            # Se añade al diccionario.
            if name in all_names:
                all_names[name] += (file,)
            else:
                all_names[name] = (file,)

        # Se filtran los archivos únicos y repetidos.
        unique_files = list(filter(lambda a: len(a) == 1, all_names.values()))
        dup_files = list(filter(lambda a: len(a) != 1, all_names.values()))

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

    INT2STR = {
        1: '01 - Enero',
        2: '02 - Febrero',
        3: '03 - Marzo',
        4: '04 - Abril',
        5: '05 - Mayo',
        6: '06 - Junio',
        7: '07 - Julio',
        8: '08 - Agosto',
        9: '09 - Septiembre',
        10: '10 - Octubre',
        11: '11 - Noviembre',
        12: '12 - Diciembre'
    }

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
            is_picture = file_extension.upper() in ext
            logging.debug('Verificando si es una foto "%s"... %s',
                          file, is_picture)
            return is_picture

        return list(filter(check_extension, files))

    @staticmethod
    def date_file(file: str) -> Tuple[str, str, str]:
        """
        Método para saber la fecha de la foto (tiene que estar en el nombre en
        la forma YYYYMMDD).
        :param file: path del archivo.
        :return: una tupla con el año, mes y día de la foto.
        """

        # Se obtiene el nombre.
        file_name = os.path.basename(file)

        # Se filtran los que no tienen en el nombre el patrón YYYYMMDD.
        result = re.search(r'(\d{4})(\d{2})(\d{2})', file_name)
        if not result:
            return None

        # Se obtienen el año, mes y día.
        year, month, day = result.group(1), result.group(2), result.group(3)

        # Se verifica que sea válida.
        try:
            # Intentar crear un objeto de fecha
            datetime.date(int(year), int(month), int(day))
            return year, month, day
        except (ValueError, TypeError):
            # Si se lanza una excepción ValueError, la fecha no es válida
            return None

    @staticmethod
    def get_month(month: str) -> str:
        """
        El método convierte un str 'XX' con el número del mes en otro con
        'XX - name'.

        :param month: Mes.
        :return: Mes en el formato indicado.
        """
        return Picture.INT2STR[int(month)]
