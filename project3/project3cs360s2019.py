from datetime import datetime

"""
gamma = 0.9
eplison = 0.1

.7
"""
class mdp:
    def __init__(self, grid_size, num_obstacles, obstacles, goal):


def value_iteration(mdp, error):

"""
Input: The input file will be formatted as follows (all arguments are 32-bit integers):
<grid_size> // strictly positive
<num_obstacles> // non-negative
Next num_obstacles lines: <x>, <y> // strictly positive, denoting locations of obstacles
<x>,<y> // destination point

Output:
- Obstacles are represented by the letter ‘o’
- EAST is represented by the right-caret character ‘>’
- WEST is represented by the left-caret character ‘<’
- NORTH is represented by the hat symbol ‘^’
- SOUTH is represented by the letter ‘v’
- The destination is represented by a period symbol ‘.’

Utility(state) = Reward(state) + gamma*(max(sum of probability of actions * utility of actions)
"""


def read_input(file):
    start_time = datetime.now()
    f = open(file, "r")

    grid_size = int(f.readline().strip())
    num_obstacles = int(f.readline().strip())
    obstacles = [f.readline().strip() for x in range(num_obstacles)]
    goal = f.readline().strip()

    print(grid_size, num_obstacles)
    print(obstacles)
    print(goal)

    value_iteration(mdp, error)

    print(datetime.now() - start_time)


read_input("dev_cases/input-0.txt")