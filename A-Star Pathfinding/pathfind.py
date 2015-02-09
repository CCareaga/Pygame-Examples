import numpy
from heapq import *

def heuristic(a, b, pathing):
    
    x = abs(a[0]-b[0])
    y = abs(a[1]-b[1])

    if pathing == '*':

        if x > y:
            return 14*y + 10*(x - y)
        else:
            return 14*x + 10*(y - x)
    else:
        return 10*(x + y)

def astar(array, start, goal, pathing):

    if pathing == '+':
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    else:
        neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal, pathing)}
    oheap = []
    checked = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]
        checked.append(current)

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]

            return list(reversed(data)), checked

        array[current[0], current[1]] = 2
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor, pathing)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array.flat[array.shape[1] * neighbor[0]+neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if array[neighbor[0]][neighbor[1]] == 2 and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal, pathing)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False