import turtle
from time import sleep as wait
from random import randint as randi
from random import random as randf
import sys
import os
import json

TREES_FOLDER_NAME = "trees"
if not os.path.exists(TREES_FOLDER_NAME): os.mkdir(TREES_FOLDER_NAME)

### HOW THE SCRIPT WORKS:
# A fractal tree is a shape you can build by following an algorithm:
# 1. you draw a line: the first branch with a given length (STARTING_LENGTH) and a STARTING_ANGLE
# 2. you save the CURRENT_ANGLE, then you rotate by a certain angle (LEFT_ANGLE) to the left
#    relatively to your previous heading and you draw a new line,
#    this time with a length decreased by a certain amount (LENGTH_MULTIPLIER)
#    you save your current position after drawing the branch
# 3. you go back to the node where you started drawing the last branch,
#    set your heading to the CURRENT_ANGLE again, then and
#    rotate by a certain angle (RIGHT_ANGLE) to the right
#    you save your current position after drawing the branch
# 4. repeat the algorithm, each time drawing a left and a right branch
#    for all the positions you ended up at and saved in the previous branch generation
#############################################################################################

### RUN ARGUMENTS:
# nothing runs with the set parameters
# -r randomize starting parameters
# -l [tree_name] loads the tree parameters from "tree_name.txt"
# -s [tree_name] saves the current tree parameters to "tree_name.txt", then exits the program
num_args = len(sys.argv)
if num_args != 1 and num_args != 2 and num_args != 3:
    print("Invalid arguments")
    exit()

### TREE PARAMETERS
LEFT_ANGLE = 10 # THE BENDING ANGLE IN DEGREES OF EACH LEFT BREANCH RELATIVELY TO THE PREVIOUS ONE
RIGHT_ANGLE = 60 # THE BENDING ANGLE IN DEGREES OF EACH RIGHT BREANCH RELATIVELY TO THE PREVIOUS ONE
LENGTH_MULTIPLIER = 0.7 # THE LENGTH RATIO BETWEEN THE NEXT GENERATION OF BRANCHES AND THE CURRENT ONE
STARTING_LENGTH = 180 # THE LENGTH OF THE FIRST BRANCH
STARTING_ANGLE = 10 # THE ANGLE OF THE FIRST BRANCH RELATIVELY TO THE NORTH (positive goes to the left, negative goes to the right)
STARTING_WIDTH = 15 # THE WIDTH OF THE FIRST BRANCH
ENDING_WIDTH = 1 # THE WIDTH OF THE FINAL GENERATION OF BRANCHES
NUM_GENERATIONS = 10 # THE NUMBER OF BRANCH GENERATIONS (the first branch is always drawn and counts as generation 0)
ANIMATE = True # animates the tree drawing process if set to True, draws the tree instantly if set to False
BACKGROUND_COLOR = (1, 1, 0.9) # the name is pretty self explainatory
# fractal tree color gradient
STARTING_COLOR = (0.25, 0.15, 0.0)
ENDING_COLOR = (0.0, 0.8, 0.0)

### "HIDDEN LOGIC"
# If you intend to only play with the tree parameters
# you shouldn't change anything past this line in the script.
# If your goal is to edit the script itself of course you're welcome to do it.
# A couple ideas it could be fun to play with:
# 1. Every branch generates N branches where N is a variable (beware the number of recusive calls and iterations could skyrocket)
# 2. Every branch generates a random amount of branches (beware the number of recusive calls and iterations could skyrocket)
# 3. Live parameter editing to avoid having to rerun the script every time

# rounding for file writing
BACKGROUND_COLOR = (
    round(BACKGROUND_COLOR[0], ndigits=2),
    round(BACKGROUND_COLOR[1], ndigits=2),
    round(BACKGROUND_COLOR[2], ndigits=2)
)

STARTING_COLOR = (
    round(STARTING_COLOR[0], ndigits=2),
    round(STARTING_COLOR[1], ndigits=2),
    round(STARTING_COLOR[2], ndigits=2)
)

ENDING_COLOR = (
    round(ENDING_COLOR[0], ndigits=2),
    round(ENDING_COLOR[1], ndigits=2),
    round(ENDING_COLOR[2], ndigits=2)
)

# randomized
if num_args == 2 and sys.argv[1] == "-r":
    LEFT_ANGLE = randf() * 360
    RIGHT_ANGLE = randf() * 360
    LEFT_ANGLE = randf() * 60
    RIGHT_ANGLE = randf() * 60
    LENGTH_MULTIPLIER = 0.25 + randf()
    STARTING_LENGTH = randi(100, 200)
    STARTING_ANGLE = randi(-30, 30)
    STARTING_WIDTH = 0.1 + (randf() * 15)
    NUM_GENERATIONS = randi(5, 10)

# load option
if num_args == 3 and sys.argv[1] == "-l":
    path = TREES_FOLDER_NAME + "/" + sys.argv[2] + ".json"
    try:
        with open(path, "r") as f:
            lines = f.readlines()
            json_content = "".join(lines)
            fractal_tree_data = dict(json.loads(json_content))
            
            LEFT_ANGLE = fractal_tree_data["left_angle"]
            RIGHT_ANGLE = fractal_tree_data["right_angle"]
            LENGTH_MULTIPLIER = fractal_tree_data["length_multiplier"]
            STARTING_LENGTH = fractal_tree_data["starting_length"]
            STARTING_ANGLE = fractal_tree_data["starting_angle"]
            STARTING_WIDTH = fractal_tree_data["starting_width"]
            ENDING_WIDTH = fractal_tree_data["ending_width"]
            NUM_GENERATIONS = fractal_tree_data["generations_number"]
            BACKGROUND_COLOR = fractal_tree_data["background_color"]
            STARTING_COLOR = fractal_tree_data["starting_tree_color"]
            ENDING_COLOR = fractal_tree_data["ending_tree_color"]
        print("Successfully loaded the tree parameters!")
    except:
        print("Failed to load the tree parameters!")
        exit()

# save option
if num_args == 3 and sys.argv[1] == "-s":
    path = TREES_FOLDER_NAME + "/" + sys.argv[2] + ".json"
    if is.path.exists(path) and input(f"The file at the given path (\"{path}\") already exists, do you want to replace the existing file? [ENTER/n]: ").strip() == "n":
        exit()
    try:
        with open(path, "w") as f:
            fractal_tree_data = dict()
            fractal_tree_data["left_angle"] = LEFT_ANGLE
            fractal_tree_data["right_angle"] = RIGHT_ANGLE
            fractal_tree_data["length_multiplier"] = LENGTH_MULTIPLIER
            fractal_tree_data["starting_length"] = STARTING_LENGTH
            fractal_tree_data["starting_angle"] = STARTING_ANGLE
            fractal_tree_data["starting_width"] = STARTING_WIDTH
            fractal_tree_data["ending_width"] = ENDING_WIDTH
            fractal_tree_data["generations_number"] = NUM_GENERATIONS
            fractal_tree_data["background_color"] = BACKGROUND_COLOR
            fractal_tree_data["starting_tree_color"] = STARTING_COLOR
            fractal_tree_data["ending_tree_color"] = ENDING_COLOR
            f.write(json.dumps(fractal_tree_data, indent=4))
        print("Successfully saved the current tree parameters!")
    except:
        print("Failed to save the current parameters!")
        exit()
    exit()

# window width and height
WIDTH, HEIGHT = 800, 800

# turtle moving function (changes the turtle position without drawing the line)
def move_turtle(position:tuple[int, int]):
    turtle.penup()
    turtle.goto(position)
    turtle.pendown()

# calculate gradient deltas
if NUM_GENERATIONS > 0:
    # used to make the branches greener as we get to the end of the tree
    current_color = [STARTING_COLOR[0], STARTING_COLOR[1], STARTING_COLOR[2]]
    red_delta = (ENDING_COLOR[0] - STARTING_COLOR[0]) / NUM_GENERATIONS
    green_delta = (ENDING_COLOR[1] - STARTING_COLOR[1]) / NUM_GENERATIONS
    blue_delta = (ENDING_COLOR[2] - STARTING_COLOR[2]) / NUM_GENERATIONS

    # used to make the branches thiner as we get to the end of the tree
    current_width = STARTING_WIDTH
    width_delta = (STARTING_WIDTH - ENDING_WIDTH) / NUM_GENERATIONS

# recursion is for branch layer generation
# for loop iteration is for drawing all the branches in the same generation
generations = 0
def draw_fractal_tree(starting_positions:list[tuple[int, int, int]]):
    global generations, current_color, current_width
    
    # stop if the NUM_GENERATIONS limit is reached (the first branch counts as generation zero)
    if generations >= NUM_GENERATIONS: return
    generations += 1

    # evaluate what the current generation branch length is (exponential by generations)
    current_length = STARTING_LENGTH * LENGTH_MULTIPLIER ** (generations)

    # make the color greener
    current_color = [min(1, current_color[0] + red_delta), min(1, current_color[1] + green_delta), min(1, current_color[2] + blue_delta)]
    turtle.color(current_color[0], current_color[1], current_color[2])

    # shrink the branch width
    if generations == 0: current_width -= width_delta
    current_width = max(0.1, current_width - width_delta)
    turtle.pensize(current_width)
    
    # this will contain the starting node position and heading for the next branch generation
    next_starting_positions = []

    # draw all the pairs of branches in the generation in a left to right order
    for pos in starting_positions:
        # draw the left branch
        move_turtle(pos[0]) # move to the starting position for this pair of branches
        turtle.setheading(pos[1]) # set the heading to the previous branch angle
        turtle.left(LEFT_ANGLE) # turn left by the LEFT_ANGLE
        turtle.forward(current_length) # draw the branch
        next_starting_positions.append((turtle.pos(), turtle.heading())) # add this node position to the next ones
        # draw the right branch
        move_turtle(pos[0]) # move to the starting position for this pair of branches
        turtle.setheading(pos[1]) # set the heading to the previous branch angle
        turtle.right(RIGHT_ANGLE) # turn right by the RIGHT_ANGLE
        turtle.forward(current_length) # draw the branch
        next_starting_positions.append((turtle.pos(), turtle.heading())) # add this node position to the next ones

    # by refreshing the screen only at the end of each generation draw call,
    # we'll see the branches from the same generation all popping up at the same time)
    if ANIMATE:
        turtle.update()
        wait(0.05)
    draw_fractal_tree(next_starting_positions)

# set window width and height
turtle.title("Fractal Trees!")
turtle.setup(WIDTH, HEIGHT)

# turtle setup
turtle.hideturtle()
if ANIMATE:
    turtle.speed("slowest")
else:
    turtle.speed("fastest")
turtle.tracer(0) # disables the automatic screen refresh
turtle.bgcolor(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
turtle.pensize(STARTING_WIDTH)
turtle.color(STARTING_COLOR[0], STARTING_COLOR[1], STARTING_COLOR[2])

# go to bottom center
move_turtle((0, -(HEIGHT / 2) + 60))

# draw the first branch
turtle.setheading(90 + STARTING_ANGLE)
turtle.forward(STARTING_LENGTH)
if ANIMATE: turtle.update()
# start recursion
draw_fractal_tree([(turtle.pos(), turtle.heading())])

# if the tree drawing process is not animated,
# then refresh the screen only at the end to make the tree appear all at once
if not ANIMATE: turtle.update()

# press the ESCAPE key to exit once the tree is drawn
turtle.onkeypress(exit, "Escape")
turtle.listen()
turtle.mainloop()
