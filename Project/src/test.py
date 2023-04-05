import numpy as np
from PIL import Image
from random import randint
import json

def columnshift(a, index, n):
    col = []
    for i in range(len(a)):
        col.append(a[i][index])
    shift_col = np.roll(col, -n)
    for i in range(len(a)):
        a[i][index] = shift_col[i]
    return a

def rotate(n):
    bits = '{0:b}'.format(n)
    return int(bits[::-1], 2)

class Encryptor():
    def __init__(self, image_path) -> None:
        self.image = Image.open(image_path)
        self.pix = self.image.load()
        self.m = self.image.size[0]
        self.n = self.image.size[1]

    def create_key(self, iter_max : int, key_path : str, alpha : int = 8):
        self.Kr = [randint(0, 2 ** alpha - 1) for i in range(self.m)]
        self.Kc = [randint(0, 2 ** alpha - 1) for i in range(self.n)]
        self.iter_max = iter_max

        dict_key = {
            'Kr': self.Kr,
            'Kc': self.Kc,
            'iter_max' : self.iter_max
        }

        with open(key_path, 'w') as F:
            json.dump(dict_key, F, indent=4)
    
    def encrypt(self, key_path: str, encrypted_image: str, iter_max: int):
        self.create_key(iter_max, key_path)

        r = []
        g = []
        b = []

        for i in range(self.m):
            r.append([])
            g.append([])
            b.append([])
            for j in range(self.n):
                rgb_per_pixel = self.pix[i,j]
                r[i].append(rgb_per_pixel[0])
                g[i].append(rgb_per_pixel[1])
                b[i].append(rgb_per_pixel[2])
        
        for iter in range(iter_max):
            # For each row
            for i in range(self.m):
                r_modulus = sum(r[i]) % 2
                g_modulus = sum(g[i]) % 2
                b_modulus = sum(b[i]) % 2
                r[i] = np.roll(r[i], -self.Kr[i]) if r_modulus else np.roll(r[i], self.Kr[i])
                g[i] = np.roll(g[i], -self.Kr[i]) if g_modulus else np.roll(g[i], self.Kr[i])
                b[i] = np.roll(b[i], -self.Kr[i]) if b_modulus else np.roll(b[i], self.Kr[i])
            
            # For each column
            for i in range(self.n):
                r_sum = 0
                g_sum = 0
                b_sum = 0
                for j in range(self.m):
                    r_sum += r[j][i]
                    g_sum += g[j][i]
                    b_sum += b[j][i]
                r_modulus = r_sum % 2
                g_modulus = g_sum % 2
                b_modulus = b_sum % 2
                r = columnshift(r, i, -self.Kc[i]) if r_modulus else columnshift(r, i, self.Kc[i])
                g = columnshift(g, i, -self.Kc[i]) if g_modulus else columnshift(g, i, self.Kc[i])
                b = columnshift(b, i, -self.Kc[i]) if b_modulus else columnshift(b, i, self.Kc[i])
                        
            # For each row
            for i in range(self.m):
                for j in range(self.n):
                    if(i%2==1):
                        r[i][j] = r[i][j] ^ self.Kc[j]
                        g[i][j] = g[i][j] ^ self.Kc[j]
                        b[i][j] = b[i][j] ^ self.Kc[j]
                    else:
                        r[i][j] = r[i][j] ^ rotate(self.Kc[j])
                        g[i][j] = g[i][j] ^ rotate(self.Kc[j])
                        b[i][j] = b[i][j] ^ rotate(self.Kc[j])
            # For each column            
            for j in range(self.n):
                for i in range(self.m):
                    if(j%2==0):
                        r[i][j] = r[i][j] ^ self.Kr[i]
                        g[i][j] = g[i][j] ^ self.Kr[i]
                        b[i][j] = b[i][j] ^ self.Kr[i]
                    else:
                        r[i][j] = r[i][j] ^ rotate(self.Kr[i])
                        g[i][j] = g[i][j] ^ rotate(self.Kr[i])
                        b[i][j] = b[i][j] ^ rotate(self.Kr[i])
            
        for i in range(self.m):
            for j in range(self.n):
                self.pix[i,j] = (r[i][j], g[i][j], b[i][j])
        self.image.save(encrypted_image)
     
class Decryptor():
    def __init__(self, image_path) -> None:
        self.image = Image.open(image_path)
        self.pix = self.image.load()
        self.m = self.image.size[0]
        self.n = self.image.size[1]

    def load_key(self, key_path: str) -> None:
        with open(key_path, 'r') as F:
            dict_key = json.load(F)

        self.Kr = dict_key['Kr']
        self.Kc = dict_key['Kc']
        self.iter_max = dict_key['iter_max']
    
    def decrypt(self, key_path: str, decrypted_image : str):
        self.load_key(key_path)

        r = []
        g = []
        b = []

        for i in range(self.m):
            r.append([])
            g.append([])
            b.append([])
            for j in range(self.n):
                rgb_per_pixel = self.pix[i,j]
                r[i].append(rgb_per_pixel[0])
                g[i].append(rgb_per_pixel[1])
                b[i].append(rgb_per_pixel[2])

        for iter in range(self.iter_max):
             # For each column            
            for j in range(self.n):
                for i in range(self.m):
                    if(j%2==0):
                        r[i][j] = r[i][j] ^ self.Kr[i]
                        g[i][j] = g[i][j] ^ self.Kr[i]
                        b[i][j] = b[i][j] ^ self.Kr[i]
                    else:
                        r[i][j] = r[i][j] ^ rotate(self.Kr[i])
                        g[i][j] = g[i][j] ^ rotate(self.Kr[i])
                        b[i][j] = b[i][j] ^ rotate(self.Kr[i])
            
            # For each row
            for i in range(self.m):
                for j in range(self.n):
                    if(i%2==1):
                        r[i][j] = r[i][j] ^ self.Kc[j]
                        g[i][j] = g[i][j] ^ self.Kc[j]
                        b[i][j] = b[i][j] ^ self.Kc[j]
                    else:
                        r[i][j] = r[i][j] ^ rotate(self.Kc[j])
                        g[i][j] = g[i][j] ^ rotate(self.Kc[j])
                        b[i][j] = b[i][j] ^ rotate(self.Kc[j])
            
            # For each column
            for i in range(self.n):
                r_sum = 0
                g_sum = 0
                b_sum = 0
                for j in range(self.m):
                    r_sum += r[j][i]
                    g_sum += g[j][i]
                    b_sum += b[j][i]
                r_modulus = r_sum % 2
                g_modulus = g_sum % 2
                b_modulus = b_sum % 2
                r = columnshift(r, i, self.Kc[i]) if r_modulus else columnshift(r, i, -self.Kc[i])
                g = columnshift(g, i, self.Kc[i]) if g_modulus else columnshift(g, i, -self.Kc[i])
                b = columnshift(b, i, self.Kc[i]) if b_modulus else columnshift(b, i, -self.Kc[i])

            # For each row
            for i in range(self.m):
                r_modulus = sum(r[i]) % 2
                g_modulus = sum(g[i]) % 2
                b_modulus = sum(b[i]) % 2
                r[i] = np.roll(r[i], self.Kr[i]) if r_modulus else np.roll(r[i], -self.Kr[i])
                g[i] = np.roll(g[i], self.Kr[i]) if g_modulus else np.roll(g[i], -self.Kr[i])
                b[i] = np.roll(b[i], self.Kr[i]) if b_modulus else np.roll(b[i], -self.Kr[i])
            
        for i in range(self.m):
            for j in range(self.n):
                self.pix[i,j] = (r[i][j], g[i][j], b[i][j])
        self.image.save(decrypted_image)



key_path = '../Keys/key.json'
encrypted_image = '../Images/encrypted_image.bmp'
decrypted_image = '../Images/decrypted_image.bmp'
rubik = Encryptor(r'../Images/taj.bmp')
rubik.encrypt(key_path, encrypted_image, 1)

dec = Decryptor(encrypted_image)
dec.decrypt(key_path, decrypted_image)