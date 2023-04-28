import numpy as np
import cv2 
import os
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import random
from PIL import Image
import timeit
     

def to_Matrix(image):
    img = Image.open(image) 
    color = 1
    pixelVal = img.load()
    if type(pixelVal[0,0]) == int:
      color = 0
    imgmatrix = []
    imagesize = img.size 
    for width in range(int(imagesize[0])):
        row = []
        for height in range(int(imagesize[1])):
                row.append((pixelVal[width,height]))
        imgmatrix.append(row)
    return imgmatrix,imagesize[0],color
     
# Arnold Cat Chaos Mapping
# Function Used: (x,y) = ((x + y) mod n, (x + 2y) mod n)
def Arnold_encryption(image, key, encrypted_image_path):
    img = cv2.imread(image)
    r, c, co = img.shape
    e_img = img
    for i in range (0,key):
        new_image = np.zeros([r, c, co])
        for x in range(0, r):
            for y in range(0, c):
                new_image[x][y] = e_img[(x+y)%r][(x+2*y)%c]  
        e_img = new_image
    cv2.imwrite(encrypted_image_path, e_img)
    return e_img

def Arnold_decryption(image, key, decrypted_image_path):
    img = cv2.imread(image)
    r, c, ch = img.shape
    dim = r
    limit = dim
    if (dim%2==0) and 5**int(round(math.log(dim/2,5))) == int(dim/2):
        limit = 3*dim
    elif 5**int(round(math.log(dim,5))) == int(dim):
        limit = 2*dim
    elif (dim%6==0) and  5**int(round(math.log(dim/6,5))) == int(dim/6):
        limit = 2*dim
    else:
        limit = int(12*dim/7)
    for i in range(key,limit):
        r, c, ch = img.shape
        n = r
        new_image = np.zeros([r, c, ch])
        for x in range(0, r):
            for y in range(0, c):
                new_image[x][y] = img[(x+y)%n][(x+2*y)%n]  
        img = new_image
    cv2.imwrite(decrypted_image_path,img)
    return img
    

# Henon Chaos Mapping
def generate_Henon_map(dim, key):
    x = key[0]
    y = key[1]
    seqSize = dim * dim * 8
    bits = []
    decArray = []
    HMatrix = []
    for i in range(seqSize):
        xi = y + 1 - 1.4 * x**2
        yi = 0.3 * x

        x = xi
        y = yi
        if xi <= 0.4:
            bit = 0
        else:
            bit = 1
        bits.append(bit)
        if i % 8 == 7:
            decimal = 0
            for bit in bits:
                decimal = decimal * 2 + int(bit)           
            decArray.append(decimal)
            bits = []
        decArraySize = dim*8
        if i % decArraySize == decArraySize-1:
            HMatrix.append(decArray)
            decArray = []
    return HMatrix
     

def Henon_encryption(image,key, encrypted_image_path):
    imgMatrix, dim, iscolor = to_Matrix(image)
    transformMatrix = generate_Henon_map(dim, key)
    newMatrix = []
    for i in range(dim):
        row = []
        for j in range(dim):
            if iscolor:
                row.append(tuple([transformMatrix[i][j] ^ x for x in imgMatrix[i][j]]))
            else:
                row.append(transformMatrix[i][j] ^ imgMatrix[i][j])
        newMatrix.append(row)

    if iscolor:
      im = Image.new("RGB", (dim, dim))
    else: 
      im = Image.new("L", (dim, dim))

    pix = im.load()
    for x in range(dim):
        for y in range(dim):
            pix[x, y] = newMatrix[x][y]
    im.save(encrypted_image_path)
     

def Henon_decryption(imageEnc, key, decrypted_image_path):
    imgMatrix, dim, color = to_Matrix(imageEnc)
    transformMatrix = generate_Henon_map(dim, key)
    pil_im = Image.open(imageEnc, 'r')
    imshow(np.asarray(pil_im))
    henonDImage = []
    for i in range(dim):
        row = []
        for j in range(dim):
            if color:
                row.append(tuple([transformMatrix[i][j] ^ x for x in imgMatrix[i][j]]))
            else:
                row.append(transformMatrix[i][j] ^ imgMatrix[i][j])
        henonDImage.append(row)

    if color:
        im = Image.new("RGB", (dim, dim))
    else: 
        im = Image.new("L", (dim, dim)) # L is for Black and white pixels

    pix = im.load()
    for x in range(dim):
        for y in range(dim):
            pix[x, y] = henonDImage[x][y]
    im.save(decrypted_image_path)
     

     

# Combined Arnold+Henon Chaos Function

def Arnold_Henon_encryption(key1, key2, original_image_path, encrypted_image_path):
    AE = Arnold_encryption(original_image_path, key1, encrypted_image_path)
    Henon_encryption(encrypted_image_path, key2, encrypted_image_path)


def Arnold_Henon_decryption(key1, key2, encrypted_image_path, decrypted_image_path):
    Henon_decryption(encrypted_image_path, key2, decrypted_image_path)
    Arnold_DIm = Arnold_decryption(decrypted_image_path, key1, decrypted_image_path)


original_image =  '../Images/c10.png'
encrypted_image = '../Images/h_c10_encrypted.png'
decrypted_image = '../Images/_decrypted.png'


# start_time = timeit.default_timer()   
# key1 = 42
# key2 = (0.5,0.5)
     
# Arnold_Henon_encryption(key1, key2, original_image, encrypted_image)
# Arnold_Henon_decryption(key1, key2, encrypted_image, decrypted_image)

# key = 42
# Arnold_EIm = Arnold_encryption(original_image, key, encrypted_image)
# Arnold_DIm = Arnold_decryption(encrypted_image, key, decrypted_image)

key = (0.1,0.1)
Henon_encryption(original_image, key, encrypted_image)
Henon_decryption(encrypted_image, key, decrypted_image)

# ellapsed_time = timeit.default_timer() - start_time
# print(ellapsed_time)
