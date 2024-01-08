from queue import PriorityQueue
from maze_generating import Environment_Generating

class UCS:
    def __init__(self, environment, start, goal):
        self.environment = environment
        self.start = start
        self.goal = goal
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.open_set = PriorityQueue()

    # Check if the node is valid 
    def is_valid(self, pos):
        if 1 <= pos[0] < self.environment.shape[0] and 1 <= pos [1] < self.environment.shape[1]:
            return self.environment[pos[0]][pos[1]] == 0

    # Get the next cells surround and their costs
    def get_next_cells(self, current, visited):
        next_actions = []
        action_costs = []

        for direct in self.directions:
   
            cost = 1
            new_pos = (current[0] + direct[0], current[1] + direct[1])

            # If it was in visited, then skip
            if new_pos in visited:  
                continue

            # Check if new pos valid
            elif self.is_valid(new_pos):
                next_actions.append(new_pos)
                action_costs.append(cost)
            else:
                continue
        return zip(next_actions, action_costs)

    def uniform_cost_search(self):
        # Put the start to the queue
        self.open_set.put((0, self.start, []))
        visited = []
        paths_explored = []

        while not self.open_set.empty():
            # Get the cell with the lowest cost
            cost, current, path = self.open_set.get()

            # Check if terminal
            if current == self.goal:
                paths_explored.append(path + [current])  
                return path + [current], visited
        
            if current in visited:
                continue

            # Add the cell to visited list
            visited.append(current)
            paths_explored.append(path + [current])
            
            # Get the next actions and put them to the queue
            for next_node, action_cost in self.get_next_cells(current, visited):
                new_cost = cost + action_cost  
                self.open_set.put((new_cost, next_node, path + [current]))

        return None, None
    
if __name__ == "__main__":
    maze_bot = Environment_Generating(35, 35, ((0, 0), (3,3)), 31, 1)
    maze_bot.main_generating()

    ucs = UCS(maze_bot.maze, maze_bot.agent_coord, maze_bot.target_list[0] )
    path, visited = ucs.uniform_cost_search()

    print(path)
    
    maze_bot.maze_visualizing(maze_bot.agent_coord, maze_bot.target_list)