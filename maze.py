import random
import time
from threading import Thread
import sys
import termios
import tty
import os

width, height = os.get_terminal_size()
width /= 2
WIDTH = int(width) if width % 2 == 1 else int(width - 1)
HEIGHT = height - 2 if height % 2 == 1 else height - 3
EMPTY = '  '
WALL = "\033[37;47m"
RESEST = "\033[m"
USER = "\033[31;41m"
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'
maze = [["W" for _ in range(WIDTH)] for _ in range(HEIGHT)]
hasVisited = [(1, 1)]

def generate_maze():
    random.seed(time.time() * 10**7)
    visit(1, 1)
    maze[1][0] = "S"
    maze[-2][-1] = "S"

def printMaze(maze):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if maze[y][x] == "W":
                print(WALL, "  ", RESEST, sep="", end="")
            elif maze[y][x] == "S":
                print("  ", end="")
            elif maze[y][x] == "P":
                print(USER, "  " +  RESEST, sep="", end="")
        print()


def visit(x, y):
    global maze
    maze[y][x] = "S"

    while True:
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)

        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)

        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)

        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            return
        else:
            nextIntersection = random.choice(unvisitedNeighbors)
            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[y - 1][x] = "S"
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[y + 1][x] = "S"
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[y][x - 1] = "S"
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[y][x + 1] = "S"

            hasVisited.append((nextX, nextY))
            visit(nextX, nextY)


class Maze:
    def __init__(self):
        self.user_x = 0
        self.user_y = 1
        self.direction = None
        
    def play(self):
        self.start_input_thread()
        generate_maze()
        maze[self.user_y][self.user_x] = "P"
        
        while True:
            print("\033[H")
            self.update_user_place()
            printMaze(maze)
            if self.user_x == WIDTH - 1 and self.user_y == HEIGHT - 2:
                print("YOU WON!")
                return
            time.sleep(0.1)
            
    def update_user_place(self):
        y = self.user_y
        x = self.user_x
        maze[y][x] = "S"
        if self.direction == "R" and x < WIDTH -1 and maze[y][x+1] != "W":
            x += 1
        if self.direction == "L" and x > 0 and maze[y][x-1] != "W":
            x -= 1
        if self.direction == "D" and maze[y+1][x] != "W":
            y += 1
        if self.direction == "U" and maze[y-1][x] != "W":
            y -= 1
        self.user_x = x
        self.user_y = y
        maze[self.user_y][self.user_x] = "P"
        
    def start_input_thread(self):
        input_thread = Thread(target=self.read_input)
        input_thread.start()
        
    def read_input(self):
        K_RIGHT = b'\x1b[C'
        K_LEFT  = b'\x1b[D'
        K_UP  = b'\x1b[A'
        K_DOWN = b'\x1b[B'
        for key in self.read_keys():
            if key == K_RIGHT:
                self.direction = "R"
            elif key == K_LEFT:
                self.direction = "L"
            elif key == K_DOWN:
                self.direction = "D"
            elif key == K_UP:
                self.direction = "U"
            
        
        
    def read_keys(self):
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)
        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            while True:
                yield sys.stdin.buffer.read1()
        except KeyboardInterrupt:
            yield None
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)
            

os.system("clear")
m = Maze()
m.play()
