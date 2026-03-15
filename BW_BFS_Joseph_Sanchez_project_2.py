import numpy as np
import pandas as pd
import time
from collections import deque
from pynput import keyboard
from pynput.keyboard import Key
import pygame
pygame.init()  

# JS4432

ppmm = 142 / 25.4 # 142 ppi of current display

height = int(ppmm*50) # 50mm box requirement
width = int(ppmm*180)


surface = pygame.display.set_mode((width, height))  # 50mm x 180mm
obstacle_color = (255, 192, 203)
char_color = (255, 80, 200)

# border
# these are the mathematical models of the letter geometry for the obstacle space
# J
J_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(117, 39, 54, 122), width=30) # basic geometry of rectangle that forms "J"
J_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(49, 89, 122, 122), start_angle=2.90, stop_angle=0, width=60) 
# S
S_arc = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169, 39, 112, 112), start_angle=0.1, stop_angle=4.81239, width=60)
S_arc_2 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(169, 94, 122, 122), start_angle=-3.24, stop_angle=1.97, width=60)
# 4 432
four_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274, 39, 54, 97), width=30)
four_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(274, 89, 97, 54), width=30)
four_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(324, 39, 54, 172), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374, 39, 54, 97), width=30)
four_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(374, 89, 97, 54), width=30)
four_rect6 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(424, 39, 54, 172), width=30)
# 3
three_rect = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464, 39, 112, 112), start_angle=4.71239, stop_angle=2.85619, width=60)
three_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(494, 97, 62, 54), width=30)
three_rect3 = pygame.draw.arc(surface, obstacle_color, pygame.Rect(464, 99, 112, 112), start_angle=3.42699, stop_angle=1.5708, width=60)
# 2
two_rect = pygame.draw.rect(surface, obstacle_color, pygame.Rect(589, 39, 102, 54), width=30)
two_rect2 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(649, 39, 54, 114), width=30)
two_rect3 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(624, 99, 54, 54), width=30)
two_rect4 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(599, 129, 54, 54), width=30)
two_rect5 = pygame.draw.rect(surface, obstacle_color, pygame.Rect(579, 159, 142, 54), width=30)


# characters
# J
J_rect = pygame.draw.rect(surface, char_color, pygame.Rect(128, 50, 32, 100), width=30)
J_arc = pygame.draw.arc(surface, char_color, pygame.Rect(60, 100, 100, 100), start_angle=3.1415, stop_angle=0, width=30)
# S
S_arc = pygame.draw.arc(surface, char_color, pygame.Rect(180, 50, 90, 90), start_angle=0.5, stop_angle=4.71239, width=30)
S_arc_2 = pygame.draw.arc(surface, char_color, pygame.Rect(180, 110, 90, 90), start_angle=-2.64, stop_angle=1.57, width=30)
# 4 432
four_rect = pygame.draw.rect(surface, char_color, pygame.Rect(285, 50, 32, 75), width=30)
four_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(285, 100, 75, 32), width=30)
four_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(335, 50, 32, 150), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 50, 32, 75), width=30)
four_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 100, 75, 32), width=30)
four_rect6 = pygame.draw.rect(surface, char_color, pygame.Rect(435, 50, 32, 150), width=30)
# 3
three_rect = pygame.draw.arc(surface, char_color, pygame.Rect(475, 50, 90, 90), start_angle=4.71239, stop_angle=2.35619, width=30)
three_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(505, 108, 40, 32), width=30)
three_rect3 = pygame.draw.arc(surface, char_color, pygame.Rect(475, 110, 90, 90), start_angle=3.92699, stop_angle=1.5708, width=30)
# 2
two_rect = pygame.draw.rect(surface, char_color, pygame.Rect(600, 50, 80, 32), width=30)
two_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(660, 50, 32, 92), width=30)
two_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(635, 110, 32, 32), width=30)
two_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(610, 140, 32, 32), width=30)
two_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(590, 170, 120, 32), width=30)


# these if statement branches are for the user input of start and goal state x and y coordinates
# get start state

start_state_x = input("Enter Start State x coordinate: ")
start_state_x = int(start_state_x)
start_state_y = input("Enter Start State y coordinate: ")
start_state_y = int(start_state_y)

if start_state_x <= 0:
    print("Error. Enter x value greater than 0")
    start_state_x = input("Enter Start State x coordinate: ")
    start_state_x = int(start_state_x)

elif start_state_x >= width:
    print("Error. Enter x value less than ", width)
    start_state_x = input("Enter Start State x coordinate: ")
    start_state_x = int(start_state_x)

if start_state_y <= 0:
    print("Error. Enter y value greater than 0")
    start_state_y = input("Enter Start State y coordinate: ")
    start_state_y = int(start_state_y)

elif start_state_y >= height:
    print("Error. Enter y value less than ", height)
    start_state_y = input("Enter Start State y coordinate: ")
    start_state_y = int(start_state_y)


start_color = surface.get_at((start_state_x, start_state_y)) # pixel value of the selected coordinate is checked

while start_color != (0, 0, 0): # the selected pixel value is checked agains the black background for proper selection. If the coordinate is not in the free space as 
                                # defined by the mathematical models above, then the user is prompted to try again
    print("Error. Selected coordinate is within character boundry. Please try again.")
    start_state_x = input("Enter Start State x coordinate: ")
    start_state_x = int(start_state_x)
    start_state_y = input("Enter Start State y coordinate: ")
    start_state_y = int(start_state_y)

    if start_state_x <= 0:
        print("Error. Enter x value greater than 0")
        start_state_x = input("Enter Start State x coordinate: ")
        start_state_x = int(start_state_x)

    elif start_state_x >= width:
        print("Error. Enter x value less than ", width)
        start_state_x = input("Enter Start State x coordinate: ")
        start_state_x = int(start_state_x)

    if start_state_y <= 0:
        print("Error. Enter y value greater than 0")
        start_state_y = input("Enter Start State y coordinate: ")
        start_state_y = int(start_state_y)

    elif start_state_y >= height:
        print("Error. Enter y value less than ", height)
        start_state_y = input("Enter Start State y coordinate: ")
        start_state_y = int(start_state_y)

    start_color = surface.get_at((start_state_x, start_state_y))
    

start_state = (start_state_y, start_state_x)


# get goal state

goal_state_x = input("Enter Goal State x coordinate: ")
goal_state_x = int(goal_state_x)
goal_state_y = input("Enter Goal State y coordinate: ")
goal_state_y = int(goal_state_y)

if goal_state_x <= 0:
    print("Error. Enter x value greater than 0")
    goal_state_x = input("Enter Goal State x coordinate: ")
    goal_state_x = int(goal_state_x)

elif goal_state_x >= width:
    print("Error. Enter x value less than ", width)
    goal_state_x = input("Enter Goal State x coordinate: ")
    goal_state_x = int(goal_state_x)

if goal_state_y <= 0:
    print("Error. Enter y value greater than 0")
    goal_state_y = input("Enter Goal State y coordinate: ")
    goal_state_y = int(goal_state_y)

elif goal_state_y >= height:
    print("Error. Enter y value less than ", height)
    goal_state_y = input("Enter GOal State y coordinate: ")
    goal_state_y = int(goal_state_y)


goal_color = surface.get_at((goal_state_x, goal_state_y))


while goal_color != (0, 0, 0):
    print("Error. Selected coordinate is within character boundry. Please try again.")
    goal_state_x = input("Enter Goal State x coordinate: ")
    goal_state_x = int(goal_state_x)
    goal_state_y = input("Enter Goal State y coordinate: ")
    goal_state_y = int(goal_state_y)


    if goal_state_x <= 0:
        print("Error. Enter x value greater than 0")
        goal_state_x = input("Enter Goal State x coordinate: ")
        goal_state_x = int(goal_state_x)

    elif goal_state_x >= width:
        print("Error. Enter x value less than ", width)
        goal_state_x = input("Enter Goal State x coordinate: ")
        goal_state_x = int(goal_state_x)

    if goal_state_y <= 0:
        print("Error. Enter y value greater than 0")
        goal_state_y = input("Enter Goal State y coordinate: ")
        goal_state_y = int(goal_state_y)

    elif goal_state_y >= height:
        print("Error. Enter y value less than ", height)
        goal_state_y = input("Enter Goal State y coordinate: ")
        goal_state_y = int(goal_state_y)

    goal_color = surface.get_at((goal_state_x, goal_state_y))
    

goal_state = (goal_state_y, goal_state_x)


# conversion for movement attempts
def tuple_to_list(state):
    return list(state) 


def list_to_tuple(state):
    return tuple(state) 


# surface = pygame.display.set_mode((900, 250))  # window
robot_radius = 5
# 
# Moving the robot
# these functions provide the 8 degrees of freedom for the point robot
def move_left(state, row, col):

    original_state = state # original position is saved

    if col - 1 > 0:

        state = tuple_to_list(state) # conversion for easier handling

        state[1] = state[1]-1 
        
        state = list_to_tuple(state) # new position is updated
    # pygame.display.flip()

    new_color = surface.get_at((state[1], state[0])) # new pixel value is recorded

    if new_color[:3] == obstacle_color: # if the new pixel position is the same color as the defined characters then the pixel does not update
        state = original_state
    
    return state # returns either updated position or same position
    
def move_right(state, row, col):
    original_state = state

    if col + 1 < width:
        state = tuple_to_list(state) 
        state[1] = state[1]+1 
        state = list_to_tuple(state) 
    # pygame.display.flip()
    
    print("current coord: ", state[0], state[1])
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_up(state, row, col):
    original_state = state

    if row - 1 > 0:
        state = tuple_to_list(state)
        state[0] = state[0]-1
        # state[row-1][col] = 0 
        state = list_to_tuple(state)
    # pygame.display.flip()
   
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_down(state, row, col):
    original_state = state

    if row + 1 < height:
        state = tuple_to_list(state)
        state[0] = state[0]+1
        state = list_to_tuple(state)
    # pygame.display.flip()
    
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_diag_up_left(state, row, col):
    original_state = state

    if col - 1 > 0 and row - 1 > 0:
        state = tuple_to_list(state) 
        state[0] = state[0]-1 
        state[1] = state[1]-1 
        state = list_to_tuple(state) 
    # pygame.display.flip()
    
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_diag_up_right(state, row, col):
    original_state = state
    
    if col + 1 < width and row - 1 > 0:
        state = tuple_to_list(state)
        state[0] = state[0]-1
        state[1] = state[1]+1
        state = list_to_tuple(state)
    # pygame.display.flip()
    
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_diag_down_left(state, row, col):
    original_state = state

    if row + 1 < height and col - 1 > 0:
        state = tuple_to_list(state)
        state[0] = state[0]+1
        state[1] = state[1]-1
        state = list_to_tuple(state)
    pygame.display.flip()
    
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state

def move_diag_down_right(state, row, col):
    original_state = state

    if row + 1 < height and col + 1 < width:
        state = tuple_to_list(state)
        state[0] = state[0]+1
        state[1] = state[1]+1
        state = list_to_tuple(state)
    pygame.display.flip()
    
    new_color = surface.get_at((state[1], state[0]))

    if new_color[:3] == obstacle_color:
        state = original_state
    return state



# this possible moves function will call the move functions and return the updated tuples
def possibleMoves(state, row, col):

    new_posA = move_left(state, row, col)
    new_posB = move_right(state, row, col)
    new_posC = move_up(state, row, col)
    new_posD = move_down(state, row, col)

    new_posE = move_diag_up_left(state, row, col)
    new_posF = move_diag_up_right(state, row, col)
    new_posG = move_diag_down_left(state, row, col)
    new_posH = move_diag_down_right(state, row, col)

    return new_posA, new_posB, new_posC, new_posD, new_posE, new_posF, new_posG, new_posH


closedList = []

parents = {}

children = {}

child_to_parent = {}
child_to_parent_index = {}

# in this function the updated states are compared to the closed list for confirmed movement
# if the attempted move is the same as the current position of in the closed list then the position is not updated
def getPossibleMoves(new_node_x, row, col, counter):

    node_a, node_b, node_c, node_d, node_e, node_f, node_g, node_h = possibleMoves(new_node_x, row, col)
    
    # num_moves = 0
    parents[counter] = new_node_x

    # check if new nodes are in closed list, if not, append to open list
    if node_a not in closedList and node_a not in openList and node_a != new_node_x:
        openList.append(node_a)
        child_to_parent[node_a] = new_node_x # child to parent dictionary is updated with the new position and the position before it (the parent)
        child_to_parent_index[node_a] = counter
         

    if node_b not in closedList and node_b not in openList and node_b != new_node_x:
        openList.append(node_b)
        child_to_parent[node_b] = new_node_x 
        child_to_parent_index[node_b] = counter


    if node_c not in closedList and node_c not in openList and node_c != new_node_x:
        openList.append(node_c)
        child_to_parent[node_c] = new_node_x
        child_to_parent_index[node_c] = counter

 
    if node_d not in closedList and node_d not in openList and node_d != new_node_x:
        openList.append(node_d)
        child_to_parent[node_d] = new_node_x
        child_to_parent_index[node_d] = counter



    if node_e not in closedList and node_e not in openList and node_e != new_node_x:
        openList.append(node_e)
        child_to_parent[node_e] = new_node_x
        child_to_parent_index[node_e] = counter
         

    if node_f not in closedList and node_f not in openList and node_f != new_node_x:
        openList.append(node_f)
        child_to_parent[node_f] = new_node_x
        child_to_parent_index[node_f] = counter


    if node_g not in closedList and node_g not in openList and node_g != new_node_x:
        openList.append(node_g)
        child_to_parent[node_g] = new_node_x
        child_to_parent_index[node_g] = counter

 
    if node_h not in closedList and node_h not in openList and node_h != new_node_x:
        openList.append(node_h)
        child_to_parent[node_h] = new_node_x
        child_to_parent_index[node_h] = counter

    return


openList = deque([start_state]) # open list begins with start state to initialize the loop

closedList = set()


counter = 0
end = 0

start_time = time.time()

# this is the main loop
# the first open list state is opped and compared to the goal state
# the check goal value is passed on to evaluate next moves
# if the check goal is equal to the goal state then the loop is broken
while len(openList):

    for i in range(len(openList)):

        check_goal = openList.popleft()

        if check_goal == goal_state:
            parents[(counter)] = check_goal
            end = 1
            print("enddddddd: ", end)
            break

        closedList.add(check_goal) # add looked at node to closed list

        # zero = get_zero_state(check_goal)
        a, b = check_goal[0], check_goal[1] #zero[0][0], zero[0][1]
        print("check_goal before get possible moves: ", check_goal)
        found_end = getPossibleMoves(check_goal, a, b, counter)

        if counter % 20000 == 0:
            print("Iterations: ", i)
            print("Length of openList: ", len(openList))
            print("CLosed List: \n", closedList)

        # closedList.add(check_goal)

        counter += 1

    if end == 1:
        print("SUCCESS \n SUCCESS \n SUCCESS \n SUCCESS")
        # print("CLosed List: \n", closedList)
        
        break
    
pygame.quit()
print("end: ", end)


# the shortest path is discovered using the child to parent dict from before
# the dict is reversed to account for the start of the search beginning at the end of the dict
shortest_path = [goal_state]
current = goal_state

while current != start_state:
    current = child_to_parent[current]
    shortest_path.append(current)

shortest_path.reverse()

print("--- %s seconds ---" % (time.time() - start_time)) # time for full search and shortest path is recorded for analysis



ppmm = 142 / 25.4 # 142 ppi of current display

height = int(ppmm*50)
width = int(ppmm*180)


surface = pygame.display.set_mode((width, height))  # 50mm x 180mm
obstacle_color = (255, 192, 203)
char_color = (255, 80, 100)



# this updates the display to hide the 2mm border geometry color for ease of visual inspection
# characters
# J
J_rect = pygame.draw.rect(surface, char_color, pygame.Rect(128, 50, 32, 100), width=30)
J_arc = pygame.draw.arc(surface, char_color, pygame.Rect(60, 100, 100, 100), start_angle=3.1415, stop_angle=0, width=30)
# S
S_arc = pygame.draw.arc(surface, char_color, pygame.Rect(180, 50, 90, 90), start_angle=0.5, stop_angle=4.71239, width=30)
S_arc_2 = pygame.draw.arc(surface, char_color, pygame.Rect(180, 110, 90, 90), start_angle=-2.64, stop_angle=1.57, width=30)
# 4 432
four_rect = pygame.draw.rect(surface, char_color, pygame.Rect(285, 50, 32, 75), width=30)
four_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(285, 100, 75, 32), width=30)
four_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(335, 50, 32, 150), width=30)
# 4
four_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 50, 32, 75), width=30)
four_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(385, 100, 75, 32), width=30)
four_rect6 = pygame.draw.rect(surface, char_color, pygame.Rect(435, 50, 32, 150), width=30)
# 3
three_rect = pygame.draw.arc(surface, char_color, pygame.Rect(475, 50, 90, 90), start_angle=4.71239, stop_angle=2.35619, width=30)
three_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(505, 108, 40, 32), width=30)
three_rect3 = pygame.draw.arc(surface, char_color, pygame.Rect(475, 110, 90, 90), start_angle=3.92699, stop_angle=1.5708, width=30)
# 2
two_rect = pygame.draw.rect(surface, char_color, pygame.Rect(600, 50, 80, 32), width=30)
two_rect2 = pygame.draw.rect(surface, char_color, pygame.Rect(660, 50, 32, 92), width=30)
two_rect3 = pygame.draw.rect(surface, char_color, pygame.Rect(635, 110, 32, 32), width=30)
two_rect4 = pygame.draw.rect(surface, char_color, pygame.Rect(610, 140, 32, 32), width=30)
two_rect5 = pygame.draw.rect(surface, char_color, pygame.Rect(590, 170, 120, 32), width=30)


# this full search loop was used to record the frames of each node explored to later compile into an mp4 video
# this loop displays an animation, but can stall if the search tree is large
# full search
for i in range(len(parents)): # -151000):
    # print(state)
    pygame.init()
    # screen = pygame.display.set_mode((800, 600))

    pygame.draw.circle(surface, color=(25, 0, 255), center=(parents[i][1], parents[i][0]), radius=1)
    # pygame.image.save(surface, f"full_search_images\\full_search_images" + str(i) + ".jpeg")
    
    # pygame.image.save(selectOutput("Select a file to write to:")); Thank you for your answers!

    pygame.display.flip() # if the animation stalls, comment this out and uncomment the pygame.display.flip() below to see the result in full with
                          # shortest path animation

# pygame.display.flip() # if the animation stalls uncomment


# this loop was also used to record the frames for making the video
# this will play an animation of the shortest path
# a better animation has been recorded in the mp4
# shortest path
for i in range(len(shortest_path)):
    # print(state)
    pygame.draw.circle(surface, color=(255, 0, 255), center=(shortest_path[i][1], shortest_path[i][0]), radius=2)
    # pygame.image.save(surface, f"_images\\full_search_images" + str(i) + ".jpeg")
    # pygame.image.save(surface, f"shortest_path__images\\shortest_path_images" + str(i + len(parents)) + ".jpeg")


    pygame.display.flip() 

    
# pygame.display.flip() 
pygame.time.wait(10000)  # Pause for 10 seconds
pygame.quit()