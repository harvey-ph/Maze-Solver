from maze_generating import Environment_Generating
from mcts import MCTS_Solver
from ucs import UCS
import config as cfg
import time
import tracemalloc
import pickle
import matplotlib.pyplot as plt

# Get maze, start and target from pickle file
def read_pickle_file(file_name):
    with open(file_name, 'rb') as f:
        env_data = pickle.load(f)
    maze = env_data['maze']
    agent_coord = env_data['agent_coord']
    target_coord = env_data['target_list'][0]
    return maze, agent_coord, target_coord

# Visualize maze from file
def maze_visualizing(maze, agent, target_list):
    fig, ax = plt.subplots(figsize=(maze.shape[1], maze.shape[0]))
    cmap = plt.cm.colors.ListedColormap(['white', 'black'])
    circle = plt.Circle((agent[1], agent[0]), radius=0.3, color='blue')
    plt.gca().add_patch(circle)
    for target in target_list:
        circle_target = plt.Circle((target[1], target[0]), radius=0.3, color='red')
        plt.gca().add_patch(circle_target)
    # ax.set_xticks(np.arange(-.5, len(self.maze[0]), 1), minor=True)
    # ax.set_yticks(np.arange(-.5, len(self.maze), 1), minor=True)
    ax.grid(which='minor', color='grey', linewidth=2)
    ax.imshow(maze, cmap=cmap, interpolation='nearest')
    plt.show()

# MCTS Solver
def mcts_solving(maze, start, target):
    # Tracking memory usage and time consuming
    start_time = time.time()
    tracemalloc.start()

    solver = MCTS_Solver(maze, start, target)
    solver.run()
    
    memory_info = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time = time.time() - start_time
    path_result = solver.path_result

    return path_result, total_time, memory_info

# UCS Solver
def ucs_solving(maze, start, target):
    # Tracking memory usage and time consuming
    start_time = time.time()
    tracemalloc.start()

    solver = UCS(maze, start, target)
    path_result, _ = solver.uniform_cost_search()
    
    memory_info = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time = time.time() - start_time
    return path_result, total_time, memory_info
    

if __name__ == '__main__':
    
    # Generating environment
    # maze = Environment_Generating(cfg.MAZE_WIDTH, cfg.MAZE_HEIGHT, cfg.AGENT_AREA, cfg.MIN_DISTANCE, cfg.NUM_OF_TARGETS, cfg.MAZE_TYPE, cfg.IS_SAVE)
    # maze.main_generating()
    # maze.maze_visualizing()

    # Maze from pickle file
    maze, start, target = read_pickle_file('Saved_Maze/complex_maze.pkl')
    maze_visualizing(maze, start, [target])

    # MCTS Solver
    path_result, total_time, memory_info = mcts_solving(maze, start, target)

    # UCS Solver
    # path_result, total_time, memory_info = ucs_solving(maze, start, target)
    print("Path found: ", path_result)
    print("Path length: ", len(path_result))
    print("Total time: ", total_time)
    print("Memory usage: ", memory_info)