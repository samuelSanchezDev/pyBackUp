"""
Archivo main.
"""
import argparse
import logging
from pyBackUp.save import save_pictures, Depth

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
