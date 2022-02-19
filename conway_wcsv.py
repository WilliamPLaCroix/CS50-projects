from random import randint
import sys
import csv


def main():

    if len(sys.argv) == 1:
        while (True):
            width = int(input('Please enter a width between 3 and 50 for our grid\n'))
            if width > 2 and width < 51:
                break
        while (True):
            height = int(input('Please enter a height between 3 and 50 for our grid\n'))
            if height > 2 and height < 51:
                break
        array = [[0 for x in range(width)] for y in range(height)]
        build_array(array, width, height)
    elif len(sys.argv) == 2:
        array = list(csv.reader(open(sys.argv[1])))
        width = len(array[0])
        height = len(array)
    elif len(sys.argv) == 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        array = [[0 for x in range(width)] for y in range(height)]
        build_array(array, width, height)
    elif len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        array = [[0 for x in range(width)] for y in range(height)]
        build_array(array, width, height, sys.argv[3])
    else:
        print('Usage: python FILENAME.py (PRESET.csv) OR (WIDTH HEIGHT r)')

    proceed = input('Press or hold enter to advance generations, enter any value to quit\n')
    while (True):
        for k in range(height):
            print(*array[k])
        run = input('')
        if run != '':
            break
        array = next_generation(array, width, height)
        if is_dead(array, width, height) == True:
            print('all cells dead, game over')
            return

    return


def build_array(array, width, height, random = ''):

    if random != 'r':
        random = input('Enter "r" for a random array, otherwise press enter to continue\n')
    if random != 'r':
        for i in range(height):
            for j in range(width):
                while (True):
                    value = input('Please enter either a space for an empty cell, or just press enter for a full cell\n')
                    if value == ' ' or value == '':
                        break
                if value == '':
                    array[i][j] = '#'
                else:
                    array[i][j] = value
    else:
        for i in range(height):
            for j in range(width):
                if randint(0, 1) == 1:
                    array[i][j] = '#'
                else:
                    array[i][j] = ' '
    return

def check_neighbors(array, i, j, width, height):

    neighbors = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if k == 0 and l == 0:
                continue
            elif i + k >= 0 and i + k < height and j + l >= 0 and j + l < width:
                if array[i + k][j + l] == '#':
                    neighbors += 1
    return neighbors


def is_dead(array, width, height):

    dead = True
    for i in range(height):
        for j in range(width):
            if array[i][j] == '#':
                dead = False
    return dead

def next_generation(array, width, height):

    temp_array = [[0 for x in range(width)] for y in range(height)]
    for i in range(height):
        for j in range(width):
            neighbors = check_neighbors(array, i, j, width, height)
            if follow_rules(array, i, j, neighbors) == 1:
                temp_array[i][j] = '#'
            else:
                temp_array[i][j] = ' '
    return temp_array


def follow_rules(array, i, j, neighbors):

    if array[i][j] == '#' and (neighbors == 2 or neighbors == 3):
        value = 1
    elif array[i][j] != '#' and neighbors == 3:
        value = 1
    else:
        value = 0
    return value


if __name__ == "__main__":
    main()