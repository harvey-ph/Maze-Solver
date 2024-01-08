# Generating Maze (Main environment for agent and targets) using Prim Algorithm
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import datetime
import pickle
import os

class Environment_Generating():
    def __init__(self, width, height, area, min_distance, num_of_target=1, type='simple', is_save = False):
        self.width = width
        self.height = height
        self.area = area
        self.num_of_target = num_of_target
        self.min_distance = min_distance
        self.type = type
        self.is_save = is_save
   
        # List of valid nodes for generating agent and targets
        self.agent_valid_nodes = []
        self.target_valid_nodes = []
        self.target_list = []

        
    # Main function generating all maze, agent, targets
    def main_generating(self):
        self.maze_generating()
        self.agent_generating()
        self.target_generating()

        if self.is_save:
            self.save_maze()
    # Generating maze using Prim's Algorithm
    def maze_generating(self):

        self.maze = np.ones((self.width, self.height))

        self.start = (random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        self.maze[self.start[0]][self.start[1]] = 0

        # Initialize frontiers list and space list nodes
        self.frontiers = [(self.start[0], self.start[1] - 2), (self.start[0], self.start[1] + 2),
                          (self.start[0] - 2, self.start[1]), (self.start[0] + 2, self.start[1])]
        
        # Add the starting node to the list of space nodes
        self.space_nodes = [self.start]

        while self.frontiers:
            self.f_node = random.choice(self.frontiers)
            self.frontiers.remove(self.f_node)

            if 1 <= self.f_node[0] <= (self.width - 2) and 1 <= self.f_node[1] <= (self.height - 2) and self.maze[self.f_node[0]][self.f_node[1]] == 1:
                self.f_node_frontiers = [(self.f_node[0], self.f_node[1] - 2), (self.f_node[0], self.f_node[1] + 2), (self.f_node[0] - 2, self.f_node[1]), (self.f_node[0] + 2, self.f_node[1])]
                random.shuffle(self.f_node_frontiers)

                # Check if there is any frontier valid and can connect to created space nodes
                space_add_count = 0
                for f_n_f in self.f_node_frontiers:
                    if 1 <= f_n_f[0] <= (self.width - 2) and 1 <= f_n_f[1] <= (self.height - 2) and self.maze[f_n_f[0]][f_n_f[1]] == 0:
                        self.maze[self.f_node[0]][self.f_node[1]] = 0
                        # Connect the frontier with created space nodes
                        self.maze[int((self.f_node[0]+f_n_f[0])/2)][int((self.f_node[1]+f_n_f[1])/2)] = 0
                        # Add new space nodes to list of space nodes
                        self.space_nodes.extend([self.f_node,(int((self.f_node[0]+f_n_f[0])/2), int((self.f_node[1]+f_n_f[1])/2))])
                        if self.type == 'simple':
                            space_add_count+=1
                            if random.random() > 0.3 or space_add_count == 2:
                                break
                        else:
                            # type: complex
                            break

                # Add all the current node's frontiers to the main frontiers list:
                self.frontiers += self.f_node_frontiers

    # Generate agent in selected area
    def agent_generating(self):
        # Get a list of valid nodes for generating agent inside selected space area
        for a_cell in self.space_nodes:
            if (self.area[0][0] <= a_cell[0] <= self.area[1][0] and self.area[0][1] <= a_cell[1] <= self.area[1][1]) or (
                    self.area[0][0] >= a_cell[0] >= self.area[1][0] and self.area[0][1] >= a_cell[1] >= self.agent_init_area[1][1]):
                self.agent_valid_nodes.append(a_cell)
        self.agent_coord = random.choice(self.agent_valid_nodes)

    # Calculate the distance between two node
    def euclidean_distance(self, node_a, node_b):
        return math.dist(node_a, node_b)

    # Generate target in selected area away from agent at least min_distance
    def target_generating(self):
        # Get a list of valid nodes for generating targets, meaning the node that is inside the space area
        self.target_valid_nodes = self.space_nodes.copy()
        self.target_valid_nodes.remove(self.agent_coord)
        random.shuffle(self.target_valid_nodes)
        for node in self.target_valid_nodes:
            if self.euclidean_distance(self.agent_coord, node) >= self.min_distance:
                self.target_list.append(node)
                # self.maze[node[0]][node[1]] = 3
            if len(self.target_list) == self.num_of_target:
                break
        if len(self.target_list) == 0:
            print("Cannot generate any targets with that minimum distance, 1 target will be randomly generated")
            self.target_list.append(random.choices(self.target_valid_nodes))

    # Static visualizing, only maze, agent and targets
    def maze_visualizing(self):
        fig, ax = plt.subplots(figsize=(self.maze.shape[1], self.maze.shape[0]))
        cmap = plt.cm.colors.ListedColormap(['white', 'black'])
        circle = plt.Circle((self.agent_coord[1], self.agent_coord[0]), radius=0.3, color='blue')
        plt.gca().add_patch(circle)
        for target in self.target_list:
            circle_target = plt.Circle((target[1], target[0]), radius=0.3, color='red')
            plt.gca().add_patch(circle_target)
        # ax.set_xticks(np.arange(-.5, len(self.maze[0]), 1), minor=True)
        # ax.set_yticks(np.arange(-.5, len(self.maze), 1), minor=True)
        ax.grid(which='minor', color='grey', linewidth=2)
        ax.imshow(self.maze, cmap=cmap, interpolation='nearest')
        plt.show()

    # Visualizing with animation of the path found:
    def visualizing_animation(self, path, delay=0.001):
        plt.ion()
        fig, ax = plt.subplots(figsize=(self.maze.shape[1], self.maze.shape[0]))
        cmap = plt.cm.colors.ListedColormap(['white', 'black'])
        circle = plt.Circle((self.agent_coord[1], self.agent_coord[0]), radius=0.3, color='blue')
        plt.gca().add_patch(circle)
        circle_target = plt.Circle((self.target_list[0][1], self.target_list[0][0]), radius=0.3, color='red')
        plt.gca().add_patch(circle_target)
        
        for move in path:
            circle_explo = plt.Circle((move[1], move[0]), radius=0.3, color='green')
            plt.gca().add_patch(circle_explo)
            plt.imshow(self.maze, cmap=cmap, interpolation='nearest')
            plt.pause(delay)
            # circle_explo.remove()
        plt.ioff()
        ax.set_xticks(np.arange(-.5, len(self.maze[0]), 1), minor=True)
        ax.set_yticks(np.arange(-.5, len(self.maze), 1), minor=True)
        ax.grid(which='minor', color='grey', linewidth=2)
        ax.imshow(self.maze, cmap=cmap, interpolation='nearest')
        plt.show()

    # Save the maze to pickle file
    def save_maze(self):
        saving_data = {
            'maze': self.maze,
            'agent_coord': self.agent_coord,
            'target_list': self.target_list
        }
        if not os.path.exists('Saved_Maze'):
            os.makedirs('Saved_Maze')

        file_name = 'Saved_Maze/maze_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.pkl'
        with open(file_name, 'wb') as f:
            pickle.dump(saving_data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':

    maze_bot = Environment_Generating(35, 35, ((0, 0), (2,2)), 40, 1, 'complex')
    maze_bot.main_generating()
    maze_bot.maze_visualizing()
    # maze_bot.save_maze()
