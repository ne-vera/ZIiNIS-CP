from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import normalized_mutual_information as nmi

import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_float, io

# from grain import Grain
# from rc4 import rc4_cipher
# from rubik import Rubik

# загрузка оригинального и восстановленного изображений
original = img_as_float(io.imread('../Images/taj.png', as_gray=True))
reconstructed = img_as_float(io.imread('../Images/decrypted_image.png', as_gray=True))

# вычисление SSIM метрики
ssim_score = ssim(original, reconstructed, data_range=1.0)
psnr_score = psnr(original, reconstructed, data_range=1.0)
nmi_score = nmi(original, reconstructed)

# вывод результата
print(f"SSIM: {ssim_score:.4f}")
print(f"PSNR: {psnr_score:.2f} dB")
print(f"NMI: {nmi_score:.4f}")


original_image = '../Images/taj.png'
encrypted_image = '../Images/encrypted_image.png'
decrypted_image = '../Images/decrypted_image.png'

import cv2 
fig, ax = plt.subplots(2, 3, figsize=(20, 10))

for x, c in zip([0,1,2], ["r", "g", "b"]):
    xs = np.arange(256)
    ys = cv2.calcHist(original_image[:, :, x], [0], None, [256], [0,256])
    ax[0, x].plot(xs, ys.ravel(), color=c)
    ax[0, x].set_title("Ori_img-{}".format(c))

for x, c in zip([0,1,2], ["r", "g", "b"]):
    xs = np.arange(256)
    ys = cv2.calcHist(encrypted_image[:, :, x], [0], None, [256], [0,256])
    ax[1, x].plot(xs, ys.ravel(), color=c)
    ax[1, x].set_title("Enc_img-{}".format(c))

fig.show()