"""
Main para una interfaz gráfica.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pyBackUp.save import save_pictures, Depth

EMPTY_INPUT_FIELD = 'No se ha seleccionado una carpeta de la que hacer BackUp.'
EMPTY_OUTPUT_FIELD = 'No se ha seleccionado una carpeta destino.'
INVALID_INPUT_FIELD = 'El path de la carpeta de BackUp no existe.'
INVALID_OUTPUT_FIELD = 'El path de la carpeta de destino no existe.'


class GUI(tk.Frame):
    """
    Interfaz gráfica
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build()

    def build(self) -> None:
        """
        Constructor de la interfaz.
        """
        # Ventaja principal.
        self.root.title('Ordenar Fotos')

        # Se crean el input
        input_label = tk.Label(self.root, text='Carpeta de entrada:')
        input_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)

        input_button = tk.Button(self.root, text='Buscar',
                                 command=lambda: self.select_directory(self.input_entry, 'Fichero con las fotos.'))
        input_button.grid(row=1, column=1, padx=10, pady=5)

        # Se crea el output
        output_label = tk.Label(self.root, text='Carpeta de salida:')
        output_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=3, column=0, padx=10, pady=5)

        output_button = tk.Button(self.root, text='Buscar',
                                  command=lambda: self.select_directory(self.output_entry, 'Fichero donde copiarlas.'))
        output_button.grid(row=3, column=1, padx=10, pady=5)

        # Se crea el input de profundidad
        depth_label = tk.Label(self.root, text='Profundidad:')
        depth_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        self.depth_var = tk.StringVar(value='Mes')

        depth_options = ttk.Combobox(self.root,
                                     textvariable=self.depth_var,
                                     state='readonly')
        depth_options['values'] = ('Mes', 'Día', 'Año')
        depth_options.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        # Botones para ejecutar.
        run_button = tk.Button(self.root, text='Ejecutar',
                               command=self.run_script)
        run_button.grid(row=5, column=0, columnspan=2, pady=20, sticky='e')

    def select_directory(self, entry, title) -> None:
        """
        Método para seleccionar un archivo.
        :param entry: Entrada donde almacenar el path.
        :param title: Titulo de la ventana.
        """
        folder_selected = filedialog.askdirectory(title=title)
        if folder_selected:
            entry.delete(0, tk.END)
            entry.insert(0, folder_selected)

    def run_script(self) -> None:
        """
        Método para lanzar el proceso de backUp.
        """
        input_folder = self.input_entry.get()
        output_folder = self.output_entry.get()
        depth_option = self.depth_var.get()

        # Se verifican si hay paths.
        if not input_folder:
            messagebox.showerror('Error - Campo vacío.', EMPTY_INPUT_FIELD)
            return

        if not output_folder:
            messagebox.showerror('Error - Campo vacío.', EMPTY_OUTPUT_FIELD)
            return

        # Se verifica si los paths son carpetas.
        if not os.path.isdir(input_folder):
            messagebox.showerror('Error - Path inválido.', INVALID_INPUT_FIELD)
            return

        if not os.path.isdir(output_folder):
            messagebox.showerror('Error - Path inválido.',
                                 INVALID_OUTPUT_FIELD)
            return

        # Se selecciona la profundidad
        if depth_option == 'Día':
            depth = Depth.DAY
        elif depth_option == 'Año':
            depth = Depth.YEAR
        else:
            depth = Depth.MONTH

        try:
            save_pictures(input_folder=input_folder,
                          output_folder=output_folder,
                          no_date_folder='no_date',
                          depth=depth)
            messagebox.showinfo('Éxito',
                                'Las fotos se han almacenado correctamente.')
        except Exception as e:
            messagebox.showerror('Error', f'Ha ocurrido un error: {e}')


def main():
    """
    Método main.
    """

    root = tk.Tk()
    GUI(root)

    root.mainloop()


if __name__ == '__main__':
    main()
