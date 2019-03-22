"""
Gavin Bains
USCID: 6826294332
CSCI 360

Project 1
"""
import queue

frontier = queue.PriorityQueue()
explored = set()
board = []
maxTigerCount = 0
tigerCoords = []
tigerCoordsMap = {}
heuristicMap = {}
c = 0
a = 0
n = 0


def check_correctness(row, col):
	for i in range(row):
		existing_camera_loc = board[i]
		if existing_camera_loc == col or existing_camera_loc == col - (row - i) or existing_camera_loc == col + (row - i):
			return False
	return True


def solve(row, numCamerasPlaced, tigerCount):
	if row == n or numCamerasPlaced == c:
		for i in range(n):
			coordinate = str(i) + "," + str(board[i])
			if coordinate in tigerCoords:
				tigerCount += 1
		global maxTigerCount
		if tigerCount > maxTigerCount:
			maxTigerCount = tigerCount
	else:
		for i in range(n):
			if check_correctness(row, i):
				board[row] = i
				solve(row+1, numCamerasPlaced+1, tigerCount)


def dfs_backtracking():
	numCamerasPlaced = 0
	for i in range(n):
		board.append(0)
	solve(0, 0, 0)
	print(maxTigerCount)


"""
A* should be generating the next states dynamically, so you choose initial state based on heuristic. The heuristic should maximize tigers and minimize conflicts. So it should be #tigers+something. Need to figure out that something. Use priority queue for the A*. Could the minimize conflicts mean the number of open squares left on the board?
"""


def make_child(coordinate, astar_board):
	astar_board[coordinate] = True
	return astar_board


def get_sum_of_successors(x, y):
	successors = []
	successors.append([x - 1, y - 2])
	successors.append([x + 1, y - 2])
	successors.append([x - 1, y + 2])
	successors.append([x + 1, y + 2])
	successors.append([x - 2, y - 1])
	successors.append([x + 2, y - 1])
	successors.append([x - 2, y + 1])
	successors.append([x + 2, y + 1])
	sum = 0
	for coords in successors:
		coordinate = str(coords[0]) + "," + str(coords[1])
		if coordinate in tigerCoordsMap:
			sum += tigerCoordsMap[coordinate]
	return sum


def get_heuristic(x, y, cameras_left):
	coordinate = str(x) + "," + str(y)
	sum = get_sum_of_successors(x, y)
	if coordinate in tigerCoords:
		currScore = maxTigerCount + tigerCoordsMap[coordinate]
	else:
		currScore = maxTigerCount
	return currScore + sum * cameras_left


def check_correctness_astar(row, col, astar_board):
	for i in range(row):
		existing_camera_loc = astar_board[i]
		if existing_camera_loc == col or existing_camera_loc == col - (row - i) or existing_camera_loc == col + (row - i):
			return False
	return True


def init_astar(astar_board):
	global maxTigerCount
	global board
	for i in range(n):
		for j in range(n):
			coordinate = str(i) + "," + str(j)
			astar_board[coordinate] = False
			if coordinate in tigerCoords:
				heuristicMap[coordinate] = tigerCoordsMap[coordinate] + get_sum_of_successors(i, j) * c
			else:
				heuristicMap[coordinate] = get_sum_of_successors(i, j) * c
	first_choice = max(heuristicMap, key=lambda key: heuristicMap[key])
	astar_board[first_choice] = True
	choice_x = int(first_choice.split(",")[0])
	choice_y = int(first_choice.split(",")[1])
	board[choice_x] = choice_y
	if first_choice in tigerCoords:
		maxTigerCount = tigerCoordsMap[first_choice]
	return astar_board


def is_in_queue(x, q):
		return x in q.queue

"""
could be a good heuristic: theoretical max minus how many animals captured by placing on a specific square
another one: fill frontier with initial states using heuristic h(n) = -#tigers + #clashes
see if you can just use nqueens to come up with a configuration on the board
"""


def countTigers(map):
	sum = 0
	for i in range(n):
		for j in range(n):
			coordinate = str(i) + "," + str(j)
			if map[coordinate] and coordinate in tigerCoordsMap:
				sum += tigerCoordsMap[coordinate]
	return sum


def astar():
	# h(n) = current score + sum of all successors * cameras left
	numCamerasLeft = c
	astar_board = {}
	initNode = init_astar(astar_board)
	global frontier
	global explored
	global maxTigerCount
	global board
	frontier.put((0, initNode))

	while not frontier.empty():
		# if frontier.empty():
		# 	return 0
		node = frontier.get()
		node_map = node[1]
		print("in loop")
		if sum(1 for condition in node_map.values() if condition) == c:
			print("c: ", c)
			tigerCount = countTigers(node_map)
			if tigerCount > maxTigerCount:
				maxTigerCount = tigerCount
				print(maxTigerCount)
		for i in range(n):
			for j in range(n):
				coordinate = str(i) + "," + str(j)
				if not node_map[coordinate]:
					if check_correctness(i, j):
						board[i] = j
						child = node_map
						child[coordinate] = True
						frontier.put((-1*get_heuristic(i, j, numCamerasLeft) , child))


"""
Input: 
First line: strictly positive 32-bit integer n, the width and height of the nx 
npark area, n<= 15
Second line: strictly positive 32-bit integer c, the number of camera traps, 
c <= n
Third line: strictly positive 32-bit integer a, the number of animals, a <= 100
Fourth line: algorithm to use, either astar for A* search or dfsfor depth-first 
search
Next a lines: the list of animal x,y coordinates, separated with the End-of-line 
character LF. 
"""


def read_input(file):
	global tigerCoords
	global tigerCoordsMap
	global board
	f = open(file, "r")
	count = 0
	dfs = False
	tigerCoords = []
	for x in f:
		count += 1
		x = x.rstrip()
		if count == 1:
			global n
			n = int(x)
			for i in range(n):
				board.append(0)
		elif count == 2:
			global c
			c = int(x)
		elif count == 3:
			global a
			a = int(x)
		elif count == 4:
			if x == "dfs":
				dfs = True
		else:
			tigerCoords.append(x)
			if x in tigerCoordsMap:
				tigerCoordsMap[x] += 1
			else:
				tigerCoordsMap[x] = 1
	if dfs:
		dfs_backtracking()
	else:
		dfs_backtracking()
		# astar()
	print(board)
	print(maxTigerCount)


read_input("input.txt")







