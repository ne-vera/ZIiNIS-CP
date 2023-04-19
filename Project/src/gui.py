import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from rubik import Cubik
from tkinter import messagebox
from PIL import ImageTk, Image

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Rubik')
        self.state('zoomed') 

        # -----------------------------------------------
        # Frames
        self.inputs_frame = ttk.Frame(self,  borderwidth=1, relief=tk.SUNKEN)
        self.inputs_frame.grid(row=0, column=1, rowspan=10,
                 columnspan=10, pady=10, padx=30)
        self.inputs_frame['padding'] = (5, 20, 5, 20)

        self.outputs_frame = ttk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
        self.outputs_frame.grid(row=11, column=1, rowspan=8, pady=5, padx=10)
        self.outputs_frame['padding'] = (5, 0, 5, 0)

        # -----------------------------------------------
        # Operation type combobox
        self.operation_type_str = tk.StringVar()
        self.operation_label = ttk.Label(
            self.inputs_frame, text='Operation Type:')
        self.operation_label.grid(row=0, column=0, sticky=tk.W)
        self.operation_dropdown = ttk.Combobox(
            self.inputs_frame, textvariable=self.operation_type_str, state='readonly',  width=27)
        self.operation_dropdown.grid(row=1, column=0, sticky=tk.W)
        self.operation_dropdown['values'] = ('Encrypt', 'Decrypt')
        self.operation_dropdown.current(0)
        self.operation_dropdown.bind('<<ComboboxSelected>>', lambda event: self.operation_type_changed())
        # -----------------------------------------------
        # Input fields

        # Original image
        self.original_image_path_label = ttk.Label(self.inputs_frame, text = 'Image Path:')
        self.original_image_path_label.grid(row=2, column=0, sticky=tk.W)
        self.original_image_path_entry = ttk.Entry(self.inputs_frame, width='50')
        self.original_image_path_entry.grid(row=3, column=0, sticky=tk.W)
        self.btn_select_original_image_path = ttk.Button(self.inputs_frame, text = 'Open', command=lambda: self.select_original_image_path())
        self.btn_select_original_image_path.grid(row=3, column=1, sticky = tk.W)

        # Key
        self.key_path_label = ttk.Label(self.inputs_frame, text = 'Key Path:')
        self.key_path_label.grid(row=4, column=0, sticky=tk.W)
        self.key_path_entry = ttk.Entry(self.inputs_frame, width = '50')
        self.key_path_entry.grid(row=5, column=0, sticky=tk.W)
        self.btn_select_key_path = ttk.Button(self.inputs_frame, text = 'Open', command=lambda: self.select_key_path())
        self.btn_select_key_path.grid(row=5, column=1, sticky = tk.W)

        # Transformed image
        self.transformed_image_path_label = ttk.Label(self.inputs_frame, text = 'Encrypted Image Path:')
        self.transformed_image_path_label.grid(row=8, column=0, sticky=tk.W)
        self.transformed_image_path_entry = ttk.Entry(self.inputs_frame, width = '50')
        self.transformed_image_path_entry.grid(row=9, column=0, sticky=tk.W)
        self.btn_choose_transfromed_image_path = ttk.Button(self.inputs_frame, text = 'Open', command=lambda: self.select_transformed_image_path())
        self.btn_choose_transfromed_image_path.grid(row=9, column=1, sticky = tk.W)
        # -----------------------------------------------
        # Otput fields

        # Progress bar
        self.progressbar = ttk.Progressbar(self.outputs_frame, orient="horizontal", length=550, mode="indeterminate")
        
        # Exit button
        self.btn_exit = ttk.Button(self.outputs_frame, text="Exit", width=8)
        self.btn_exit.grid(row=3, column=3, sticky=tk.E, pady=10)
        # -----------------------------------------------

    def start_mainloop(self) -> None:
        self.operation_type_changed()
        self.mainloop()

    def operation_type_changed(self) -> None:
        text = self.operation_type_str.get()

        if text == 'Encrypt':
             # Iterations
            self.iter_label = ttk.Label(self.inputs_frame, text = 'Number of Iterations:')
            self.iter_label.grid(row=6, column=0, sticky=tk.W)
            self.iter_entry = ttk.Entry(self.inputs_frame, width = '30')
            self.iter_entry.grid(row=7, column=0, sticky=tk.W)

        if text == 'Decrypt':
            self.iter_label.grid_remove()
            self.iter_entry.grid_remove()
            self.transformed_image_path_label.config(text='Decrypred Image Path:')

        # Transform button
        self.btn_transform_image = ttk.Button(self.inputs_frame, text = text, state = 'normal', command=lambda: self.transform())
        self.btn_transform_image.grid(row = 10, column = 1, sticky=tk.W)

    def select_original_image_path(self) -> None:
        tk.Tk().withdraw()
        image_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                    ("Image Files", ".png .bmp")])
        self.original_image_path_entry.delete(0, tk.END)
        self.original_image_path_entry.insert(tk.INSERT, image_path)

        # opens the image
        img = Image.open(image_path)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)

        # create a label
        self.original_image_panel = ttk.Label(self.outputs_frame, image=img)

        # set the image as img
        self.original_image_panel.image = img
        self.original_image_panel.grid(row=1, column=1, padx=5)
    
    def select_transformed_image_path(self) -> None:
        tk.Tk().withdraw()
        image_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                    ("Image Files", ".png .bmp")])
        self.transformed_image_path_entry.delete(0, tk.END)
        self.transformed_image_path_entry.insert(tk.INSERT, image_path)

    def select_key_path(self) -> None:
        tk.Tk().withdraw()
        key_path = filedialog.askopenfilename(title="Open JSON", filetypes=[
                                                    ("JSON", ".json ")])
        self.key_path_entry.delete(0, tk.END)
        self.key_path_entry.insert(tk.INSERT, key_path)
        
    def transform(self):
        self.original_image_path = self.original_image_path_entry.get()
        self.transformed_image_path = self.transformed_image_path_entry.get()
        self.key_path = self.key_path_entry.get()
        rubik = Cubik(self.original_image_path)
        if self.operation_type_str.get() == 'Encrypt':
            self.iter_max = int(self.iter_entry.get())
            rubik.encrypt(self.transformed_image_path, self.iter_max, self.key_path)
        elif self.operation_type_str.get() == 'Decrypt':
            rubik.decrypt(self.transformed_image_path, self.key_path)

        # opens the image
        img = Image.open(self.transformed_image_path)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)

        # create a label
        self.transformed_image_panel = ttk.Label(self.outputs_frame, image=img)

        # set the image as img
        self.transformed_image_panel.image = img
        self.transformed_image_panel.grid(row=1, column=2, padx=5)

root = GUI()
root.start_mainloop()
