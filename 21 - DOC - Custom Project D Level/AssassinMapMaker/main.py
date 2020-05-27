from random import randrange

global grid

def write_file(name):
    global grid
    # Open file for reading
    f = open("../Assassin/maps/{}.csv".format(name), "a")
    
    # Write name and grid dimensions
    f.write('{}\n{}\n{}\n'.format(name,len(grid[0]),len(grid)))

    # Write type of each point
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            z = grid[x][y]
            f.write('{},{},{}\n'.format(x,y,z))
    f.close()

def generate_map():
    global grid
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if x in [0,int(width) - 1] or y in [0,int(height) - 1]:
                grid[x][y] = 1
            else:
                has_path = False
                for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    new_x = x + i[0]
                    new_y = y + i[1]
                    if grid[new_x][new_y] != 0 and not has_path:
                        has_path = True
                if has_path:
                    grid[x][y] = 0
                else:
                    grid[x][y] = randrange(1,3)

def randomise():
    global grid
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            options = [0,0,0,0,0,0,0,0,0,0,1,2,3]
            grid[x][y] = options[randrange(0,len(options))]

def initialise_grid(height,width):
    global grid
    grid = [ [0]*width for _ in range(height) ]

if __name__ == '__main__':
    name = input('Enter Map Name : ')
    height = int(input('Enter Height : '))
    width = int(input('Enter Width : '))
    
    initialise_grid(height,width)
    randomise()
    #generate_map()

    write_file(name)
