"""
Archivo main.
"""

import argparse
import logging
import os
from typing import List
from enum import IntEnum
from pyBackUp.folder import Folder
from pyBackUp.file import File, Picture

SEPARADOR = '-'*20


class Depth(IntEnum):
    """
    Nivel de profundidad de la copia.
    """
    YEAR = 0
    MONTH = 1
    DAY = 2


def get_unique_hash_pictures(pictures: List[str]) -> List[str]:
    """
    Método para abstraer el obtener fotos únicas y notificar las duplicadas.

    :param pictures: Lista con las fotos que comprobar.
    :return: Lista de fotos únicas (filtrado para que no haya dos fotos con el
    mismo digest).
    """

    # Se filtran los archivos para evitar los duplicados
    logging.info('Obteniendo fotos únicas...')
    unique_pics, dup_digest = File.unique_files(pictures)

    # Se obtiene una copia de cada uno.
    if len(dup_digest) > 0:
        logging.info('Obteniendo copia única de las fotos duplicadas.')

        used_files, ignored_files = [], []
        for dup_files in dup_digest:
            # Se separa el primer elemento y el resto.
            used_files.append(dup_files[:1][0])
            ignored_files.append(dup_files[1:])
        unique_pics += used_files

        # Las fotos que no se usan, se indican.
        logging.info('Las siguientes fotos no se van a copiar:')
        logging.info(SEPARADOR)
        for used_file, same_hash in zip(used_files, ignored_files):
            logging.info('Las fotos con el mismo hash que "%s"', used_file)

            for unused_file in same_hash:
                logging.info('\t- %s', unused_file)
            logging.info(SEPARADOR)

    else:
        logging.info('No hay fotos duplicadas.')

    return unique_pics


def save_pictures(input_folder: str, output_folder: str,
                  no_date_folder: str, depth: Depth) -> None:
    """
    Función para almacenar las fotos.

    :param input_folder: Carpeta de donde buscar.
    :param output_folder: Carpeta donde volcar las fotos.
    :param no_date_folder: Carpeta para las fotos sin nombre.
    :param depth: Profundidad de las carpetas de fecha.
    """

    # Se obtiene todas las fotos de la carpeta
    logging.info('Obteniendo archivos de "%s"...', input_folder)
    all_files = Folder.all_files(input_folder)

    # Se obtienen únicamente los archivos que son fotos.
    logging.info('Separando fotos...')
    all_pictures = Picture.filter(all_files)

    # Se filtran los archivos para evitar los duplicados
    logging.info('Obteniendo fotos únicas...')
    unique_pics = get_unique_hash_pictures(all_pictures)

    # Se obtienen los archivos con nombre único.
    logging.info('Obteniendo fotos con nombres repetidos...')
    unique_name, dup_name = File.unique_names(unique_pics)

    # Se renombran los archivos.
    if len(dup_name) > 0:
        # Las fotos que no se usan, se indican.
        logging.info('Fotos ignoradas: Mismo nombre.')
        logging.info(SEPARADOR)
        for pictures_names in dup_name:
            for name in pictures_names:
                logging.info('\t- %s', name)
            logging.info(SEPARADOR)
    else:
        logging.info('No hay fotos con nombre duplicado.')

    # Se obtiene la fecha de cada foto.
    logging.info('Obteniendo fechas...')
    picture_and_folder = []
    for picture in unique_name:
        date = Picture.date_file(picture)

        if date is not None:
            year, month, day = date
            logging.debug('Fotografía con fecha: "%s/%s/%s" %s',
                          year, month, day, picture)

            if depth == Depth.YEAR:
                path = year
            elif depth == Depth.MONTH:
                path = os.path.join(year, Picture.get_month(month))
            else:
                path = os.path.join(year, Picture.get_month(month), day)

        else:
            # Si no tiene fecha, se indica
            logging.debug('Fotografía sin fecha: "%s"', picture)
            path = no_date_folder

        # Se crea el full_path
        full_path = os.path.join(output_folder, path)

        picture_and_folder.append((picture, full_path))

    # Se vuelca el resultado.
    logging.info('Copiando fotos...')
    Folder.move_files(picture_and_folder)

    logging.info('Terminado.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', dest='input',
                        type=str, required=True,
                        help='Carpeta de la que obtener las fotos.')

    parser.add_argument('--output', '-o', dest='output',
                        type=str, required=True,
                        help='Carpeta de la volcar las fotos ordenadas.')

    parser.add_argument('--no_date', dest='no_date',
                        type=str, default='no_date',
                        help='Carpeta (en -o) para las fotos sin fechas.')

    parser.add_argument('--debug', dest='debug',
                        action='store_true', default=False,
                        help='Flag para mensajes de debug.')

    # Flags para un comportamiento especial
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--use_day', dest='day',
                       action='store_true', default=False,
                       help='Flag para usar hasta el día.')

    group.add_argument('--only_year', dest='year',
                       action='store_true', default=False,
                       help='Flag para solo usar el año.')

    # Se obtienen los parámetros.
    args = parser.parse_args()

    # Se configura el logging
    if args.debug is True:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)

    # Nivel de profundidad.
    if args.day:
        save_pictures(input_folder=args.input, output_folder=args.output,
                      no_date_folder=args.no_date, depth=Depth.DAY)
    elif args.year:
        save_pictures(input_folder=args.input, output_folder=args.output,
                      no_date_folder=args.no_date, depth=Depth.YEAR)
    else:
        save_pictures(input_folder=args.input, output_folder=args.output,
                      no_date_folder=args.no_date, depth=Depth.MONTH)
