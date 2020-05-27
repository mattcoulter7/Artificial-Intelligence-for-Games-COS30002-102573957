from vector2d import Vector2D
from node import Node
from math import *

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = Vector2D(current_node.position.x + new_position[0], current_node.position.y + new_position[1])

            # Make sure within range
            if node_position.x > (len(maze) - 1) or node_position.x < 0 or node_position.y > (len(maze[len(maze)-1]) -1) or node_position.y < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position.x][node_position.y] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position.x - end_node.position.x) ** 2) + ((child.position.y - end_node.position.y) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

# Smooth code referenced from https://github.com/htx1219/Python/blob/master/373/path%20smoothing.py, https://www.youtube.com/watch?v=v0-OUApP_5Q
def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.00001):

    newpath = []
    # Make a deep copy of path into newpath
    for i in range(len(path)):
        newpath.append(Vector2D(path[i].x,path[i].y))

    #### ENTER CODE BELOW THIS LINE ###
    change = 1
    while change > tolerance:
        change = 0
        #First and last points stay the same
        for i in range(1,len(path)-1):
            # Updates x value
            ori = newpath[i].x
            newpath[i].x = newpath[i].x + weight_data*(path[i].x-newpath[i].x)
            newpath[i].x = newpath[i].x + weight_smooth*(newpath[i+1].x+newpath[i-1].x-2*newpath[i].x)
            change += abs(ori - newpath[i].x)
            # Updates y value
            ori = newpath[i].y
            newpath[i].y = newpath[i].y + weight_data*(path[i].y-newpath[i].y)
            newpath[i].y = newpath[i].y + weight_smooth*(newpath[i+1].y+newpath[i-1].y-2*newpath[i].y)
            change += abs(ori - newpath[i].y)
    
    return newpath # Leave this line for the grader!



