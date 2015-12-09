import matplotlib.image as mpli
import math
import numpy as np


class SeamCarver:
    # an RGB 2d array
    m_data = None
    row = 0 #y
    col = 0 #x
    energyMap = None
    abcd = None
    
    def __init__(self, imagePath):
        self.m_data = mpli.imread(imagePath)
        self.row = len(self.m_data)
        self.col = len(self.m_data[0])

    def saveImageAs(self, filename = "image.png"):
        mpli.imsave(full_path, self.m_data)

    # returns a grayscale image using the Matlab grayscale formula
    def toGrayscale(self):
        z = np.zeros((self.row, self.col, 3), dtype=np.uint8)
        for x in range (0, self.col): #x
            for y in range (0, self.row): #y
                g_rgb = 0.2989 * (float)(self.m_data[y][x][0]) + 0.5870 * (float)(self.m_data[y][x][1]) + 0.1140 * (float)(self.m_data[y][x][2])
                z[y][x][0] = g_rgb
                z[y][x][1] = g_rgb
                z[y][x][2] = g_rgb
        return z

    # returns a visual energy map; the lighter a pixel is, the higher energy it is
    def generateEnergyMap(self):
        if self.energyMap == None:
            self.generateEMap()
        z = np.zeros((self.row, self.col, 3), dtype=np.uint8)
        for x in range (0, self.col): #x
            for y in range (0, self.row): #y
                pixel_energy = np.uint8(self.energyMap[y][x])
                z[y][x][0] = pixel_energy
                z[y][x][1] = pixel_energy
                z[y][x][2] = pixel_energy
        return z

    # returns energy of specified pixel
    def energy(self, x, y):
        return math.sqrt((self.rgb2gray(x - 1, y) - self.rgb2gray((x + 1) % self.col, y))**2 + (self.rgb2gray(x, y - 1) - self.rgb2gray(x, (y + 1) % self.row))**2)
    
    # sets energyMap to a two dimensional array of energy values
    def generateEMap(self):
        self.energyMap = []
        for i in range (0, self.row):
            self.energyMap.append([])
            for j in range (0, self.col):
                self.energyMap[i].append(self.energy(j, i))

    # Matlab formula
    def rgb2gray(self, x, y):
        return 0.2989 * (int)(self.m_data[y][x][0]) + 0.5870 * (int)(self.m_data[y][x][1]) + 0.1140 * (int)(self.m_data[y][x][2])
    
    # Marks the lowest energy vertical seam in red
    def markVerticalSeam(self):
        seam = self.findVSeam()
        for i in range (0, self.row):
            self.m_data[i][seam[i]][0] = 255
            self.m_data[i][seam[i]][1] = 0
            self.m_data[i][seam[i]][2] = 0

    # Marks the lowest energy horizontal seam in red
    def markHorizontalSeam(self):
        seam = self.findHSeam()
        for i in range (0, self.col):
            self.m_data[seam[i]][i][0] = 255
            self.m_data[seam[i]][i][1] = 0
            self.m_data[seam[i]][i][2] = 0

    # find minimum vertical energy seam using [algorithm]
    # returns col indices in reverse row order (from bottom to top)
    def findVSeam(self):
        self.generateEMap()
        M = list(self.energyMap)
        # 0th row remains the same
        for row in range (1, self.row):
            M[row][0] += min(M[row - 1][0], M[row - 1][1])
            for col in range (1, self.col - 1):
                M[row][col] += min(M[row - 1][col - 1], M[row - 1][col], M[row - 1][col + 1])
            M[row][-1] += min(M[row - 1][-1], M[row - 1][-2])
        index_min = M[-1].index(min(M[-1]))
        vertical = []
        vertical.append(index_min)
        for row in range (self.row - 2, -1, -1):
            if index_min == 0:
                if M[row][index_min] > M[row][index_min + 1]:
                    index_min = index_min + 1
            elif index_min == self.col - 1:
                if M[row][index_min] > M[row][index_min - 1]:
                    index_min = index_min - 1
            else:
                if M[row][index_min] > M[row][index_min - 1]:
                    if M[row][index_min - 1] > M[row][index_min + 1]:
                        index_min = index_min + 1
                    else:
                        index_min = index_min - 1
                else:
                    if M[row][index_min] > M[row][index_min + 1]:
                        index_min = index_min + 1
            vertical.append(index_min)

        return vertical
    
    # returns the energy map with the 'x' and 'y' axis of the two dimensional array switched
    # facilitates the finding of horizontal seams
    def transposeEMap(self):
        transposed = []
        self.generateEMap()
        for i in range (0, self.col):
            transposed.append([])
            for j in range (0, self.row):
                transposed[i].append(self.energyMap[j][i])

        return transposed

    # finds and returns lowest energy horizontal seam using [algorithm]
    def findHSeam(self):
        M = list(self.transposeEMap())
        # 0th row remains the same
        for row in range (1, self.col):
            M[row][0] += min(M[row - 1][0], M[row - 1][1])
            for col in range (1, self.row - 1):
                M[row][col] += min(M[row - 1][col - 1], M[row - 1][col], M[row - 1][col + 1])
            M[row][-1] += min(M[row - 1][-1], M[row - 1][-2])
        index_min = M[-1].index(min(M[-1]))
        vertical = []
        vertical.append(index_min)
        for row in range (self.col - 2, -1, -1):
            if index_min == 0:
                if M[row][index_min] > M[row][index_min + 1]:
                    index_min = index_min + 1
            elif index_min == self.row - 1:
                if M[row][index_min] > M[row][index_min - 1]:
                    index_min = index_min - 1
            else:
                if M[row][index_min] > M[row][index_min - 1]:
                    if M[row][index_min - 1] > M[row][index_min + 1]:
                        index_min = index_min + 1
                    else:
                        index_min = index_min - 1
                else:
                    if M[row][index_min] > M[row][index_min + 1]:
                        index_min = index_min + 1
            vertical.append(index_min)

        return vertical
    
    # removes vertical seams from m_data by removing the pixels that compose the lowest energy seam
    def removeVSeam(self):
        seam = self.findVSeam()
        new_data = np.ndarray((self.row, self.col - 1, 3), np.uint8)
        for row in range (0, self.row):
            deleted = seam.pop()
            for i in range (0, deleted):
                new_data[row][i][0] = self.m_data[row][i][0]
                new_data[row][i][1] = self.m_data[row][i][1]
                new_data[row][i][2] = self.m_data[row][i][2]
            for i in range (deleted + 1, self.col):
                new_data[row][i - 1][0] = self.m_data[row][i][0]
                new_data[row][i - 1][1] = self.m_data[row][i][1]
                new_data[row][i - 1][2] = self.m_data[row][i][2]
        self.m_data = new_data
        self.col -= 1
    
    # removes horizontal seams from m_data by removing the pixels that compose the lowest energy seam
    def removeHSeam(self):
        seam = self.findHSeam()
        new_data = np.ndarray((self.row - 1, self.col, 3), np.uint8)
        for col in range (0, self.col):
            deleted = seam.pop()
            for i in range (0, deleted):
                new_data[i][col][0] = self.m_data[i][col][0]
                new_data[i][col][1] = self.m_data[i][col][1]
                new_data[i][col][2] = self.m_data[i][col][2]
            for i in range (deleted + 1, self.row):
                new_data[i - 1][col][0] = self.m_data[i][col][0]
                new_data[i - 1][col][1] = self.m_data[i][col][1]
                new_data[i - 1][col][2] = self.m_data[i][col][2]
        self.m_data = new_data
        self.row -= 1

    # adds vertical seams from m_data by duplicating the pixels that compose the lowest energy seam
    # and placing them adjacent to the seam
    def addVSeam(self):
        seam = self.findVSeam()
        new_data = np.ndarray((self.row, self.col + 1, 3), np.uint8)

        for row in range (0, self.row):
            added = seam.pop()
            for i in range (0, added + 1):
                new_data[row][i][0] = self.m_data[row][i][0]
                new_data[row][i][1] = self.m_data[row][i][1]
                new_data[row][i][2] = self.m_data[row][i][2]
            
            for i in range (added, self.col):
                new_data[row][i + 1][0] = self.m_data[row][i][0]
                new_data[row][i + 1][1] = self.m_data[row][i][1]
                new_data[row][i + 1][2] = self.m_data[row][i][2]

        self.m_data = new_data
        self.col += 1
    
    # adds horizontal seams from m_data by duplicating the pixels that compose the lowest energy seam
    # and placing them adjacent to the seam
    def addHSeam(self):
        seam = self.findHSeam()
        new_data = np.ndarray((self.row + 1, self.col, 3), np.uint8)
            
        for col in range (0, self.col):
            added = seam.pop()
            for i in range (0, added + 1):
                new_data[i][col][0] = self.m_data[i][col][0]
                new_data[i][col][1] = self.m_data[i][col][1]
                new_data[i][col][2] = self.m_data[i][col][2]
            
            for i in range (added, self.row):
                new_data[i + 1][col][0] = self.m_data[i][col][0]
                new_data[i + 1][col][1] = self.m_data[i][col][1]
                new_data[i + 1][col][2] = self.m_data[i][col][2]
    
        self.m_data = new_data
        self.row += 1
