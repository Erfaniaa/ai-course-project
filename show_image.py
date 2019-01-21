import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import sleep

image1 = cv2.imread('stable.png', cv2.IMREAD_COLOR)
image2 = cv2.imread('wolf.png', cv2.IMREAD_COLOR)
image3 = cv2.imread('wood.png', cv2.IMREAD_COLOR)
image4 = cv2.imread('cow.png', cv2.IMREAD_COLOR)


f, axarr = plt.subplots(2, 2)
axarr[0, 0].imshow(image1)
plt.xticks([])
plt.yticks([])
axarr[0, 1].imshow(image2)
plt.xticks([])
plt.yticks([])
axarr[1, 0].imshow(image3)
plt.xticks([])
plt.yticks([])
axarr[1, 1].imshow(image4)
plt.xticks([])
plt.yticks([])


for i in range()
	cnt += 1
	pyplot.subplot(5, 12, cnt)
	pyplot.imshow(numpy.reshape(permutation, [2, 3]), interpolation=None, extent=[0, 3, 2, 0], cmap='gray')
	pyplot.xticks([])
	pyplot.yticks([])

pyplot.show()



plt.draw()

plt.pause(4)

axarr[0, 0].imshow(image4)
axarr[0, 1].imshow(image3)
axarr[1, 0].imshow(image2)
axarr[1, 1].imshow(image1)

plt.draw()
plt.pause(4)
