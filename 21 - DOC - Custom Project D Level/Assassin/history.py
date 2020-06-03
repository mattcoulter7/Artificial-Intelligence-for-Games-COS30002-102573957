class History(object):
    """description of class"""
    def __init__(self,guard,world):
        self.guard = guard
        self.world = world
        self.yet_to_visit = world.graph.all_available_nodes

    def update(self):
        # Check if everywhere has been visited
        if self.empty():
            self.reset()

    def reset(self):
        ''' resets history once yet_to_visit is empty '''
        self.yet_to_visit = world.graph.all_available_nodes

    def remove(self,pt):
        ''' remove a given point from yet_to_visit when it has been visited '''
        if pt in self.yet_to_visit:
            self.yet_to_visit.remove(pt)

    def empty(self):
        return len(self.yet_to_visit) == 0


