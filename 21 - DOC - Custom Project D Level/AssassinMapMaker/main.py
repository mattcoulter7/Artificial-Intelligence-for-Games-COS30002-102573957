from random import randrange

global grid

def write_file(name,guards,assassin):
    global grid
    # Open file for reading
    f = open("../Assassin/maps/{}.csv".format(name), "a")
    
    # Write name and grid dimensions
    f.write('{}\n{}\n{}\n'.format(name,len(grid[0]),len(grid)))

    # Write type of each point
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            type = None
            z = grid[x][y]
            if z == 0:
                type = 'tile'
            else:
                type = 'block'
            f.write('{},{},{},{}\n'.format(type,x,y,z))
    f.write('map_done,\n')
    # Guards
    f.write('{},{}\n'.format('num_guards',len(guards)))
    for i in range(len(guards)):
        f.write('{},{},{}\n'.format('guard',guards[i][0],guards[i][1]))
    # Assassin
    f.write('{},{},{}\n'.format('assassin',assassin[0],assassin[1]))
    f.close()

def randomise():
    global grid
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            options = [0,0,0,0,0,0,0,0,0,0,1,2,3]
            grid[x][y] = options[randrange(0,len(options))]

def set_perimeter():
    global grid
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if x in [0,len(grid) - 1] or y in [0,len(grid[x]) - 1]:
                grid[x][y] = 2

def fix_grid():
    global grid
    diagonals = [(1,1),(-1,-1),(1,-1),(-1,1)]
    for x in range(1,len(grid)-1):
        for y in range(len(grid[x])-1):
            for pt in diagonals:
                new_pt = (x+pt[0],y+pt[1])
                for type in [1,2,3]:
                    if grid[x][y] == type and grid[new_pt[0]][new_pt[1]] == type:
                        grid[x+pt[0]][y] = type
                        grid[x][y+pt[1]] = type

def initialise_grid(height,width):
    global grid
    grid = [ [0]*width for _ in range(height) ]

def generate_loc():
    x = randrange(0,len(grid))
    y = randrange(0,len(grid[0]))
    if grid[x][y] != 0:
        return generate_loc()
    return (x,y)

if __name__ == '__main__':
    for i in range(100):
        # Meta
        name = 'map{}'.format(i)
        height = randrange(10,40)
        width = randrange(10,40)
        num_guards = round(((width+height)/2)/5)

        # Create grid
        initialise_grid(height,width)

        # Generate map data
        randomise()
        fix_grid()
        set_perimeter()

        # Players
        guards = []
        for i in range(num_guards):
            guards.append(generate_loc())
        assassin = generate_loc()

        # Write to file
        write_file(name,guards,assassin)
