# from skimage.metrics import structural_similarity as ssim
# from skimage.metrics import peak_signal_noise_ratio as psnr
# from skimage.metrics import normalized_mutual_information as nmi

# import matplotlib.pyplot as plt
# import numpy as np
# from skimage import img_as_float, io

# # загрузка оригинального и восстановленного изображений
# original = img_as_float(io.imread('../Images/taj.png', as_gray=False))
# reconstructed = img_as_float(io.imread('../Images/decrypted_image.png', as_gray=False))
# wind_size = original.min() - 1 if original.min() % 2 == 0 else original.min()

# # вычисление SSIM метрики
# ssim_score = ssim(original, reconstructed, win_size=wind_size)
# psnr_score = psnr(original, reconstructed, data_range=original.max() - original.min())
# nmi_score = nmi(original, reconstructed)

# # вывод результата
# print(f"SSIM: {ssim_score:.4f}")
# print(f"PSNR: {psnr_score:.2f} dB")
# print(f"NMI: {nmi_score:.4f}")


from skimage.metrics import structural_similarity
import cv2
import numpy as np

before = cv2.imread('../Images/taj.png')
after = cv2.imread('../Images/decrypted_image.png')

# Convert images to grayscale
before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images
(score, diff) = structural_similarity(before_gray, after_gray, full=True)
print("Image similarity", score)

# The diff image contains the actual image differences between the two images
# and is represented as a floating point data type in the range [0,1] 
# so we must convert the array to 8-bit unsigned integers in the range
# [0,255] before we can use it with OpenCV
diff = (diff * 255).astype("uint8")

# Threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.drawContours(mask, [c], 0, (0,255,0), -1)
        cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

cv2.imshow('before', before)
cv2.imshow('after', after)
cv2.imshow('diff',diff)
cv2.imshow('mask',mask)
cv2.imshow('filled after',filled_after)
cv2.waitKey(0)