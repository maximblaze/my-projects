from astropy.io import fits
import matplotlib.pyplot as plt
from termcolor import colored
import os
import numpy as np

path = 'FITS'
list_of_OCC_FITS = []
list_of_colours = 100000*['-', '--', 'g', 'r', 'c', 'k', 'm', 'y', 'x', 'b']
list_of_labels = []
with open('OCC.txt', 'r') as fileOCC:
    lines = fileOCC.readlines()
    for filename in os.listdir(path):
        for line in lines:
            if line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6] in filename:
                list_of_OCC_FITS.append('FITS/'+str(filename))


for filelabel in list_of_OCC_FITS:
    list_of_labels.append(filelabel[14]+filelabel[15]+filelabel[16]+filelabel[17]+filelabel[18]+filelabel[19]+filelabel[20])





p = []

for i in range(1, 384):
        p.append(i)

A = -0.548
B = 315.5

wl = []
for number in p:
    wl.append(A * number + B)

plt.figure()
plt.grid(True)
plt.title('Очищенный солнечный спектр 2007-2014')
plt.xlabel('Длина волны, нм')
plt.ylabel('Интенсивность излучения')
for fits_file in range(len(list_of_OCC_FITS)):
    hdu_list = fits.open(list_of_OCC_FITS[fits_file])
    data = hdu_list[0].data
    array = data[2]
    pixels1 = []
    Sdark = []
    for number in p:
        for measurement in range(len(array)):
            height = array[measurement][768]
            if 0 < height < 50:
                pixel = array[measurement][number]
                pixels1.append(pixel)
        Sdark.append((np.mean(pixels1)))
        pixels1.clear()

    pixels2 = []
    Ssun = []
    for number in p:
        for measurement in range(len(array)):
            height = array[measurement][768]
            if 170 < height < 200:
                pixel = array[measurement][number]
                pixels2.append(pixel)
        Ssun.append((np.mean(pixels2)))
        pixels2.clear()

    S0 = []
    for i in range(len(Ssun)):
            S0.append(Ssun[i]-Sdark[i])
    plt.plot(wl, S0, str(list_of_colours[fits_file]), label=str(list_of_labels[fits_file]))
    plt.legend(loc='best')
plt.savefig('S0')



"""
-0.68481237
-1.6717739







"""





