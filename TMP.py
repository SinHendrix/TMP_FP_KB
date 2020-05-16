from pygame.locals import *
import time
import pygame
import queue
import networkx as nx
import threading
import time

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
  def __init__(self, maze, real_x, real_y):
    self.key_left = 4
    self.maze = maze
    self.real_x = 5
    self.real_y = 0
    self.x = self.real_x * 44
    self.y = self.real_y * 44
    self.speed = 44
    self.finish = 0
    
  def moveRight(self):
    if self.real_x != 8 and self.maze[self.real_y * 9 + self.real_x + 1] != '1':
      if self.maze[self.real_y * 9 + self.real_x + 1] == 'F' and self.key_left > 0:
        return
      self.real_x = self.real_x + 1
      self.x = self.x + self.speed

  def moveLeft(self):
    if self.real_x != 0 and self.maze[self.real_y * 9 + self.real_x - 1] != '1':
      if self.maze[self.real_y * 9 + self.real_x + 1] == 'F' and self.key_left > 0:
        return
      self.real_x = self.real_x - 1
      self.x = self.x - self.speed

  def moveUp(self):
    if self.real_y != 0 and self.maze[(self.real_y - 1) * 9 + self.real_x] != '1':
      if self.maze[(self.real_y - 1) * 9 + self.real_x] == 'F' and self.key_left > 0:
        return
      self.real_y = self.real_y - 1
      self.y = self.y - self.speed

  def moveDown(self):
    if self.real_y != 8 and self.maze[(self.real_y + 1) * 9 + self.real_x] != '1':
      if self.maze[(self.real_y + 1) * 9 + self.real_x] == 'F' and self.key_left > 0:
        return
      
      self.real_y = self.real_y + 1
      self.y = self.y + self.speed

class Maze:
  def __init__(self, maze, m, n, x, y):
    self.M = m
    self.N = n
    self.maze = maze
    self.x = x
    self.y = y

  def draw(self, display_surf, bush_image_surf, key_image_surf, door_image_surf):
    bx = 0
    by = 0
    dx = self.x
    dy = self.y
    for i in self.maze:
      if self.maze[ bx + (by*self.M) ] == '1':
        display_surf.blit(bush_image_surf,( (bx + dx) * 44 , (by + dy) * 44))

      if self.maze[ bx + (by*self.M) ] == 'A' or self.maze[ bx + (by*self.M) ] == 'B' or self.maze[ bx + (by*self.M) ] == 'C' or self.maze[ bx + (by*self.M) ] == 'D' :
        display_surf.blit(key_image_surf,( (bx + dx) * 44 , (by + dy) * 44))

      if self.maze[ bx + (by*self.M) ] == 'F':
        display_surf.blit(door_image_surf,( (bx + dx) * 44 , (by + dy) * 44))

      bx = bx + 1
      if bx > self.M-1:
        bx = 0 
        by = by + 1


class App:
  windowWidth = 44 * 18
  windowHeight = 44 * 9
  player = 0
  loading = True
  full_path = ''

  def __init__(self):
    self._running = True
    self._display_surf = None
    self._image_surf = None
    self._bush_surf = None
    self._key_surf = None
    self._door_surf = None
    
    self.hard_maze = [['1', '1', '1', '1', '1', 'S', '1', '1', '1'], 
                      ['1', '0', 'D', '0', '0', '0', '0', '0', '1'], 
                      ['1', '0', '1', '1', '0', '1', '1', 'C', '1'], 
                      ['1', '0', '1', '0', '0', '0', '1', '0', '1'], 
                      ['1', '0', '1', '0', '1', '0', '1', '0', '1'], 
                      ['1', '0', '1', '0', '1', 'B', '1', '0', '1'], 
                      ['1', '0', '1', '0', '1', '0', '1', '1', '1'], 
                      ['1', 'A', '0', '0', '0', '0', '0', '0', '1'], 
                      ['1', '1', '1', '1', '1', '1', '1', 'F', '1'] ]

    self.game_maze = []
    for features in self.hard_maze:
      for feature in features:
        self.game_maze.append(feature)

    self.player_maze = self.game_maze.copy()

    self.player = Player(self.player_maze, 9 + 5, 0)
    self.robot = Player(self.game_maze, 5, 0)

    self.maze = Maze(self.game_maze, 9, 9, 0, 0)
    self.player_right_maze = Maze(self.player_maze, 9, 9, 9, 0)

  def on_init(self):
    self._display_surf.fill((255, 255, 255)) 
    self._running = True
    self._image_surf = pygame.image.load("assets/mazeman.png").convert()
    self._bush_surf = pygame.image.load("assets/bush.png").convert()
    self._key_surf = pygame.image.load("assets/key.png").convert()
    self._player_door_surf = pygame.image.load("assets/door.png").convert()
    self._robot_door_surf = pygame.image.load("assets/door.png").convert()

  def on_event(self, event):
    if event.type == QUIT:
      self._running = False

  def on_loop(self):
    pass
  
  def on_render(self):
    self._display_surf.fill((255, 255, 255))
    feature = self.game_maze[self.robot.real_y * 9 + self.robot.real_x]
    if feature == 'A' or feature == 'B' or feature == 'C' or feature == 'D':
      self.game_maze[self.robot.real_y * 9 + self.robot.real_x] = '0'
      self.robot.key_left = self.robot.key_left - 1
      if self.robot.key_left == 0:
        self._robot_door_surf = pygame.image.load("assets/unlocked_door.png").convert()

    player_feature = self.player_maze[self.player.real_y * 9 + self.player.real_x]
    if player_feature == 'A' or player_feature == 'B' or player_feature == 'C' or player_feature == 'D':
      self.player_maze[self.player.real_y * 9 + self.player.real_x] = '0'
      self.player.key_left = self.player.key_left - 1
      if self.player.key_left == 0:
        self._player_door_surf = pygame.image.load("assets/unlocked_door.png").convert()

    self.maze.draw(self._display_surf, self._bush_surf, self._key_surf, self._robot_door_surf)
    self.player_right_maze.draw(self._display_surf, self._bush_surf, self._key_surf, self._player_door_surf)

    self._display_surf.blit(self._image_surf,(self.player.x + (9 * 44), self.player.y))
    self._display_surf.blit(self._image_surf,(self.robot.x, self.robot.y))
    pygame.display.flip()

  def on_cleanup(self):
    pygame.quit()

  def loadingScreen(self):
    font = pygame.font.Font('freesansbold.ttf', 32) 
    self._display_surf.fill((255, 255, 255)) 
    loadingText = 'Now Loading'
    text = font.render(loadingText, True, (0, 0, 0), (255, 255 ,255)) 
      
    textRect = text.get_rect()  
    textRect.center = (self.windowWidth // 2, self.windowHeight // 2) 

    self._display_surf.blit(text, textRect) 
    pygame.display.flip()

    while (self.loading == True):
      self._display_surf.fill((255, 255, 255)) 
      loadingText = 'Now Loading'
      for i in range(0, 3):
        loadingText = loadingText + '.'
        text = font.render(loadingText, True, (0, 0, 0), (255, 255 ,255)) 
        self._display_surf.blit(text, textRect) 
        pygame.display.update()
        time.sleep(0.5)

  def robotThread(self):
    for path in self.full_path:
      if path == 'L':
        self.robot.moveLeft()

      if path == 'R':
        self.robot.moveRight()

      if path == 'U':
        self.robot.moveUp()

      if path == 'D':
        self.robot.moveDown()

      time.sleep(0.3)
      self.on_loop()
      self.on_render()

  def on_execute(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
    pygame.display.set_caption('Travelling Mazeman Problem')

    thread = threading.Thread(target=self.loadingScreen)
    thread.start()

    all_path = {}

    graph, all_path = mazeToGraph(self.hard_maze)
    local_minimum_condition = []
    local_minimum_condition.append('S')
    local_minimum_objectives, local_minimum_cost = evaluate(graph, ['A', 'B', 'C', 'D'])
    for objective in local_minimum_objectives:
      local_minimum_condition.append(objective)

    local_minimum_condition.append('F')

    for i in range (int(len(local_minimum_condition)) - 1) :
      self.full_path = self.full_path + str(all_path[local_minimum_condition[i] + local_minimum_condition[i + 1]])

    self.loading = False
    thread.join()

    if self.on_init() == False:
      self._running = False

    self.on_render()

    robot_thread = threading.Thread(target=self.robotThread)
    robot_thread.start()

    while (self._running):
      pygame.event.pump()
      event = pygame.event.wait()
      keys = pygame.key.get_pressed()

      if event.type == pygame.KEYDOWN: 
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