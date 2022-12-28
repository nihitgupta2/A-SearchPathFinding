# Nihit Gupta 
# Id 20759430
import numpy as np 
import matplotlib.pyplot as plt
import copy

# Each square in the grid is a node
class Node:
    def __init__(self,position):
        self.position = position
        self.fnValue = 0
        self.gnValue = 0
        self.hnValue = 0
        self.parent = None


def AstarSearchAlgo(maze,startPosition,endPositions):
    startNode = Node(startPosition)
    startNode.gnValue = 1
    openQueue = [startNode]
    closedQueue = []
    currentNode = None
    nodeCounter = 0
    finalEndNode = None
    allNodesExpanded = []
    traversalDict = {}
    while openQueue!=[]: 
        currentNode = openQueue.pop(0)      # pop first element of open queue
        closedQueueCordinates = [i.position for i in closedQueue]   
        if currentNode.position in closedQueueCordinates:   # check if popped element that is [x,y] position exists in closed queue
            continue                                        # if exists then ignore and just move on to next open queue element
        allNodesExpanded.append(currentNode.position)
        nodeCounter+=1
        if currentNode.position in endPositions:
            finalEndNode = currentNode
            break
            # goal node found so break
        else:
            childNodes = findAllChildNodes(maze,currentNode)
            childNodesNoRep = []
            for node in childNodes:
                if node.position not in closedQueueCordinates:      # check if child nose already exists in closed queue
                    node.hnValue = manhattanDistance(node.position,endPositions)
                    node.gnValue = (node.parent.gnValue)+1 # parent node gn or technically currNode gn
                    node.fnValue = node.hnValue + node.gnValue
                    childNodesNoRep.append(node)
                else:
                    continue                                        #if exists in closed queue then ignore and move on to next child node
            openQueue.extend(childNodesNoRep)
            openQueue.sort(key=lambda s: s.fnValue)  #Open Queue is always sorted in ascending order of Fn value of nodes so that minimum one gets popped
            closedQueue.append(currentNode)
    
    route = nodesFinder(finalEndNode)
    routeLength = len(route)
    if route[routeLength-1].position==endPositions[1]:
        print(f"The Goal node found is E2 - {endPositions[1]}")
    else:
        print(f"The Goal node found is E1 - {endPositions[0]}")
    print(f"The total nodes expanded is {nodeCounter}")
    print(f"The total cost is {route[routeLength-1].gnValue}")
    return route
    

def nodesFinder(finalEndNode):
    # this function finds the actual path taken by the agent
    goalNode = finalEndNode
    totalPath = [goalNode]
    #this function takes a goal node and finds the parent node
    #using recusrsion we find all parent nodes and thus get the actual path
    def recursiveFinding(goalNode):
        if goalNode.parent==None:
            return 0
        else:
            iterNode = goalNode.parent
            totalPath.append(iterNode)
            recursiveFinding(iterNode)

    finish = recursiveFinding(goalNode)
    totalPath.reverse()
    return totalPath

 
def manhattanDistance(p1,endPositions): # Manhattan Distance is the heuristic value
    e1 = endPositions[0]
    e2 = endPositions[1]
    result = min((abs(e1[0]-p1[0]) + abs(e1[1]-p1[1])),(abs(e2[0]-p1[0]) + abs(e2[1]-p1[1])))
    return result


def findAllChildNodes(maze,currNode):
    upPosition = None
    downPosition = None
    leftPosition = None
    rightPosition = None
    childNodes = None
    finalChildren = None
    # checking non is out of boud or blocked and then considering them as a child node
    if (currNode.position[1]+1)<25 and (currNode.position[1]+1)>=0 and maze[currNode.position[1]+1][currNode.position[0]]!=1:
        upPosition = Node([currNode.position[0],currNode.position[1]+1])

    if (currNode.position[1]-1)<25 and (currNode.position[1]-1)>=0 and maze[currNode.position[1]-1][currNode.position[0]]!=1:
        downPosition = Node([currNode.position[0],currNode.position[1]-1])
    
    if (currNode.position[0]+1)<25 and (currNode.position[0]+1)>=0 and maze[currNode.position[1]][currNode.position[0]+1]!=1:
        rightPosition = Node([currNode.position[0]+1,currNode.position[1]])
    
    if (currNode.position[0]-1)<25 and (currNode.position[0]-1)>=0 and maze[currNode.position[1]][currNode.position[0]-1]!=1:
        leftPosition = Node([currNode.position[0]-1,currNode.position[1]])
    
    childNodes = [leftPosition,upPosition,rightPosition,downPosition]
    finalChildren = [i for i in childNodes if i is not None]
    for i in finalChildren:
        i.parent=currNode
    
    return finalChildren


def generateGraph(maze,actualPath):
    
    # "_" means blocks that can used i.e. positions where agent can go
    # "X" means blocks that are blocked and the agent 
    # "*" represents the blocks agent took in the actual path

    for i in range(24,-1,-1):
        mazeLine = ""
        for j in range(25):
            if [j,i] in actualPath:
                if i==11 and j==2:      # Start never changes
                    mazeLine+=" S "
                elif i==21 and j==2:    # E2 never changes
                    mazeLine+=" E "
                elif i==19 and j==23:   # E1 never changes
                    mazeLine+=" E "
                else:
                    mazeLine+=" * "
            elif maze[i][j] == 0:
                mazeLine+=" _ "
            elif maze[i][j] == 1:
                mazeLine+=" X "
            else:
                mazeLine+=" * "
        print(mazeLine)


def generateColorGraph(maze,actualPath):
    maze_replica = maze.copy()          # Copy so that actual maze doesnt change
    for i in range(24,-1,-1):
        for j in range(25):
            if [j,i] in actualPath:
                if i==11 and j==2:      # Start never changes
                    maze_replica[i][j]=100
                elif i==21 and j==2:    # E2 never changes
                    maze_replica[i][j]=100
                elif i==19 and j==23:   # E1 never changes
                    maze_replica[i][j]=100
                else:
                    maze_replica[i][j]=100
            elif maze_replica[i][j] == 0:
                maze_replica[i][j]=0
            elif maze_replica[i][j] == 1:
                maze_replica[i][j]=-100
            else:
                maze_replica[i][j]=100
    copymaze = []            
    for i in range(24,-1,-1):
        copymaze.append(maze_replica[i])
    H = np.array(copymaze)
    plt.imshow(H, interpolation='none')
    plt.show()
            

def main ():
    totalspots = [25,25]
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]
    # I have assumed that in the given map on Learn the 0,0 is the bottom left square and the square 
    # on its right is 1,0 and the square above 0,0 is 0,1 and so on 
    # However in the above 2D arrays every sublist is a row and first sublist is the bottom most row
    # so in order to access 9,11 graph value I use 11,9 in 2D Array.
    # The coordinate values in output corresponds to the GRAPH. 
    S = [2,11]      #start position 2,21
    E1 = [23,19]    #Exit position 1  23,19
    E2 = [2,21]     #Exit position 2 2,21
    endPositions = [E1,E2]
    print(f"------------------A* Search Algorithm with Heuristic -> Manhattan Distance------------------")
    pathRouteAstar = AstarSearchAlgo(maze,S,endPositions)             #invoking A* Algo that returns list of nodes in actual path
    print(f"------Complete Path to Exit Written------")
    pathInArray = [i.position for i in pathRouteAstar]                #list of positions of nodes in actual path                  
    print(pathInArray)
    print(f"------Complete Path to Exit Graph------")
    generateGraph(maze,pathInArray)                                   #Generate terminal grid with path
    print(f"------Complete Path to Exit Colored Graph------")
    generateColorGraph(maze,pathInArray)                              #Generate colored coded grid with path

if __name__ == '__main__':
    main()      #invoking the main function