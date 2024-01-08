# This is the code for desiginng the solving maze using Monte Carlo Tree Search Algorithm
import random
from maze_generating import Environment_Generating
import numpy as np
import math
import config as cfg

# Class for node of MCTS
class MCTS_Node:
    def __init__(self, position, parents=None, path=None):
        self.position = position
        self.parents = parents
        self.children = []
        self.visit_count = 0
        self.outcome_value = 0
        self.path = path if path is not None else []

# Class MCTS Solver
class MCTS_Solver:
    def __init__(self, maze, agent_start, target, max_iterations=cfg.MAX_ITERATIONS, exploration_constant=cfg.EXPLORATION_CONSTANT):
        self.environment = maze
        self.start = agent_start
        self.target = target
        self.max_iterations = max_iterations
        self.exploration_constant = exploration_constant
        self.path_result = None
        self.list_of_nodes_position = [self.start]

    # Get the valid move for simulation and expansion: left, right, forward
    def get_valid_move(self, current_position, last_postion=None):
        valid_move = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moveable_node = [(current_position[0]+direct[0], current_position[1]+direct[1]) for direct in directions]
        for m_node in moveable_node:
            if 1 <= m_node[0] <= (self.environment.shape[0] - 2) and 1 <= m_node[1] <= (self.environment.shape[1] - 2) and self.environment[m_node[0]][m_node[1]] == 0 and m_node != last_postion:
                valid_move.append(m_node)
        return valid_move

    # Check if the node is terminal
    def is_terminal(self, position):
        return position == self.target

    # Selection phase
    def select(self, node):
        if node.children:
            unvisited_node = [child for child in node.children if child.visit_count == 0]
            if unvisited_node:
                return random.choice(unvisited_node)
            else:
                selected_node = max(node.children, key=lambda c: c.outcome_value/c.visit_count + self.exploration_constant * math.sqrt(math.log(node.visit_count)/c.visit_count))
                return selected_node
        return None

    # def calculate_distance(self, coord_1, coord_2, mod):
    #     if mod == 'manhattan':
    #         return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])
    #     elif mod == 'cosine':
    #         return 1 - np.dot(coord_1, coord_2)/(np.linalg.norm(coord_1)*np.linalg.norm(coord_2))
    #     else:
    #         # Euclidean distance
    #         return math.dist(coord_1, coord_2)

    # def heuristic_move(self, posible_move):
    #     return min(posible_move, key=lambda move: self.calculate_distance(move, self.target, 'euclidean'))

    # Simulation phase
    def simulate(self, node):
        simulation_iteration = 0
        last_position = None
        current_position = node.position
        while simulation_iteration < cfg.MAX_SIMULATION_ITERATIONS:
            if current_position == self.target:
                return cfg.MAX_SIMULATION_POINT - (cfg.REDUCTION_FACTOR * simulation_iteration)
            simulation_iteration += 1
            possible_move = self.get_valid_move(current_position, last_position)
            if len(possible_move) > 0:
                last_position = current_position
                current_position = random.choice(possible_move)
                # current_position = self.heuristic_move(possible_move)
            else: 
                return 0
        return 0

    # Expansion phase
    def expand(self, node):
        possible_move = self.get_valid_move(node.position)
        for move in possible_move:
            if move not in self.list_of_nodes_position:
                new_path = node.path.copy()
                new_path.append(move)
                node.children.append(MCTS_Node(move, parents=node, path=new_path))
                self.list_of_nodes_position.append(move)

    # Backpropagation phase
    def backpropagate(self, node, outcome):
        while node:
            node.visit_count += 1
            node.outcome_value += outcome
            node = node.parents

    # Main function
    def run(self):
        # Generating children of root node:
        root = MCTS_Node(self.start, path=[self.start])
        self.expand(root)
       
        for _ in range(self.max_iterations):

            # Selection
            current_node = root
            while current_node.children:
                current_node = self.select(current_node)
        
            # Check terminal
            if self.is_terminal(current_node.position):
                self.path_result = current_node.path
                break

            # Expansion
            self.expand(current_node)
       
            # Simulation
            outcome = -100
            if current_node.children:
                outcome = self.simulate(current_node)
            
            # Backpropagation
            self.backpropagate(current_node, outcome)


if __name__ == "__main__":
    maze = Environment_Generating(205, 205, ((0, 0), (3,3)), 220, 1)
    maze.main_generating()
    solver = MCTS_Solver(maze.maze, maze.agent_coord, maze.target_list[0])
    result = solver.run()
    print(solver.path_result)