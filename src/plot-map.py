import numpy as np


if __name__ == '__main__':
    distances = np.matrix(
        [[0, 461, 451, 373],
        [461, 0, 486, 273],
        [451, 486, 0, 273],
        [373, 273, 273, 0]])

    coordinates = np.empty([4, 4])
    for i in range(0, 4):
        for j in range(0, 4):
            a = distances[0,j]**2 + distances[i,0]**2 + distances[i,j]**2
            coordinates[i,j]=a/2

    
    print()