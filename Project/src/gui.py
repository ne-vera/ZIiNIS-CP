import tkinter as tk
import tkinter.ttk as ttk

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
        self.operation_dropdown['values'] = ('encrypt', 'decrypt')
        self.operation_dropdown.current(0)

        # -----------------------------------------------
        # Input fields

        # Original image
        self.original_image_path_label = ttk.Label(self.inputs_frame, text = 'Image Path:')
        self.original_image_path_label.grid(row=2, column=0, sticky=tk.W)
        self.original_image_path_entry = ttk.Entry(self.inputs_frame, width='50')
        self.original_image_path_entry.grid(row=3, column=0, sticky=tk.W)
        self.btn_choose_original_image_path = ttk.Button(self.inputs_frame, text = 'Open')
        self.btn_choose_original_image_path.grid(row=3, column=1, sticky = tk.W)

        # Key
        self.key_path_label = ttk.Label(self.inputs_frame, text = 'Key Path:')
        self.key_path_label.grid(row=4, column=0, sticky=tk.W)
        self.key_path_entry = ttk.Entry(self.inputs_frame, width = '50')
        self.key_path_entry.grid(row=5, column=0, sticky=tk.W)
        self.btn_choose_key_path = ttk.Button(self.inputs_frame, text = 'Open')
        self.btn_choose_key_path.grid(row=5, column=1, sticky = tk.W)

        # Iterations
        self.iter_label = ttk.Label(self.inputs_frame, text = 'Number of Iterations:')
        self.iter_label.grid(row=6, column=0, sticky=tk.W)
        self.iteration_entry = ttk.Entry(self.inputs_frame, width = '30')
        self.iteration_entry.grid(row=7, column=0, sticky=tk.W)
        self.iter_max = tk.IntVar(self.iteration_entry)

        # Transformed image
        self.transformed_image_path_label = ttk.Label(self.inputs_frame, text = 'Encrypted Image Path:')
        self.transformed_image_path_label.grid(row=8, column=0, sticky=tk.W)
        self.transformed_image_path_entry = ttk.Entry(self.inputs_frame, width = '50')
        self.transformed_image_path_entry.grid(row=9, column=0, sticky=tk.W)
        self.btn_choose_transfromed_image_path = ttk.Button(self.inputs_frame, text = 'Open')
        self.btn_choose_transfromed_image_path.grid(row=9, column=1, sticky = tk.W)

        # Transform button
        self.btn_choose_transformed_image_path = ttk.Button(self.inputs_frame, text = 'Encrypt')
        self.btn_choose_transformed_image_path.grid(row = 10, column = 1, sticky=tk.W)
        # -----------------------------------------------
        # Otput fields

        # Progress bar
        self.progressbar = ttk.Progressbar(self.outputs_frame, orient="horizontal", length=550, mode="indeterminate")
        
        # Exit button
        self.btn_exit = ttk.Button(self.outputs_frame, text="Exit", width=8)
        self.btn_exit.grid(row=3, column=3, sticky=tk.E, pady=10)
        # -----------------------------------------------

    def start_mainloop(self) -> None:
        self.mainloop()



root = GUI()
root.start_mainloop()
