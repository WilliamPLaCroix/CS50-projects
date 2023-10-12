# Conway's Game of Life in Python terminal

#### Description:

I had been toying with the idea of trying to make a text based game in python terminal, and was trying to decide how to handle things like static UI elements, maps, etc. when I watched The Art of Code (https://youtu.be/6avJHaC3C2U), and thought that making a terminal-based version of Conway's Game of Life would be the perfect challenge.

CGoL has fairly straightforward parameters, following only four rules (detailed below), and there aren't terribly many moving parts, so I felt it would be a manageable challenge for me to undertake. I had to decide how I would implement the display, which started out as a 2D array of 0s and 1s, and eventually transitioned into a much cleaner and easier to follow comma-stripped array using spaces and hashes instead. With the same idea of do-while loops that we developed early on in the course, I realised I could render each generation successively simply by pressing or holding 'enter', which gives the illusion of moving pixel graphics.

main() primarily handles various options of user input in setting up the initial starting conditions, allowing for: manual input in a 2D array from 3x3 to 50x50; randomly generated starting conditions in the same grid; or CSV imported patterns of any size as starting conditions. I chose 50x50 because that's about the largest size I could display in my VS terminal without the text wrapping, which completely kills the cohesive picture. Theoretically though, this is only limited by your screen realestate, so one could introduce an enormous CSV, given enough display space.

build_array() gets called with the user's starting conditions and constructs the initial grid, filled with spaces and hashes.

check_neighbors() takes the ideas from week 4 Filter and iterates over a given pixel's neighbors in order to check the conditions in follow_rules() for building the next generation

is_dead() simply checks the grid to see if there are any living cells, since without live cells, the game is essentially over and this gives an exit condition.

next_generation() is the meatiest function, calling check_neighbors() on each pixel and using the return in a call to follow_rules(), filling a temporary array in order to return a new array as the next generation/iteration without modifying the original array and checking the modified array for neighbors.

follow_rules() takes the 4 base rules of Conway's Game of Life:

    Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overpopulation.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Condensed into 3 conditions:

    Any live cell with two or three live neighbours survives.
    Any dead cell with three live neighbours becomes a live cell.
    All other live cells die in the next generation. Similarly, all other dead cells stay dead.

And returns 0 or 1 for each cell in order to fill the next generation.

The only file necessary here is the .py, any CSV files are just for fun/testing. It should be as simple as filling and exporting a Google Sheet if you want to test your own patterns, so here's a link to the Wiki page containing several patterns, concepts, and any other info on the "game" that you might need to get started: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

I'm William LaCroix, and this is CS50.
