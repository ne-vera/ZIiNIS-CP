import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from rubik import Rubik
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sv_ttk

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Курсовая работа ЗИиНИС')
        sv_ttk.set_theme('dark')

        # -----------------------------------------------
        # Frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack()

        self.fields_frame = ttk.Frame(self.main_frame)
        self.fields_frame.grid(row=1, column=0, padx=20, pady=10)

        self.inputs_frame = ttk.LabelFrame(self.fields_frame, text='Входные параметры')
        self.inputs_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=10)
        
        self.outputs_frame = ttk.LabelFrame(self.fields_frame, text='Выходные параметры')
        self.outputs_frame.grid(row=2, column=0, columnspan=2, padx=0, pady=10)

        self.images_frame = ttk.LabelFrame(self.main_frame, text='Результат')
        self.images_frame.grid(row=1, column=1, padx=20, pady=10)

        # -----------------------------------------------
        # Label
        self.title_label = ttk.Label(self.main_frame, text='Кодирование изображений на основе прицнипа кубика Рубика')
        self.title_label.grid(row=0, column=0, padx=20, pady=10)

        # -----------------------------------------------
        # Operation type combobox
        self.operation_type_str = tk.StringVar()
        self.operation_type_str.set('')
        self.operation_label = ttk.Label(
            self.inputs_frame, text='Операция:')
        self.operation_label.grid(row=0, column=0,  padx=10, pady=(10,5), sticky='ew')
        self.operation_dropdown = ttk.Combobox(
            self.inputs_frame, textvariable=self.operation_type_str, state='readonly',  width=27)
        self.operation_dropdown.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.operation_dropdown['values'] = ('Кодирование', 'Декодирование')
        self.operation_dropdown.current(0)
        self.operation_dropdown.bind('<<ComboboxSelected>>', lambda event: self.operation_type_changed())

        # -----------------------------------------------
        # Input fields
        # Original image path
        self.original_image_path = tk.StringVar()
        self.original_image_path.trace('w', self.display_original_image)
        self.original_image_path_label = ttk.Label(self.inputs_frame, text = 'Путь к изображению:')
        self.original_image_path_label.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        self.original_image_path_entry = ttk.Entry(self.inputs_frame, width=50, textvariable=self.original_image_path)
        self.original_image_path_entry.grid(row=3, column=0, padx=10, pady=5, sticky='ew')
        self.btn_select_original_image_path = ttk.Button(self.inputs_frame, text = 'Открыть', command=lambda: self.select_original_image_path())
        self.btn_select_original_image_path.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        # Key path
        self.key_path = tk.StringVar()
        self.key_path_label = ttk.Label(self.outputs_frame, text = 'Путь к ключу:')
        self.key_path_label.grid(row=4, column=0, padx=10, pady=5, sticky='ew')
        self.key_path_entry = ttk.Entry(self.outputs_frame, width= 50, textvariable=self.key_path)
        self.key_path_entry.grid(row=5, column=0, padx=10, pady=5, sticky='ew')
        self.btn_select_key_path = ttk.Button(self.outputs_frame, text = 'Открыть', command=lambda: self.select_key_path())
        self.btn_select_key_path.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

        # Transformed image path
        self.transformed_image_path = tk.StringVar()
        self.transformed_image_path_label = ttk.Label(self.outputs_frame, text = 'Путь к закодированному изображению:')
        self.transformed_image_path_label.grid(row=8, column=0, padx=10, pady=5, sticky='ew')
        self.transformed_image_path_entry = ttk.Entry(self.outputs_frame, width= 50, textvariable=self.transformed_image_path)
        self.transformed_image_path_entry.grid(row=9, column=0, padx=10, pady=5, sticky='ew')
        self.btn_choose_transfromed_image_path = ttk.Button(self.outputs_frame, text = 'Открыть', command=lambda: self.select_transformed_image_path())
        self.btn_choose_transfromed_image_path.grid(row=9, column=1, padx=10, pady=5, sticky='ew')

        # Exit button
        self.btn_exit = ttk.Button(self.fields_frame, text='Выйти', width=20, command=self.destroy)
        self.btn_exit.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        # -----------------------------------------------
        # Output
        self.original_image_label = ttk.Label(self.images_frame, text='Оригинальное изображение')
        self.original_image_label.grid(row=0, column=0, padx=10, pady=20, sticky='ew')

        self.transformed_image_label = ttk.Label(self.images_frame, text='Закодированное изображение')
        self.transformed_image_label.grid(row=0, column=1, padx=10, pady=20, sticky='ew')

        self.progressbar = ttk.Progressbar(self.images_frame, orient='horizontal', mode='indeterminate')
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky='ew')
        # -----------------------------------------------

    def operation_type_changed(self) -> None:
        text = self.operation_type_str.get()

        if text == 'Кодирование':
            # Iterations                              
            self.iter_max = tk.IntVar()
            self.iter_label = ttk.Label(self.inputs_frame, text = 'Количество итераций (ITER_MAX):')
            self.iter_label.grid(row=6, column=0, padx=10, pady=5, sticky='w')
            self.iter_entry = ttk.Entry(self.inputs_frame, width=30, textvariable=self.iter_max)
            self.iter_entry.grid(row=7, column=0, padx=10, pady=5, sticky='w')
            self.iter_entry.configure(validate="key", validatecommand=(self.register(self.validate_iter), '%P'))


        if text == 'Декодирование':
            self.iter_label.grid_remove()
            self.iter_entry.grid_remove()
            self.transformed_image_path_label.config(text='Путь к декодированному изображению:')
            self.transformed_image_label.config(text='Декодированное изображение')

        # Transform button
        self.btn_transform_image = ttk.Button(self.fields_frame, text=text, state ='normal', style='Accent.TButton', width=20, command=lambda: self.transform())
        self.btn_transform_image.grid(row=3, column=1, padx=0, pady=20, sticky='w')

    def validate_iter(self, new_value):
        if new_value.isdigit():
            return True
        else:
            return False
    
    def select_original_image_path(self) -> None:
        image_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                    ("Image Files", ".png .bmp")])
        self.original_image_path_entry.delete(0, tk.END)
        self.original_image_path_entry.insert(tk.INSERT, image_path)
  
    def display_original_image(self, *args) -> None:
        img_path = self.original_image_path.get()
        if img_path != '':
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((300, 300))
                img = ImageTk.PhotoImage(img)
                self.original_image_display = ttk.Label(self.images_frame, image=img)
                self.original_image_display.image = img
                self.original_image_display.grid(row=1, column=0, padx=10, pady=20)
    
    def select_transformed_image_path(self) -> None:
        image_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                    ("Image Files", ".png .bmp")])
        self.transformed_image_path_entry.delete(0, tk.END)
        self.transformed_image_path_entry.insert(tk.INSERT, image_path)

    def select_key_path(self) -> None:
        key_path = filedialog.askopenfilename(title="Open JSON", filetypes=[
                                                    ("JSON", ".json ")])
        self.key_path_entry.delete(0, tk.END)
        self.key_path_entry.insert(tk.INSERT, key_path)
    
    def display_transformed_image(self, transformed_image_path: str):
        img = Image.open(transformed_image_path)
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        self.transformed_image_display = ttk.Label(self.images_frame, image=img)
        self.transformed_image_display.image = img
        self.transformed_image_display.grid(row=1, column=1, padx=10, pady=20)

    def check_fields(self):
        original_image_path = self.original_image_path.get()
        transformed_image_path = self.transformed_image_path.get()
        key_path = self.key_path.get()
        if os.path.exists(original_image_path):
            if self.operation_type_str.get() == 'Кодирование':
                iter_max = int(self.iter_max.get())
                if original_image_path != '' and os.path.exists(original_image_path) and transformed_image_path != '' and key_path != '' and iter_max != '':
                    return True
            elif self.operation_type_str.get() == 'Декодирование':
                if original_image_path != '' and transformed_image_path != '' and key_path != '':
                    return True
        else:
            messagebox.showerror(message='Изображение не найдено')

    def transform(self):
        try:
            original_image_path = self.original_image_path.get()
            transformed_image_path = self.transformed_image_path.get()
            key_path = self.key_path.get()
            rubik = Rubik(original_image_path)
            if self.operation_type_str.get() == 'Кодирование':
                iter_max = int(self.iter_max.get())
                rubik.encrypt(transformed_image_path, iter_max, key_path)
            elif self.operation_type_str.get() == 'Декодирование':
                rubik.decrypt(transformed_image_path, key_path)
            self.display_transformed_image(transformed_image_path) 
        except FileNotFoundError:
            messagebox.showerror(message='Файл не найден')
        except AttributeError:
            messagebox.showerror(message='Изображение не найдено')
        except ValueError:
            messagebox.showerror(message='Непраивльный формат файла')
        
    def start_mainloop(self) -> None:
        self.operation_type_changed()
        self.mainloop()

root = GUI()
root.start_mainloop()