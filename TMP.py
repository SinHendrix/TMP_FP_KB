import queue
import networkx as nx

def mazeToGraph(maze):
  graph = nx.Graph()
  all_path = {}
  for i in range(0, 4):
    key = chr(ord('A') + i)
    all_path['S' + key] = findPath(maze, 'S', key)
    all_path[key + 'S'] = findPath(maze, key, 'S')
    graph.add_edge(key, 'S', weight=len(all_path['S' + key]))

    all_path['F' + key] = findPath(maze, 'F', key)
    all_path[key + 'F'] = findPath(maze, key, 'F')
    graph.add_edge(key, 'F', weight=len(all_path[key + 'F']))
    
    for j in range(3 - i):
      target = chr(ord(key) + j + 1)
      
      all_path[key + target] = findPath(maze, key, target)
      all_path[target + key] = findPath(maze, target, key)
      graph.add_edge(key, target, weight=len(all_path[key + target]))
      
  return graph, all_path

def getTotalCost(graph, condition):
  total_cost = int(graph['S'][condition[0]]['weight']) + int(graph[condition[len(condition) - 1]]['F']['weight'])
  for index in range(len(condition) - 1):
    total_cost = total_cost + int(graph[condition[index]][condition[index + 1]]['weight'])
  return total_cost

def evaluate(graph, initial_condition):
  local_minimum_cost = getTotalCost(graph, initial_condition)
  local_minimum_condition = initial_condition.copy()
  local_minimum_changed = False

  first_index = 0

  # new_initial_condition = 'S'
  # for path in initial_condition:
  #   new_initial_condition = new_initial_condition + ' -> ' + path
  # new_initial_condition  = new_initial_condition + '-> F'

  # print('evaluating initial condition : ' + str(new_initial_condition))
  
  # new_local_minimum_condition = 'S'
  # for path in local_minimum_condition:
  #   new_local_minimum_condition = new_local_minimum_condition + ' -> ' + path
  # new_local_minimum_condition = new_local_minimum_condition + '-> F'

  # print(str(local_minimum_condition) + ', cost = ' + str(local_minimum_cost))

  while first_index in range(len(initial_condition) - 1):
    second_index = first_index + 1
    while second_index < len(initial_condition):
      modified_condition = initial_condition.copy()
      modified_condition[first_index], modified_condition[second_index] = initial_condition[second_index], initial_condition[first_index]
      modified_condition_cost = getTotalCost(graph, modified_condition)

      # new_modified_condition = 'S'
      # for path in modified_condition:
      #   new_modified_condition = new_modified_condition + ' -> ' + path
      # new_modified_condition = new_modified_condition + '-> F'
      # print(str(modified_condition) + ', cost = ' + str(modified_condition_cost))

      if modified_condition_cost < local_minimum_cost:
        local_minimum_cost = modified_condition_cost
        local_minimum_condition = modified_condition.copy()
        local_minimum_changed = True

      second_index = second_index + 1
    first_index = first_index + 1

  if local_minimum_changed:
    return evaluate(graph, local_minimum_condition)

  return local_minimum_condition, local_minimum_cost

def printMaze(maze, start_pos, path):
  for y in range (len(maze)):
    for x, pos in enumerate(maze[y]):
      if pos == start_pos:
        starti = x
        startj = y
        break

  i = starti
  j = startj

  pos = set()
  for move in path:
    if move == 'L':
      i -= 1

    elif move == 'R':
      i += 1

    elif move == 'U':
      j -= 1

    elif move == 'D':
      j += 1
    pos.add((j, i))
  
  for j, row in enumerate(maze):
    for i, col in enumerate(row):
      if (j, i) in pos:
        print('+ ', end='')
      else:
        print(col + ' ', end='')
    print()
  print()

def valid(maze, moves, start_pos):
  for y in range (len(maze)):
    for x, pos in enumerate(maze[y]):
      if pos == start_pos:
        starti = x
        startj = y
        break

  i = starti
  j = startj

  for move in moves:
    if move == 'L':
      i -= 1

    elif move == 'R':
      i += 1

    elif move == 'U':
      j -= 1

    elif move == 'D':
      j += 1

    if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
      return False
    elif (maze[j][i] == '#'):
      return False

  return True

def findEnd(maze, moves, start_pos, finish_pos):
  for y in range (len(maze)):
    for x, pos in enumerate(maze[y]):
      if pos == start_pos:
        starti = x
        startj = y
        break

  i = starti
  j = startj
  for move in moves:
    if move == 'L':
      i -= 1

    elif move == 'R':
      i += 1

    elif move == 'U':
      j -= 1

    elif move == 'D':
      j += 1


  if maze[j][i] == finish_pos:
    return True

  return False

def findPath(maze, start_pos, finish_pos):
  nums = queue.Queue()
  nums.put('')
  path = ''
  while not findEnd(maze, path, start_pos, finish_pos): 
    path = nums.get()
    for j in ['L', 'R', 'U', 'D']:
      next_path = path + j
      if valid(maze, next_path, start_pos):
        nums.put(next_path)

  return path

all_path = {}
maze = []
n = int(input('size : '))
print('maze : ')
for i in range(n):
  row = input().split(' ')
  maze.append(row)

# maze example :
# # # # # S # # #
# . D . . . . . #
# . # # . # # C #
# . # . . . # . #
# . # . # . # . #
# . # . # B # . #
# . # . # . # # #
# A . . . . . . #
# # # # # # # F #

print()

graph, all_path = mazeToGraph(maze)
local_minimum_condition = []
local_minimum_condition.append('S')
local_minimum_objectives, local_minimum_cost = evaluate(graph, ['A', 'B', 'C', 'D'])
for objective in local_minimum_objectives:
  local_minimum_condition.append(objective)

local_minimum_condition.append('F')
print('minimum steps found :', local_minimum_cost)

for path in local_minimum_condition:
  if path == 'F':
    print(path)
  else:
    print(path, end=' -> ')
print()

for i in range (int(len(local_minimum_condition)) - 1) :
  print('Step', i + 1, ' : ', local_minimum_condition[i], '->', local_minimum_condition[i + 1])
  printMaze(maze, local_minimum_condition[i], all_path[local_minimum_condition[i] + local_minimum_condition[i + 1]])
