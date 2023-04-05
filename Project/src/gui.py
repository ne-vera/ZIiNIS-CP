import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import sys
from PIL import ImageTk, Image
from validation import *
from rubik import *


originalImagePath = None
transformedImagePath = None
keyPath = None
iter_max = None

root = tk.Tk()
root.minsize(500, 500)
root.title("Rubik")
root.resizable(True, True)

inputsFrame = ttk.Frame(root,  borderwidth=1, relief=tk.SUNKEN)
inputsFrame.grid(row=0, column=1, rowspan=5,
                 columnspan=10, pady=10, padx=30)
inputsFrame["padding"] = (5, 20, 5, 20)
outputsFrame = ttk.Frame(root, borderwidth=1, relief=tk.SUNKEN)
outputsFrame.grid(row=6, column=1, rowspan=8, pady=5, padx=10)
outputsFrame["padding"] = (5, 0, 5, 0)
imageFrame = ttk.Frame(inputsFrame)
imageFrame.grid(row=12, column=0, rowspan=10,
                             columnspan=10, pady=30, padx=30)

# -----------------------------------------------
# operation type combobox
opTypeStr = tk.StringVar()
operationLabel = ttk.Label(
    inputsFrame, text="Operation Type:")
operationLabel.grid(row=0, column=0, sticky=tk.W)
operationDropDown = ttk.Combobox(
    inputsFrame, textvariable=opTypeStr, state="readonly",  width=27)
operationDropDown.grid(row=1, column=0, sticky=tk.W)
operationDropDown["values"] = ("encrypt", "decrypt")
operationDropDown.current(0)
operationDropDown.bind(
    "<<ComboboxSelected>>", lambda event: operationTypeChanged())

# --------------------------------------------------------------------------------------------
# Image selection
originalImageDirLabel = ttk.Label(inputsFrame, text="Image Path:")
originalImageDirLabel.grid(row=2, column=0, sticky=tk.W)
originalImagePathEntry = ttk.Entry(inputsFrame, width="50")
originalImagePathEntry.grid(row=3, column=0, sticky=tk.W)
btnChooseOrigImgDir = ttk.Button(inputsFrame, text="Open",   width=8,
                           command=lambda: selectOriginalImage())
btnChooseOrigImgDir.grid(row=3, column=1, sticky=tk.W)
# --------------------------------------------------------------------------------------------
transformedImageLabel = ttk.Label(inputsFrame, text="Encrypted Image Path:")
transformedImageLabel.grid(row=4, column=0, sticky=tk.W)
transformedImagePathEntry = ttk.Entry(inputsFrame, width="50")
transformedImagePathEntry.grid(row=5, column=0, sticky=tk.W)
btnChooseTransformedImgDir = ttk.Button(inputsFrame, text="Open",   width=8,
                                command=lambda: selectTransformedImage())
btnChooseTransformedImgDir.grid(row=5, column=1, sticky=tk.W)
# --------------------------------------------------------------------------------------------
# Key Path Selection
keyPathLabel = ttk.Label(inputsFrame, text="Key Path:")
keyPathLabel.grid(row=6, column=0, sticky=tk.W)
keyPathEntry = ttk.Entry(inputsFrame, width="50")
keyPathEntry.grid(row=7, column=0, sticky=tk.W)
btnChooseKeyPath = ttk.Button(inputsFrame, text="Open",   width=8,
                                command=lambda: selectKeyPath())
btnChooseKeyPath.grid(row=7, column=1, sticky=tk.W)
# --------------------------------------------------------------------------------------------
vcmd = root.register(validateIntInput)
iterLabel = ttk.Label(inputsFrame, text="Iterations:")
iterLabel.grid(row=8, column=0, sticky=tk.W)
iterationEntry = ttk.Entry(
inputsFrame, width="30", validate="key", validatecommand=(vcmd, "%P"))
iterationEntry.grid(row=9, column=0, sticky=tk.W)
# --------------------------------------------------------------------------------------------
# progress bar
progressBar = ttk.Progressbar(
    outputsFrame, orient="horizontal", length=550, mode="indeterminate")
# --------------------------------------------------------------------------------------------
# cancel button
btnCancel = ttk.Button(outputsFrame, text="Exit", width=8,
                       command=lambda: sys.exit(0))
btnCancel.grid(row=13, column=3, sticky=tk.E, pady=10)

btnOpImage = ttk.Button()

def operationTypeChanged():
    text = opTypeStr.get()
    if text == "encrypt":
        transformedImageLabel.config(text="Encrypted Image Path:")
        iterLabel.grid(row=8, column=0, sticky=tk.W)
        iterationEntry.grid(row=9, column=0, sticky=tk.W)
    else:
        transformedImageLabel.config(text="Decrypted Image Path:")
        iterationEntry.grid_remove()
        iterLabel.grid_remove()

    # encrypt/decrypt button
    btnOpImage = ttk.Button(inputsFrame, text=text, width=8,
                                command=lambda: Rubik())
    btnOpImage.grid(row=1, column=2)

def selectOriginalImage():
    """Open an image from a directory"""
    # Select the Imagename  from a folder
    tk.Tk().withdraw()
    global originalImagePath
    originalImagePath = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                ("Image Files", ".png .jpg .jpeg .svg")])
    originalImagePathEntry.delete(0, tk.END)
    originalImagePathEntry.insert(tk.INSERT, originalImagePath)  
    print(type(originalImagePath))  
    # opens the image
    img = Image.open(originalImagePath)
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((100, 100), Image.ANTIALIAS)    
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)    
    # create a label
    panel = ttk.Label(imageFrame, image=img)   
    # set the image as img
    panel.image = img
    panel.grid(row=1, column=0, padx=5)
    # try:
    #     btnOpImage["state"] = "normal"
    # except:
    #     pass

def selectTransformedImage():
    """Open an image from a directory"""
    # Select the Imagename  from a folder
    tk.Tk().withdraw()
    global transformedImagePath
    transformedImagePath = filedialog.askopenfilename(title="Open Image", filetypes=[
                                                ("Image Files", ".png .jpg .jpeg .svg")])
    transformedImagePathEntry.delete(0, tk.END)
    transformedImagePathEntry.insert(tk.INSERT, transformedImagePath)
    # try:
    #     btnOpImage["state"] = "normal"
    # except:
    #     pass 

def selectKeyPath():
    tk.Tk().withdraw()
    global keyPath
    keyPath = filedialog.askopenfilename(title="Open Key", filetypes=[
                                           ("JSON Files", ".json")])
    keyPathEntry.delete(0, tk.END)
    keyPathEntry.insert(tk.INSERT, keyPath)

def Rubik():
    # image = read_image(originalImagePath)
    rubik = Cubik(originalImagePath)
    if opTypeStr.get() == "encrypt":  
        global iter_max
        iter_max = int(iterationEntry.get())
        rubik.encrypt(transformedImagePath, iter_max, keyPath)
        # dict_key = create_key(image, iter_max)
        # save_key(dict_key, keyPath)
        # transformed_image = encrypt_image(image, keyPath)
    else: 
        rubik.decrypt(transformedImagePath, keyPath)
    #     transformed_image = decrypt_image(image, keyPath)
    # save_image(transformed_image, transformedImagePath)

    img = Image.open(transformedImagePath)
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((100, 100), Image.ANTIALIAS)    
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)    
    # create a label
    panel = ttk.Label(imageFrame, image=img)   
    # set the image as img
    panel.image = img
    panel.grid(row=1, column=1, padx=5)

# def checkFields():
#     return True if (iterationEntry.get()) else False

operationTypeChanged()
root.mainloop()