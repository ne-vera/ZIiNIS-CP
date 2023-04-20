from PIL import Image
import imageio
import binascii

def save_image(image, file_name, show=False):
    img = Image.fromarray(image.astype('uint8'), 'RGB')
    if show:
        img.show()
    img.save(file_name)

def get_s_array():
    """ Build initial S array """
    return [i for i in range(256)]

def get_dec_key(key):
    """ Convert external key from string to decimal """
    hex_key = binascii.hexlify(key).decode('utf-8')
    return [ord(c) for c in hex_key]

def initialize_s_array(s, k):
    """ Initialize array S using key K """
    j = 0
    key_length = len(k)
    for i in range(256):
        j = (j + s[i] + k[i % key_length]) % 256
        s[i], s[j] = s[j], s[i]

def generate_random_number(s):
    """
    Generate a random number using array S

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

def rc4_cipher(image_path, key, file_name, decrypt=False):
    image = imageio.imread(image_path)
    print("Encrypting..." if not decrypt else "Decrypting...")
    img_width, img_height = image.shape[:2]

    # Convert external key
    dec_key = get_dec_key(key)

    # Construct S Array
    s_array = get_s_array()

    # Initialize S Array using key
    initialize_s_array(s_array, dec_key)

    # Generate keystream
    ran_gen = generate_random_number(s_array)

    # Encrypt/Decrypt image
    for i in range(img_width):
        for j in range(img_height):
            pixel = image[i, j]
            t = next(ran_gen)
            r = (pixel[0] + (t if not decrypt else (256 - t))) % 256
            t = next(ran_gen)
            g = (pixel[1] + (t if not decrypt else (256 - t))) % 256
            t = next(ran_gen)
            b = (pixel[2] + (t if not decrypt else (256 - t))) % 256
            image[i, j] = (r, g, b)

    save_image(image, file_name, show = True)
    print("Completed")

original_image = '../Images/taj.png'
encrypted_image = '../Images/encrypted_image.png'
decrypted_image = '../Images/decrypted_image.png'

key = '111'.encode()

rc4_cipher(original_image, key, encrypted_image, decrypt=False)
rc4_cipher(encrypted_image, key, decrypted_image, decrypt=True)