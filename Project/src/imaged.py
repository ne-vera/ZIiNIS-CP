from __future__ import division
import cv2
import numpy as np
from bitstring import BitArray
from grain import Grain
import time

class Images:
    def __init__(self, file, key, iv):
        #self.img_file = file
        self.img = cv2.imread(file, cv2.IMREAD_COLOR)
        self.row = self.img.shape[0]
        self.col = self.img.shape[1]

        self.grain = Grain(key, iv)

    def encrypt(self, outfile):
        for i in range(self.row):
            for j in range(self.col):
                # print("Proccessing pixel [{}][{}]".format(i, j))
                self.img[i][j] = self.grain.encrypt(self.img[i][j])

        cv2.imwrite(outfile, self.img)

    def decrypt(self, outfile):
        for i in range(self.row):
            for j in range(self.col):
                # print("Proccessing pixel [{}][{}]".format(i, j))
                self.img[i][j] = self.grain.decrypt(self.img[i][j])

        cv2.imwrite(outfile, self.img)



original_image = '../Images/taj.png'
encrypted_image = '../Images/encrypted_image.png'
decrypted_image = '../Images/decrypted_image.png'


# image = Images(original_image, "00000000000000000000", "0000000000000000")
# image.encrypt(encrypted_image)

image = Images(encrypted_image, "00000000000000000000", "0000000000000000")
image.decrypt(decrypted_image)


"""
img_file = 'cat.png'

img = cv2.imread(img_file, cv2.IMREAD_COLOR)
alpha_img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
gray_img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)

print type(img)
print 'RGB shape: ', img.shape
print 'ARGB shape: ', alpha_img.shape
print 'Gray shape: ', gray_img.shape
print 'img.dtype: ', img.dtype
print 'img.size: ', img.size

KEY = BitArray("0x00000000000000000000")
#print "Key : ", KEY.hex
KEY.byteswap()
KEY = map(int, KEY.bin)

IV = BitArray("0x0000000000000000")
#print "IV : ", IV.hex
IV.byteswap()
IV = map(int, IV.bin)

grain = Grain(KEY, IV)

#print img[0][0][2]

print "Sebelum"
c = []


for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        print "Proccessing pixel {} {}".format(i, j)
        #print img[i][j]
        #c.append(deepcopy(img[i][j]))
        #print c
        img[i][j] = grain.encrypt(img[i][j])
        #for k in range(len(img[i][j])):
            #print img[i][j][k]
            #cipher = grain.encrypt(np.asscalar(img[i][j][k]))
            #cipher = '0b' + ''.join(str(i) for i in cipher)
            #cipher = BitArray(cipher)
            #cipher.byteswap()
            #img[i][j][k] = cipher
            #img[i][j][k] -= 10
        #print img[i][j]

cv2.imwrite("tes.png", img)


img_decrypt = 'tes.png'
img_cipher = cv2.imread(img_decrypt, cv2.IMREAD_COLOR)
print "Sesudah"

d = []
# Decryp test
grain = Grain(KEY, IV)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        print "Proccessing pixel {} {}".format(i, j)
        img_cipher[i][j] = grain.decrypt(img_cipher[i][j])
        #print img_cipher[i][j]
        #for k in range(len(img_cipher[i][j])):
        #    plain = grain.decrypt(np.asscalar(img_cipher[i][j][k]))
            #plain = '0b' + ''.join(str(i) for i in plain)
            #plain = BitArray(plain)
            #plain.byteswap()
        #    img_cipher[i][j][k] = plain
        #d.append(img_cipher[i][j])
            #img_cipher[i][j][k] += 10
        #print img_cipher[i][j]

cv2.imwrite("tes1.png", img_cipher)

#for i in range(len(c)):
#    for j in range(len(c[i])):
#        if c[i][j] != d[i][j]:
#            print "Failed ", i, j
#            break

#print c
#print d
"""