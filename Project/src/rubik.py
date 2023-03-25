from PIL import Image
import random
import numpy as np
import json
import numpy as np

def upshift(a, index, n):
  '''
  Shift the collumn with index with numpy.roll(collumn, -n)
  '''
  col = a[:, index]
  shift_col = np.roll(col, -n)
  for i in range(len(a)):
    a[i][index] = shift_col[i]
  return a

def downshift(a, index, n):
  '''
  Shift the collumn with index with numpy.roll(collumn, n)
  '''
  col = a[:, index]
  shift_col = np.roll(col, n)
  for i in range(len(a)):
    a[i][index] = shift_col[i]
  return a

def rotate(n):
  '''
  Rotate 180 the binary bit string of n and convert to integer
  '''
  bits = "{0:b}".format(n)
  return int(bits[::-1], 2)

def read_image(image_path):
  image = Image.open(image_path)
  image = image.convert('RGB')
  image = np.array(image)
  return image

def save_image(image, image_save_path):
  save_img = Image.fromarray(image)
  save_img = save_img.save(image_save_path)
  return
     
# alpha
def create_key(image, ITER_MAX, alpha=8):
    # Create vector Kr and Kc
    Kr = [random.randint(0, 2 ** alpha - 1) for i in range(image.shape[0])]
    Kc = [random.randint(0, 2 ** alpha - 1) for i in range(image.shape[1])]

    dict_key = {"Kr": Kr,
                "Kc": Kc,
                "ITER": ITER_MAX
                }
    return dict_key

def save_key(dict_key, save_path):
  with open(save_path, "w") as F:
    json.dump(dict_key, F, indent=4)

def load_key(save_path):
    with open(save_path, "r") as F:
        dict_key = json.load(F)

    Kr = dict_key["Kr"]
    Kc = dict_key["Kc"]
    ITER_MAX = dict_key["ITER"]
    return Kr, Kc, ITER_MAX

def encrypt_image(image, key_path):
  # Load Key
  Kr, Kc, ITER_MAX = load_key(key_path)

  # Split channels
  r = np.array(image[:, :, 0])
  g = np.array(image[:, :, 1])
  b = np.array(image[:, :, 2])

  for iter in range(ITER_MAX):
    # For each row
    for i in range(image.shape[0]):
      r_modulus = sum(r[i]) % 2 
      g_modulus = sum(g[i]) % 2
      b_modulus = sum(b[i]) % 2
      r[i] = np.roll(r[i], -Kr[i]) if r_modulus else np.roll(r[i], Kr[i])
      g[i] = np.roll(g[i], -Kr[i]) if g_modulus else np.roll(g[i], Kr[i])
      b[i] = np.roll(b[i], -Kr[i]) if b_modulus else np.roll(b[i], Kr[i])
  
    # For each column 
    for i in range(image.shape[1]):
      r_modulus = sum(r[:, i]) % 2
      g_modulus = sum(g[:, i]) % 2
      b_modulus = sum(b[:, i]) % 2
      r = downshift(r, i, Kc[i]) if r_modulus else upshift(r, i, Kc[i])
      g = downshift(g, i, Kc[i]) if g_modulus else upshift(g, i, Kc[i])
      b = downshift(b, i, Kc[i]) if b_modulus else upshift(b, i, Kc[i])

    # For each row
    for i in range(image.shape[0]):
      for j in range(image.shape[1]):
        if(i%2==1):
          r[i][j] = r[i][j] ^ Kc[j]
          g[i][j] = g[i][j] ^ Kc[j]
          b[i][j] = b[i][j] ^ Kc[j]
        else:
          r[i][j] = r[i][j] ^ rotate(Kc[j])
          g[i][j] = g[i][j] ^ rotate(Kc[j])
          b[i][j] = b[i][j] ^ rotate(Kc[j])
  # For each column
    for j in range(image.shape[1]):
      for i in range(image.shape[0]):
        if(j%2==0):
          r[i][j] = r[i][j] ^ Kr[i]
          g[i][j] = g[i][j] ^ Kr[i]
          b[i][j] = b[i][j] ^ Kr[i]
        else:
          r[i][j] = r[i][j] ^ rotate(Kr[i])
          g[i][j] = g[i][j] ^ rotate(Kr[i])
          b[i][j] = b[i][j] ^ rotate(Kr[i])
  
  encrypted_img = np.stack((r,g,b), axis=2)
  return encrypted_img

def decrypt_image(encrypted_image, key_path):
  # Load key
  Kr, Kc, ITER_MAX = load_key(key_path)

  # Split channels
  r = np.array(encrypted_image[:, :, 0])
  g = np.array(encrypted_image[:, :, 1])
  b = np.array(encrypted_image[:, :, 2])

  for iteration in range(ITER_MAX):
    # For each column
    for j in range(encrypted_image.shape[1]):
      for i in range(encrypted_image.shape[0]):
        if(j%2==0): 
          r[i][j] = r[i][j] ^ Kr[i]
          g[i][j] = g[i][j] ^ Kr[i]
          b[i][j] = b[i][j] ^ Kr[i]
        else:
          r[i][j] = r[i][j] ^ rotate(Kr[i])
          g[i][j] = g[i][j] ^ rotate(Kr[i])
          b[i][j] = b[i][j] ^ rotate(Kr[i])
  
    # For each row
    for i in range(encrypted_image.shape[0]):
      for j in range(encrypted_image.shape[1]):
        if(i%2==1):
          r[i][j] = r[i][j] ^ Kc[j]
          g[i][j] = g[i][j] ^ Kc[j]
          b[i][j] = b[i][j] ^ Kc[j]
        else:
          r[i][j] = r[i][j] ^ rotate(Kc[j])
          g[i][j] = g[i][j] ^ rotate(Kc[j])
          b[i][j] = b[i][j] ^ rotate(Kc[j])

    # For each column 
    for i in range(encrypted_image.shape[1]):
      r_modulus = sum(r[:, i]) % 2
      g_modulus = sum(g[:, i]) % 2
      b_modulus = sum(b[:, i]) % 2
      r = upshift(r, i, Kc[i]) if r_modulus else downshift(r, i, Kc[i])
      g = upshift(g, i, Kc[i]) if g_modulus else downshift(g, i, Kc[i])
      b = upshift(b, i, Kc[i]) if b_modulus else downshift(b, i, Kc[i])

    # For each row
    for i in range(encrypted_image.shape[0]):
      r_modulus = sum(r[i]) % 2 
      g_modulus = sum(g[i]) % 2
      b_modulus = sum(b[i]) % 2
      r[i] = np.roll(r[i], Kr[i]) if r_modulus else np.roll(r[i], -Kr[i])
      g[i] = np.roll(g[i], Kr[i]) if g_modulus else np.roll(g[i], -Kr[i])
      b[i] = np.roll(b[i], Kr[i]) if b_modulus else np.roll(b[i], -Kr[i])
  
  decrypted_img = np.stack((r, g, b), axis=2)
  return decrypted_img

image_path = "../Images/lena.jpg"
key_path = "../Keys/key.json"
encrypted_path = "../Images/encrypted_image.jpg"
decrypted_path = "../Images/decrypted_image.jpg"

image = read_image(image_path)
dict_key = create_key(image, ITER_MAX=1)
save_key(dict_key, save_path=key_path)
en_image = encrypt_image(image, key_path)
save_image(en_image, encrypted_path)

encrypted_image = read_image(encrypted_path)
# encrypted_image = en_image
de_img = decrypt_image(encrypted_image,key_path)
save_image(de_img, decrypted_path)