from random import randint
import sys
import csv


def main():

    # No starting conditions, just run and ask for input
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

    # If user includes CSV test pattern
    elif len(sys.argv) == 2:
        array = list(csv.reader(open(sys.argv[1])))
        width = len(array[0])
        height = len(array)

    # Runs with argv[1] x argv[2] grid
    elif len(sys.argv) == 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        array = [[0 for x in range(width)] for y in range(height)]
        build_array(array, width, height)

    # Runs with argv[1] x argv[2] grid, in random starting configuration
    elif len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        array = [[0 for x in range(width)] for y in range(height)]
        build_array(array, width, height, sys.argv[3])

    # Invalid start attempt
    else:
        print('Usage: python FILENAME.py (PRESET.csv) OR (WIDTH HEIGHT r)')

    # Where the game begins. "proceed" doesn't even actually need to get used,
    #       it's an on-screen text prompt letting user know to continue.
    proceed = input('Press or hold enter to advance generations, enter any value to quit\n')
    while (True):
        for k in range(height):
            print(*array[k])
        # Anything besides enter will break and return the program
        run = input('')
        if run != '':
            break
        array = next_generation(array, width, height)
        if is_dead(array, width, height) == True:
            print('all cells dead, game over')
            return

    return


def build_array(array, width, height, random=''):

    if random != 'r':
        random = input('Enter "r" for a random array, otherwise press enter to continue\n')

    # Allows user to input for each cell in the grid, either nothing, or hash
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

    # Generates random starting conditions
    else:
        for i in range(height):
            for j in range(width):
                if randint(0, 1) == 1:
                    array[i][j] = '#'
                else:
                    array[i][j] = ' '
    return


def check_neighbors(array, i, j, width, height):

    # Iterates through surrounding pixels of each cell to check how many are alive
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

    # Goes through entire array to see if there are live cells still
    dead = True
    for i in range(height):
        for j in range(width):
            if array[i][j] == '#':
                dead = False
    return dead


def next_generation(array, width, height):

    # Dynamically allocated array used as a buffer while determining conditions of next generation
    temp_array = [[0 for x in range(width)] for y in range(height)]
    for i in range(height):
        for j in range(width):

            # Sends the full array as well as each pixel and the dimensions
            neighbors = check_neighbors(array, i, j, width, height)

            # Assigns values to next generation buffer array
            if follow_rules(array, i, j, neighbors) == 1:
                temp_array[i][j] = '#'
            else:
                temp_array[i][j] = ' '
    return temp_array


def follow_rules(array, i, j, neighbors):

    # If a live cell has 2 or 3 neighbors, it lives
    if array[i][j] == '#' and (neighbors == 2 or neighbors == 3):
        value = 1

    # If a dead cell has exactly 3 neighbors, it comes back to life
    elif array[i][j] != '#' and neighbors == 3:
        value = 1

    # Otherwise, live cells die and dead cells stay dead
    else:
        value = 0
    return value


if __name__ == "__main__":
    main()
