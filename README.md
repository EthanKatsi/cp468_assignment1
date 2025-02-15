# CP468 Assignment #1

## Task I:

### Instructions:

This code implements the A\* algorithm for the 8-puzzle, with heuristics:

**h1:** Misplaced Tiles

**h2:** Manhattan Distance

**h3:** Linear Conflict

The code generates 100 randomly reachable states of the 8-puzzle, solves them with h1 and h2 and records in a table the number of steps to find the solution and the number of nodes expanded by A\* in each case.

Sample output:

```plaintext
Puzzle Type          Heuristic  Average Steps to Solution  Average Nodes Expanded
   8-puzzle    misplaced_tiles                      22.13                16395.81
   8-puzzle manhattan_distance                      22.13                 1188.36
   8-puzzle    linear_conflict                      22.13                  644.90
```

### How to run the code:

#### 1. Install the numpy library:

```plaintext
pip install numpy
```

#### 2. Install the pandas library:

```plaintext
pip install pandas
```

#### 3. Download **t01.py** in the **"group20_a1"** folder

#### 4. Open **t01.py** in a code editor (Ex. VS Code, Eclipse, etc)

#### 5. Run the code in the code editor and it should print the table in the terminal

## Task II:

### Instructions:

This code implements the A\* algorithm for the 15-puzzle, with heuristics:

**h1:** Misplaced Tiles  
**h2:** Manhattan Distance  
**h3:** Linear Conflict

The code generates a random but solvable state of the 15-puzzle, solves it using the A* algorithm with each heuristic, and records the number of steps to find the solution and the number of nodes expanded by A* in each case.

Sample output:

```plaintext
Initial Puzzle:
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15  0]]

       Heuristic  Steps to Solution  Nodes Expanded
 misplaced_tiles                52            123456
 manhattan_distance            52             98765
    linear_conflict            52             54321
```

### How to run the code:

#### 1. Install the numpy library:

```plaintext
pip install numpy
```

#### 2. Install the pandas library:

```plaintext
pip install pandas
```

Download t02.py in the "group20_a1" folder
Open t02.py in a code editor.
Run the code in the code editor and it should print the results in the terminal.
