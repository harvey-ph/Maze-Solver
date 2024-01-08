from queue import PriorityQueue
from maze_generating import Environment_Generating

class UCS:
    def __init__(self, environment, start, goal):
        self.environment = environment
        self.start = start
        self.goal = goal
        self.directions_cost = {(-1, 0): 1, (1, 0): 1, (0, -1): 1, (0, 1): 1}
        self.open_set = PriorityQueue()
    def is_valid(self, x, y):
        if 0 <= x < self.environment.shape[0] and 0 <= y < self.environment.shape[1]:
            return self.environment[x][y] == 0

    def get_next_actions(self, current, visited, action_step):
        next_actions = []
        action_costs = []
        for dx, dy in self.directions_cost:
            last = None
            cost = self.directions_cost[(dx, dy)] 
            for i in range(1, action_step + 1):
                new_x, new_y = current[0] + i * dx, current[1] + i * dy
                if (new_x, new_y) in visited:  # If it was in visited, then skip
                    continue
                elif (new_x, new_y) == self.goal:
                    visited.append(last)
                    last = new_x, new_y
                    break
                elif self.is_valid(new_x, new_y):
                    visited.append(last)
                    last = (new_x, new_y)
                else:
                    break

            if last:
                next_actions.append(last)
                action_costs.append(cost)

        return zip(next_actions, action_costs)

    def uniform_cost_search(self, action_step=1):
        self.open_set.put((0, self.start, []))
        visited = []
        paths_explored = []

        while not self.open_set.empty():
            cost, current, path = self.open_set.get()

            if current == self.goal:
                paths_explored.append(path + [current])  
                return path + [current], visited

            if current in visited:
                continue
        
            visited.append(current)
            paths_explored.append(path + [current])
            
                # current, goal, environment, visited, action_step
            for next_node, action_cost in self.get_next_actions(current, visited, action_step):
                new_cost = cost + action_cost  
                self.open_set.put((new_cost, next_node, path + [current]))

        return None, None
    
if __name__ == "__main__":
    maze_bot = Environment_Generating(35, 35, ((0, 0), (3,3)), 31, 1)
    maze_bot.main_generating()
    start = maze_bot.agent_coord
    goal = maze_bot.target_list[0] 
    ucs = UCS(maze_bot.maze, start, goal)
    path, visited = ucs.uniform_cost_search()
    print(path)
    maze_bot.maze_visualizing(maze_bot.agent_coord, maze_bot.target_list)