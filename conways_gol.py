from random import randint


def main():

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

    while (True):
        for k in range(height):
            print(array[k])
        quit = input('Press enter to advance to the next generation, type "quit" to quit\n')
        if quit == 'quit':
            break
        array = next_generation(array, width, height)
        if is_dead(array, width, height) == True:
            print('all cells dead, game over')
            return

    return


def build_array(array, width, height):

    random = input('Enter "r" for a random array, otherwise press enter to continue\n')
    if random != 'r':
        for i in range(height):
            for j in range(width):
                while (True):
                    value = input('Please enter either 0 or 1\n')
                    if value == '0' or value == '1':
                        break
                array[i][j] = int(value)
                for k in range(height):
                    print(array[k])
    else:
        for i in range(height):
            for j in range(width):
                array[i][j] = randint(0, 1)
        for k in range(height):
            print(array[k])
    print('\n')
    return

def check_neighbors(array, i, j, width, height):

    neighbors = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if k == 0 and l == 0:
                continue
            elif i + k >= 0 and i + k < height and j + l >= 0 and j + l < width:
                if array[i + k][j + l] == 1:
                    neighbors += 1
    return neighbors


def is_dead(array, width, height):

    dead = True
    for i in range(height):
        for j in range(width):
            if array[i][j] == 1:
                dead = False
    return dead

def next_generation(array, width, height):

    temp_array = [[0 for x in range(width)] for y in range(height)]
    for i in range(height):
        for j in range(width):
            neighbors = check_neighbors(array, i, j, width, height)
            temp_array[i][j] = follow_rules(array, i, j, neighbors)
    return temp_array


def follow_rules(array, i, j, neighbors):

    if array[i][j] == 1 and (neighbors == 2 or neighbors == 3):
        value = 1
    elif array[i][j] == 0 and neighbors == 3:
        value = 1
    else:
        value = 0
    return value


if __name__ == "__main__":
    main()