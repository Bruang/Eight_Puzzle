# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 17:01:53 2016

@author: Haoxiang
"""

from enum import Enum
import copy
import Queue
import math
import time

MAX_QUEUE_SIZE = 100000
MAX_NODE = 1000000
MAX_DEPTH = 50


class Move(Enum):
    up = 1
    down = 2
    left = 3
    right = 4
    
class VisitedGrid:
    def __init__(self,n):
        self.visited = {}
        self.n = n
        
    def transform(self,grid):
        s = ""
        for i in xrange(self.n):
            for j in xrange(self.n):
                s += str(grid[i][j])
        return s
                
    def append(self,grid):
        s = self.transform(grid)
        self.visited[s] = True

    def is_visited(self,grid):
        s = self.transform(grid)
        if s in self.visited:
            return True
        else:
            return False

class State:
    def __init__(self,start,n,m=[]):
        self.grid = copy.deepcopy(start)
        self.n = n
        self.moves = copy.deepcopy(m)
        for i in xrange(n):
            for j in xrange(n):
                if self.grid[i][j] == 0:
                    self.pos = (i,j)
        
    def get_possible_moves(self):
        x = self.pos[0]
        y = self.pos[1]
        
        pos_moves = []
        if x != 0:
            pos_moves.append(Move.up)
        if y != 0:
            pos_moves.append(Move.left)
        if x != (self.n - 1):
            pos_moves.append(Move.down)
        if y != (self.n - 1):
            pos_moves.append(Move.right)       
        return pos_moves
        
    def get_distance(self):
        sum_dis = .0
        count = 0
        for i in xrange(self.n):
            for j in xrange(self.n):
                sum_dis += math.fabs(self.grid[i][j] - count)
                count += 1
        return sum_dis
    
    def move(self, m):
        x = self.pos[0]
        y = self.pos[1]
        new_grid = copy.deepcopy(self.grid)
        if m == Move.down:
            new_grid[x+1][y] = self.grid[x][y]
            new_grid[x][y] = self.grid[x+1][y]
        if m == Move.up:
            new_grid[x-1][y] = self.grid[x][y]
            new_grid[x][y] = self.grid[x-1][y]
        if m == Move.right:
            new_grid[x][y+1] = self.grid[x][y]
            new_grid[x][y] = self.grid[x][y+1]
        if m == Move.left:
            new_grid[x][y-1] = self.grid[x][y]
            new_grid[x][y] = self.grid[x][y-1]
        new_state = State(new_grid,self.n,self.moves)
        new_state.moves.append(m)
        return new_state
    
    def is_goal(self):
        count = 0
        for i in xrange(self.n):
            for j in xrange(self.n):
                if self.grid[i][j] != count:
                    return False
                count += 1
        return True
        
def bfs_solution(start_grid):
    start = State(start_grid,len(start_grid))
    queue = Queue.Queue(MAX_QUEUE_SIZE)
    queue.put(start)
    goal = start.is_goal()
    new_state = start
    count = 0
    visitedGrid = VisitedGrid(len(start_grid))
    while not goal and count <MAX_NODE:
        state = queue.get()
        moves = state.get_possible_moves()
        for m in moves:
            count = count+1
            new_state = state.move(m)
            if visitedGrid.is_visited(new_state.grid):
                continue
            else:
                visitedGrid.append(new_state.grid)
                if new_state.is_goal():
                    goal = True
                    break
                queue.put(new_state)
    print queue.qsize()
    print new_state.grid
    print new_state.moves
    
def dfs_solution(start_grid):
    start = State(start_grid,len(start_grid))
    stack = Queue.LifoQueue(MAX_QUEUE_SIZE)
    stack.put(start)
    goal = start.is_goal()
    new_state = start
    count = 0
    visitedGrid = VisitedGrid(len(start_grid))
    while not goal and count <MAX_NODE:
        state = stack.get()
        if len(state.moves)>MAX_DEPTH:
            continue
        moves = state.get_possible_moves()
        for m in moves:
            count = count+1
            new_state = state.move(m)
            if visitedGrid.is_visited(new_state.grid):
                continue
            else:
                visitedGrid.append(new_state.grid)
                if new_state.is_goal():
                    goal = True
                    break
                stack.put(new_state)
    print stack.qsize()
    print new_state.grid
    print new_state.moves
    
def a_search_solution(start_grid):
    start = State(start_grid,len(start_grid))
    p_queue = Queue.PriorityQueue(MAX_QUEUE_SIZE)
    p_queue.put((start.get_distance(),start))
    goal = start.is_goal()
    new_state = start
    count = 0
    visitedGrid = VisitedGrid(len(start_grid))
    while not goal and count <MAX_NODE:
        dis,state = p_queue.get()
        if len(state.moves)>MAX_DEPTH:
            continue
        moves = state.get_possible_moves()
        for m in moves:
            count = count+1
            new_state = state.move(m)
            if visitedGrid.is_visited(new_state.grid):
                continue
            else:
                visitedGrid.append(new_state.grid)
                if new_state.is_goal():
                    goal = True
                    break
                p_queue.put((new_state.get_distance(),new_state))
    print p_queue.qsize()
    print new_state.grid
    print new_state.moves
    

#extreme case
print "Extreme Case:"
grid_extreme = [[0, 8, 7],[6, 5, 4],[3, 2, 1]]

start_time = time.time()
bfs_solution(grid_extreme)
end_time = time.time()
print "BFS:"
print str(end_time - start_time) + " seconds"


start_time = time.time()
dfs_solution(grid_extreme)
end_time = time.time()
print "DFS:"
print str(end_time - start_time) + " seconds"

start_time = time.time()
a_search_solution(grid_extreme)
end_time = time.time()
print "A* Search:"
print str(end_time - start_time) + " seconds"



