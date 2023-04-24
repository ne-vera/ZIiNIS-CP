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

class Rubik():
    def __init__(self, image_path) -> None:
        with Image.open(image_path, mode='r') as img:
            self.image = img.convert('RGB')
        self.pix = self.image.load()
        self.m = self.image.size[0]
        self.n = self.image.size[1]
        self.initialize_rgb()
    
    def initialize_rgb(self) -> None:
        self.r = []
        self.g = []
        self.b = []

        for i in range(self.m):
            self.r.append([])
            self.g.append([])
            self.b.append([])
            for j in range(self.n):
                rgb_per_pixel = self.pix[i,j]
                self.r[i].append(rgb_per_pixel[0])
                self.g[i].append(rgb_per_pixel[1])
                self.b[i].append(rgb_per_pixel[2])

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
    
    def load_key(self, key_path: str) -> None:
        with open(key_path, 'r') as F:
            dict_key = json.load(F)

        self.Kr = dict_key['Kr']
        self.Kc = dict_key['Kc']
        self.iter_max = dict_key['iter_max']

    def roll_row(self, encryption_flag : bool) -> None:
        direction_coef = 1 if encryption_flag else -1
        for i in range(self.m):
                r_modulus = sum(self.r[i]) % 2
                g_modulus = sum(self.g[i]) % 2
                b_modulus = sum(self.b[i]) % 2
                self.r[i] = np.roll(self.r[i], -direction_coef * self.Kr[i]) if r_modulus else np.roll(self.r[i], direction_coef * self.Kr[i])
                self.g[i] = np.roll(self.g[i], -direction_coef * self.Kr[i]) if g_modulus else np.roll(self.g[i], direction_coef * self.Kr[i])
                self.b[i] = np.roll(self.b[i], -direction_coef * self.Kr[i]) if b_modulus else np.roll(self.b[i], direction_coef * self.Kr[i])
    
    def roll_column(self, encryption_flag: bool) -> None:
        direction_coef = 1 if encryption_flag else -1
        for i in range(self.n):
                r_sum = 0
                g_sum = 0
                b_sum = 0
                for j in range(self.m):
                    r_sum += self.r[j][i]
                    g_sum += self.g[j][i]
                    b_sum += self.b[j][i]
                r_modulus = r_sum % 2
                g_modulus = g_sum % 2
                b_modulus = b_sum % 2
                self.r = columnshift(self.r, i, - direction_coef * self.Kc[i]) if r_modulus else columnshift(self.r, i, direction_coef * self.Kc[i])
                self.g = columnshift(self.g, i, - direction_coef * self.Kc[i]) if g_modulus else columnshift(self.g, i, direction_coef * self.Kc[i])
                self.b = columnshift(self.b, i, - direction_coef * self.Kc[i]) if b_modulus else columnshift(self.b, i, direction_coef * self.Kc[i])
    
    def xor_pixels(self) -> None:
        for i in range(self.m):
            for j in range(self.n):
                row_xor_operand = self.Kc[j] if i%2==1 else rotate(self.Kc[j])
                column_xor_operand = self.Kr[i] if j%2==0 else rotate(self.Kr[j])
                self.r[i][j] = self.r[i][j] ^ row_xor_operand ^ column_xor_operand
                self.g[i][j] = self.g[i][j] ^ row_xor_operand ^ column_xor_operand
                self.b[i][j] = self.b[i][j] ^ row_xor_operand ^ column_xor_operand
        
    def encrypt(self, encrypted_image: str, iter_max : int, key_path : str) -> None:
        self.create_key(iter_max, key_path)
        for iter in range(self.iter_max):
            self.roll_row(encryption_flag=True)
            self.roll_column(encryption_flag=True)
            self.xor_pixels()
        for i in range(self.m):
            for j in range(self.n):
                self.pix[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])
        self.image.save(encrypted_image)
    
    def decrypt(self, decrypted_image : str, key_path : str) -> None:
        self.load_key(key_path)
        for iter in range(self.iter_max):
            self.xor_pixels()
            self.roll_column(encryption_flag=False)
            self.roll_row(encryption_flag=False)
        for i in range(self.m):
            for j in range(self.n):
                self.pix[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])
        self.image.save(decrypted_image)


# key_path = '../Keys/key.json'
# encrypted_image = '../Images/encrypted_image.png'
# decrypted_image = '../Images/decrypted_image.png'

# rubik = Rubik(r'../Images/taj.png')
# rubik.encrypt(encrypted_image, 1, key_path)
# rubik = Rubik(encrypted_image)
# rubik.decrypt(decrypted_image, key_path)