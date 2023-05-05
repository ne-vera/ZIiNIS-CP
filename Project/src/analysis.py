import cv2
from PIL import Image
import math
import numpy as np
from matplotlib import pyplot as plt
import random
import skimage
from skimage.color import rgb2gray
from skimage.measure import shannon_entropy
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import img_as_float, io

original_paths = ['../Images/lena.png',
                  '../Images/Mandril.png',
                  '../Images/Peppers.png']

encrypted_paths = ['../Images/lena_encrypted.png',
                  '../Images/Mandril_encrypted.png',
                  '../Images/Peppers_encrypted.png']

def count_entropy():
    for path in original_paths:
        img = cv2.imread(path)
        entropy = skimage.measure.shannon_entropy(img)
        print(entropy)

    print("---------------------------------------------------------------")

    for path in encrypted_paths:
        img = cv2.imread(path)
        entropy = skimage.measure.shannon_entropy(img)
        print(entropy)

# count_entropy()

def change_pixel():
    num = 0
    for path in original_paths:
        original = cv2.imread(path, 0)
        cv2.imwrite('../Images/c1' + str(num) +'.png', original)
        print("pixel value at [0,0]:", original[0,0])   
        original[0,0] = 0 
        cv2.imwrite('../Images/c2' + str(num) +'.png', original)
        num +=1

# change_pixel()

def unified_average_changing_intensity(image_original, image_encrypted):
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    if len(image_original.shape) < 3:

        for h in range(height):
            sum_of_numbers = 0
            for w in range(width):
                if image_original[h][w] != image_encrypted[h][w]:
                    difference = int(image_original[h][w]) - int(image_encrypted[h][w])  # with int cast
                    sum_of_numbers += math.fabs(difference) / 255
        sum_of_all += sum_of_numbers
        result = sum_of_all / (height * width) * 100
        return result
    for channel in range(3):
        one_channel_original = image_original[:, :, channel]
        one_channel_encrypted = image_encrypted[:, :, channel]
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                difference = int(one_channel_original[h][w]) - int(one_channel_encrypted[h][w]) # with int cast
                sum_of_numbers += math.fabs(difference) / 255

        sum_of_all += sum_of_numbers
    average_sum = sum_of_all / 3
    result = average_sum / (height * width) * 100
    return result

def count_uaci():
    for num in range(len(encrypted_paths)):
        org = cv2.imread(original_paths[num])
        enc = cv2.imread(encrypted_paths[num])
        print(unified_average_changing_intensity(org, enc))

# count_uaci()

def rows_correlation(image, N):
    sum = 0
    for i in range(N):
        if i + 1 < image.shape[0]:
            if len(image.shape) < 3:
                x = image[:, i], image[:, i + 1]
                cor_coef = np.corrcoef(x)
                sum += cor_coef
            else:
                tmp_sum = 0
                for j in range(3):
                    x = image[i, :, j], image[i+1, :, j]
                    cor_coef = np.corrcoef(x)
                    tmp_sum += cor_coef
                sum += tmp_sum / 3
    return sum / N

def columns_correlation(image, N):
    sum = 0
    for i in range(N):
        if i + 1 < image.shape[0]:
            if len(image.shape) < 3:
                x = image[:, i], image[:, i + 1]
                cor_coef = np.corrcoef(x)
                sum += cor_coef
            else:
                tmp_sum = 0
                for j in range(3):
                    x = image[:, i, j], image[:, i + 1, j]
                    cor_coef = np.corrcoef(x)
                    tmp_sum += cor_coef
                sum += tmp_sum / 3
    return sum / N

def diagonal_correlation(image, N):
    sum = 0
    for i in range(N):
        if i + 1 < image.shape[0]:
            if len(image.shape) < 3:
                x = make_diagonal(image[:, :], i, 200), make_diagonal(image[:, :], i + 1, 200)
                cor_coef = np.corrcoef(x)
                sum += cor_coef
            else:
                tmp_sum = 0
                for j in range(3):
                    x = make_diagonal(image[:, :, j], i, 200), make_diagonal(image[:, :, j], i + 1, 200)
                    cor_coef = np.corrcoef(x)
                    tmp_sum += cor_coef
                sum += tmp_sum / 3

    return sum / N

def make_diagonal(image, iterator, N):
    diagonal_of_image = []
    for i in range(N):
        diagonal_of_image.append(image[i + iterator][i + iterator])

    return np.array(diagonal_of_image)

def get_all_correlations(image, N):
    print("rows correlation: ")
    # print(rows_correlation(image, N))
    print(np.average(rows_correlation(image, N)))
    print("columns corelation: ")
    print(np.average(columns_correlation(image, N)))
    print("diagonal_correlation: ")
    print(np.average(diagonal_correlation(image, N)))

def count_correlations():
    num = 0
    for path in original_paths:
        print('\n' +  str(num) + '.')
        img = cv2.imread(path)
        # N = img.shape[0]
        N = 200
        get_all_correlations(img, N-1)
        num+=1

    print("---------------------------------------------------------------")

    num = 0
    for path in encrypted_paths:
        print('\n' +  str(num) + '.')
        img = cv2.imread(path)
        # N = img.shape[0]
        N = 300
        get_all_correlations(img, N-1)
        num+=1

# count_correlations()

def sumofpixel(height,width,img1, img2):
    matrix = np.empty([width, height])
    for y in range(0, height):
        for x in range(0, width):
            if img1[x,y] == img2[x,y]:
                matrix[x,y]=0
            else:
                matrix[x,y]=1
    
    psum = 0
    for y in range(0, height):
        for x in range(0, width):
            psum = matrix[x,y] + psum
    return psum

def npcrv():
    for num in range(len(encrypted_paths)):
        c1 = cv2.imread('../Images/r_c1' + str(num) +'_encrypted.png', 0)
        c2 = cv2.imread('../Images/r_c2' + str(num) +'_encrypted.png', 0)
        height = c1.shape[0]
        width = c1.shape[1]

        npcrv =((sumofpixel(height, width, c1, c2) / (height*width))*100)
        print(npcrv)

npcrv()