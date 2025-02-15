import random
import heapq
import numpy as np
import pandas as pd


class Puzzle:
    # Initializes the board
    def __init__(self, board, parent=None, move="", depth=0, cost=0):
        # Stores the tiles in the board as a tuple that can't be changed
        self.board = tuple(board)
        self.parent = parent  # previous state so it can backtrack
        self.move = move  # moves taken to reach this state
        self.depth = depth  # num of moves made (g(n))
        # cost = g(n) + h(n), g(n) is the num of moves made, h(n) is the estimated cost of the goal (heuristic value)
        self.cost = cost
        # Stores the position of the blank space in the puzzle
        self.zero_index = board.index(0)

    # Compares 2 puzzle objects to insert them into a priority queue to ensure lower cost tiles are first
    def __lt__(self, other):
        return self.cost < other.cost

    # Compares the current board with the other board to prevent checking the same board
    def __eq__(self, other):
        return self.board == other.board

    # Gets the new tile arrangements on the board (neighbors) by moving the blank space
    def get_neighbors(self):
        moves = []
        # Gets the row/column position of the current blank space from the current position of blank space to 4
        row, column = divmod(self.zero_index, 4)
        # Dictionary of the directions of the board
        directions = {
            "Up": (-1, 0),
            "Down": (1, 0),
            "Left": (0, -1),
            "Right": (0, 1)
        }

        # Iterates over the directions dictionary
        for move, (r, c) in directions.items():
            new_row, new_column = row + r, column + c

            if 0 <= new_row < 4 and 0 <= new_column < 4:
                # Converts 2D row from the board into a 1D index
                new_index_board = new_row * 4 + new_column
                new_board = list(self.board)
                # Swaps blank tile (zero_index) and new position tiles (new_index_board)
                new_board[self.zero_index], new_board[new_index_board] = new_board[new_index_board], new_board[self.zero_index]
                # Creates a new puzzle state by moving the blank tile and appends it to the list of possible moves
                moves.append(Puzzle(new_board, self, move, self.depth + 1))

        return moves


# h1: Misplaced tiles heuristic
def misplaced_tiles(puzzle, goal):
    count = 0
    for i in range(16):  # Iterates through all the tiles on board
        if puzzle.board[i] != 0 and puzzle.board[i] != goal[i]:
            count += 1
    return count

# h2: Manhattan distance heuristic


def manhattan_distance(puzzle, goal_positions):
    total_distance = 0
    for i in range(len(puzzle.board)):
        tile = puzzle.board[i]  # Tile # at index i
        if tile != 0:  # ignores the blank tile
            # difference between the rows
            row_distance = abs(i // 4 - goal_positions[tile][0])
            # difference between columns
            column_distance = abs(i % 4 - goal_positions[tile][1])
            # Adds the total distance between rows/columns to
            total_distance += row_distance + column_distance

    return total_distance

# h3: Linear conflict heuristic (manhattan distance + conflicts)


def linear_conflict(puzzle, goal_positions):
    manhattan = manhattan_distance(puzzle, goal_positions)
    conflicts = 0

    for row in range(4):
        row_tiles = []  # Tiles in current row
        for column in range(4):
            tile = puzzle.board[row * 4 + column]  # Get tile at the row/column
            if tile in goal_positions:  # Checks if the tile is in the goal state
                row_tiles.append(tile)

        row_tiles_goal = []  # Tiles that should be in this row (their goal)
        for tile in row_tiles:
            if goal_positions[tile][0] == row:  # Checks if the tile is in this row
                row_tiles_goal.append(tile)

        for i in range(len(row_tiles_goal)):
            tile_1st = row_tiles_goal[i]
            for j in range(i + 1, len(row_tiles_goal)):
                tile_2nd = row_tiles_goal[j]
                # Checks if the tile is misplaced
                if goal_positions[tile_1st][1] > goal_positions[tile_2nd][1]:
                    # Conflicts are when 2 tiles are in their correct row/column but out of order in their goal positions
                    conflicts += 2

    for column in range(4):
        column_tiles = []  # Tiles in current column
        for row in range(4):
            tile = puzzle.board[row * 4 + column]
            if tile in goal_positions:
                column_tiles.append(tile)

        # Tiles that should be in this column (their goal)
        column_tiles_goal = []
        for tile in column_tiles:
            # Checks if the tile is in this column
            if goal_positions[tile][1] == column:
                column_tiles_goal.append(tile)

        for i in range(len(column_tiles_goal)):
            tile_1st = column_tiles_goal[i]
            for j in range(i + 1, len(column_tiles_goal)):
                tile_2nd = column_tiles_goal[j]
                if goal_positions[tile_1st][0] > goal_positions[tile_2nd][0]:
                    conflicts += 2

    return manhattan + conflicts


# Implements the A* search algorithm
def a_star_search(start, goal, heuristic):
    goal_positions = {}  # Stores correct positions of each tile in goal state

    for i in range(len(goal)):
        tile = goal[i]
        if tile != 0:
            # Stores the correct row/column positions of each tile
            goal_positions[tile] = (i // 4, i % 4)

    open_set = []  # Priority queue to store only the nodes to be explored
    # Set to store the nodes that are already visited to prevent nodes being explored more than once
    closed_set = set()
    # Pushes the empty tile (0) into the priority queue
    heapq.heappush(open_set, (0, start))
    nodes_expanded = 0

    # Searches all nodes until there are no explored nodes left (open_set is empty)
    while open_set:
        # Gets the node with the lowest cost
        _, current = heapq.heappop(open_set)
        nodes_expanded += 1

        if current.board == goal:  # If current tile matches the goal board, return the current depth and the # of nodes expanded
            return current.depth, nodes_expanded
        # Stores current tile in the closed set so it can mark it as a visited tile
        closed_set.add(current.board)

        # Iterates through all the neighboring tiles
        for neighbor in current.get_neighbors():
            if neighbor.board in closed_set:  # If tile is visited already, it is skipped
                continue
            if heuristic == misplaced_tiles:
                neighbor.cost = neighbor.depth + heuristic(neighbor, goal)
            else:
                neighbor.cost = neighbor.depth + \
                    heuristic(neighbor, goal_positions)
            # Adds new tile to priority queue to be explored
            heapq.heappush(open_set, (neighbor.cost, neighbor))

    return None, None  # Return none if no solution is found in board


# Checks if a 15-puzzle is solvable
def is_solvable(board):
    # Counting the number of inversions
    # Inversions are when a higher-numbered tile on the board appears before the smaller one
    count_inversions = 0

    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            # If the tile number is 0, it is ignored because it's a blank space
            if board[i] and board[j] and board[i] > board[j]:
                count_inversions += 1

    # If the number of inversions is even, the puzzle is solvable
    return count_inversions % 2 == 0

# Generates 1 random solvable 15-puzzle


def generate_solvable_puzzle():
    # Shuffles the tiles until a solvable puzzle is found
    while True:
        tiles = list(range(16))  # 16 tiles from 0 to 15 (the board)
        random.shuffle(tiles)
        # Checks if the shuffled board is solvable, if it is then it gets returned
        if is_solvable(tiles):
            return tiles


# Runs the A* algorithm and prints the data
def run():
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    puzzle = generate_solvable_puzzle()

    results = []
    for heuristic in [misplaced_tiles, manhattan_distance, linear_conflict]:
        step_count, nodes_exp = a_star_search(
            Puzzle(puzzle), goal_state, heuristic)
        results.append({
            "Puzzle Type": "15-puzzle",
            "Heuristic": heuristic.__name__,
            "Steps to Solution": step_count,
            "Nodes Expanded": nodes_exp
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))


run()
