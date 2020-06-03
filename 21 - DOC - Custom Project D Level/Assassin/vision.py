from vector2d import Vector2D
from graphics import egi

class Vision(object):
    """description of class"""
    def __init__(self,parent,range,world):
        self.parent = parent
        self.vision_range = range
        self.world = world
        self.vision = []

    def update(self):
        # Adjacent edges of node
        adjacent = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        # Nodes that the guard will be able to see
        visible_nodes = []
        # Distance to middle point of vision square that will be made
        ahead_range = int((self.vision_range - 1) / 2)
        # Node of self
        self_node = self.world.graph.pos_to_node(self.parent.pos.copy())
        # Middle point of vision square that will be made
        ahead_node = self.world.graph.pos_to_node(self.parent.pos + self.parent.heading * self.world.graph.grid_size * (ahead_range + 1))
        # Add that centre point to begin with
        visible_nodes.append(ahead_node)
        # Expand from centre outwards adding nodes to cover full square
        check_from = 0 # Used to avoid retesting adjacent nodes that we have already checked for
        for i in range(ahead_range):
            for j in range(check_from,len(visible_nodes)):
                for pt2 in adjacent:
                    pt1 = visible_nodes[j]
                    new_node = Vector2D(pt1.x + pt2[0],pt1.y + pt2[1])
                    if self.world.graph.node_available(new_node) and new_node not in visible_nodes:
                        visible_nodes.append(new_node)
                        check_from += 1
        for i in range(len(visible_nodes)):
            visible_nodes[i] = self.world.graph.global_to_relative(visible_nodes[i])
            self.parent.history.remove(visible_nodes[i]) # Remove point from yet_to_visit list

        self.vision = visible_nodes

    def render(self):
        # Visibility
        for pt in self.vision:
            egi.red_pen()
            egi.circle(self.world.graph.node_to_pos(pt.copy(),'center'),self.world.graph.grid_size/2)