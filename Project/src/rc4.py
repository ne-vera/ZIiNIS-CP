from PIL import Image
from scipy import misc
import imageio
import binascii

def get_image(image_path):
    return imageio.imread(image_path)

# If Flag is one , display image, else do not display
def save_image(image, shape,flag, file_name):
    img = Image.fromarray((image.reshape(shape)).astype('uint8'), 'RGB')
    if(flag == 1):
        img.show()
    img.save(file_name)

def get_s_array():
    """ Build initial S array """
    s_array = []
    for _ in range(0, 256):
        s_array.append(_)
    return s_array


def get_dec_key(key):
    """ Convert external key from string to decimal """
    hex_key = str(binascii.hexlify(key))
    dec_key = []

    for _ in range(len(hex_key)):
        dec_key.append(ord(hex_key[_]))
    return dec_key

def initial_perm(s, k):
    """ Initial permutation of array S using array U. """
    j = 0
    key_length = len(k)
    for i in range(256):
        j = (j + s[i] + k[i%key_length]) % 256
        s[i], s[j] = s[j], s[i]
    return s


def prga(s):
    """
    Pseudo Random Generation Algorithm

    :param s: Permuted S Array
    :return: random int value ranging from 0 - 255
    """
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = s[(s[i] + s[j]) % 256]
        yield t

def rc4(s, u):
    s = initial_perm(s, u)
    return prga(s)

def rc4_encryption(sec_image_name, key, file_name):
    image = get_image(image_path=sec_image_name)
    print("Encrypting...")
    img_width, img_height = image.shape[:2]

    # Convert external key
    dec_key = get_dec_key(key)

    # Construct S Array
    s_array = get_s_array()

    ran_gen = rc4(s_array, dec_key)

    for i in range(img_width):
        for j in range(img_height):
            pixel = image[i, j]
            t = next(ran_gen)
            red = (pixel[0] + t) % 256
            t = next(ran_gen)
            green = (pixel[1] + t) % 256
            t = next(ran_gen)
            blue = (pixel[2] + t) % 256
            image[i, j] = (red, green, blue)

    save_image(image, shape=image.shape, flag = 0, file_name = file_name)
    print("Completed")

def rc4_decryption(encrypted_image_name, key, file_name):
    image = get_image(image_path=encrypted_image_name)

    print("Decrypting...")
    img_width, img_height = image.shape[:2]

    # Convert external key
    dec_key = get_dec_key(key)
    
    # Construct S Array
    s_array = get_s_array()

    ran_gen = rc4(s_array, dec_key)

    for i in range(img_width):
        for j in range(img_height):
            pixel = image[i, j]
            t = next(ran_gen)
            red = (pixel[0] + 256 - t) % 256
            t = next(ran_gen)
            green = (pixel[1] + 256 - t) % 256
            t = next(ran_gen)
            blue = (pixel[2] + 256 - t) % 256
            image[i, j] = (red, green, blue)

    save_image(image, shape=image.shape, flag = 1, file_name=file_name)
    print("Completed")

original_image = '../Images/taj.png'
encrypted_image = '../Images/encrypted_image.png'
decrypted_image = '../Images/decrypted_image.png'
key = '111'.encode()

# rc4_encryption(original_image, key, encrypted_image)
rc4_decryption(encrypted_image, key, decrypted_image)