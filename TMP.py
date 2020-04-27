from pygame.locals import *
import time
import pygame
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

  
  while first_index in range(len(initial_condition) - 1):
    second_index = first_index + 1
    while second_index < len(initial_condition):
      modified_condition = initial_condition.copy()
      modified_condition[first_index], modified_condition[second_index] = initial_condition[second_index], initial_condition[first_index]
      modified_condition_cost = getTotalCost(graph, modified_condition)

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
    elif (maze[j][i] == '1'):
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

class Player:
  x = 5 * 44
  y = 0 * 44
  speed = 44

  def moveRight(self):
    self.x = self.x + self.speed

  def moveLeft(self):
    self.x = self.x - self.speed

  def moveUp(self):
    self.y = self.y - self.speed

  def moveDown(self):
    self.y = self.y + self.speed

class Maze:
  def __init__(self):
    self.M = 9
    self.N = 9
    self.maze = [ 1, 1, 1, 1, 1, 0, 1, 1, 1,
                  1, 0, 2, 0, 0, 0, 0, 0, 1,
                  1, 0, 1, 1, 0, 1, 1, 2, 1,
                  1, 0, 1, 0, 0, 0, 1, 0, 1,
                  1, 0, 1, 0, 1, 0, 1, 0, 1,
                  1, 0, 1, 0, 1, 2, 1, 0, 1,
                  1, 0, 1, 0, 1, 0, 1, 1, 1,
                  1, 2, 0, 0, 0, 0, 0, 0, 1,
                  1, 1, 1, 1, 1, 1, 1, 3, 1 ]

  def draw(self, display_surf, bush_image_surf, key_image_surf, door_image_surf):
    bx = 0
    by = 0
    for i in range(0,self.M*self.N):
      if self.maze[ bx + (by*self.M) ] == 1:
        display_surf.blit(bush_image_surf,( bx * 44 , by * 44))

      if self.maze[ bx + (by*self.M) ] == 2:
        display_surf.blit(key_image_surf,( bx * 44 , by * 44))

      if self.maze[ bx + (by*self.M) ] == 3:
        display_surf.blit(door_image_surf,( bx * 44 , by * 44))

      bx = bx + 1
      if bx > self.M-1:
        bx = 0 
        by = by + 1


class App:
  windowWidth = 800
  windowHeight = 600
  player = 0

  def __init__(self):
    self._running = True
    self._display_surf = None
    self._image_surf = None
    self._bush_surf = None
    self._key_surf = None
    self._door_surf = None
    self.player = Player()
    self.maze = Maze()

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
    pygame.display.set_caption('Travelling Mazeman Problem')
    self._running = True
    self._image_surf = pygame.image.load("assets/mazeman.png").convert()
    self._bush_surf = pygame.image.load("assets/bush.png").convert()
    self._key_surf = pygame.image.load("assets/key.png").convert()
    self._door_surf = pygame.image.load("assets/unlocked_door.png").convert()

  def on_event(self, event):
    if event.type == QUIT:
      self._running = False

  def on_loop(self):
    pass
  
  def on_render(self):
    self._display_surf.fill((255, 255, 255))
    self.maze.draw(self._display_surf, self._bush_surf, self._key_surf, self._door_surf)
    self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
    pygame.display.flip()

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    self.on_render()

    all_path = {}
    maze = []
    # n = int(input('size : '))
    # print('maze : ')
    # for i in range(n):
    #   row = input().split(' ')
    #   maze.append(row)
    maze = [['1', '1', '1', '1', '1', 'S', '1', '1', '1'], 
            ['1', '0', 'D', '0', '0', '0', '0', '0', '1'], 
            ['1', '0', '1', '1', '0', '1', '1', 'C', '1'], 
            ['1', '0', '1', '0', '0', '0', '1', '0', '1'], 
            ['1', '0', '1', '0', '1', '0', '1', '0', '1'], 
            ['1', '0', '1', '0', '1', 'B', '1', '0', '1'], 
            ['1', '0', '1', '0', '1', '0', '1', '1', '1'], 
            ['1', 'A', '0', '0', '0', '0', '0', '0', '1'], 
            ['1', '1', '1', '1', '1', '1', '1', 'F', '1']]

    graph, all_path = mazeToGraph(maze)
    local_minimum_condition = []
    local_minimum_condition.append('S')
    local_minimum_objectives, local_minimum_cost = evaluate(graph, ['A', 'B', 'C', 'D'])
    for objective in local_minimum_objectives:
      local_minimum_condition.append(objective)

    local_minimum_condition.append('F')
#         print('minimum steps found :', local_minimum_cost)

#         for path in local_minimum_condition:
#           if path == 'F':
#             print(path)
#           else:
#             print(path, end=' -> ')
#         print()

    # for i in range (int(len(local_minimum_condition)) - 1) :
      # print('Step', i + 1, ' : ', local_minimum_condition[i], '->', local_minimum_condition[i + 1])
      # printMaze(maze, local_minimum_condition[i], all_path[local_minimum_condition[i] + local_minimum_condition[i + 1]])

    full_path = ''
    for i in range (int(len(local_minimum_condition)) - 1) :
      full_path = full_path + str(all_path[local_minimum_condition[i] + local_minimum_condition[i + 1]])

    for path in full_path:
      if path == 'L':
        self.player.moveLeft();
        time.sleep(0.7)

      if path == 'R':
        self.player.moveRight();
        time.sleep(0.7)

      if path == 'U':
        self.player.moveUp();
        time.sleep(0.7)

      if path == 'D':
        self.player.moveDown();
        time.sleep(0.7)

      self.on_loop()
      self.on_render()

    while (self._running):
      pygame.event.pump()
      keys = pygame.key.get_pressed()
  
      if (keys[K_RIGHT]):
        self.player.moveRight()

      if (keys[K_LEFT]):
        self.player.moveLeft()

      if (keys[K_UP]):
        self.player.moveUp()

      if (keys[K_DOWN]):
        self.player.moveDown()

      if (keys[K_ESCAPE]):
        self._running = False

      self.on_loop()
      self.on_render()
    self.on_cleanup()
 
if __name__ == "__main__" :
  theApp = App()
  theApp.on_execute()