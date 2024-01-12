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
def maze_visualizing(maze, agent, target, path=[], delay=0.1):
    # plt.ion()
    fig, ax = plt.subplots(figsize=(maze.shape[1], maze.shape[0]))
    cmap = plt.cm.colors.ListedColormap(['white', 'black'])
    circle = plt.Circle((agent[1], agent[0]), radius=0.3, color='blue')
    plt.gca().add_patch(circle)

    circle_target = plt.Circle((target[1], target[0]), radius=0.3, color='red')
    plt.gca().add_patch(circle_target)

    for move in path:
        circle_explo = plt.Circle((move[1], move[0]), radius=0.3, color='green')
        plt.gca().add_patch(circle_explo)
        # plt.imshow(maze, cmap=cmap, interpolation='nearest')
        # plt.pause(delay)
        # circle_explo.remove()
    # plt.ioff()
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
    # PLEASE READ README.md BEFORE RUNNING THIS CODE

    # Generating environment
    maze_bot = Environment_Generating(cfg.MAZE_WIDTH, cfg.MAZE_HEIGHT, cfg.AGENT_AREA, cfg.MIN_DISTANCE, cfg.NUM_OF_TARGETS, cfg.MAZE_TYPE, cfg.IS_SAVE)
    maze_bot.main_generating()
    maze = maze_bot.maze
    start = maze_bot.agent_coord
    target = maze_bot.target_list[0]

    # Maze from pickle file
    # maze, start, target = read_pickle_file('Saved_Maze/50x50_simple_maze.pkl')

    # MCTS Solver
    path_result, total_time, memory_info = mcts_solving(maze, start, target)
    print("Path found by MCTS: ", path_result)
    print("MCTS Path length: ", len(path_result))
    print("MCTS Total time: ", total_time)
    print("MCTS Memory usage: ", memory_info)
    path_result.remove(start)
    path_result.remove(target)
    maze_visualizing(maze, start, target, path_result)

    # UCS Solver
    path_result, total_time, memory_info = ucs_solving(maze, start, target)
    print("Path found by UCS: ", path_result)
    print("UCS Path length: ", len(path_result))
    print("UCS Total time: ", total_time)
    print("UCS Memory usage: ", memory_info)
    path_result.remove(start)
    path_result.remove(target)
    maze_visualizing(maze, start, target, path_result)