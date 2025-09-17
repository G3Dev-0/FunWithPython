import turtle
from time import sleep as wait

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

### TREE PARAMETERS
LEFT_ANGLE = 24 # THE BENDING ANGLE IN DEGREES OF EACH LEFT BREANCH RELATIVELY TO THE PREVIOUS ONE
RIGHT_ANGLE = 60 # THE BENDING ANGLE IN DEGREES OF EACH RIGHT BREANCH RELATIVELY TO THE PREVIOUS ONE
LENGTH_MULTIPLIER = 1 / 2 # THE LENGTH RATIO BETWEEN THE NEXT GENERATION OF BRANCHES AND THE CURRENT ONE
STARTING_LENGTH = 300 # THE LENGTH OF THE FIRST BRANCH
STARTING_ANGLE = -10 # THE ANGLE OF THE FIRST BRANCH RELATIVELY TO THE NORTH (positive goes to the left, negative goes to the right)
STARTING_WIDTH = 10 # THE WIDTH OF THE FIRST BRANCH (it will fade to 1 generation by generation)
MAX_GENERATIONS = 10 # THE NUMBER OF BRANCH GENERATIONS (the first branch is always drawn and counts as generation 0)
ANIMATE = True # animates the tree drawing process if set to True, draws the tree instantly if set to False

def move_turtle(position:tuple[int, int]):
    turtle.penup()
    turtle.goto(position)
    turtle.pendown()

if MAX_GENERATIONS > 0:
    # used to make the branches greener as we get to the end of the tree
    current_color = [0.2, 0.1, 0.0]
    green_delta = (1 - current_color[1]) / MAX_GENERATIONS

    # used to make the branches thiner as we get to the end of the tree
    current_width = STARTING_WIDTH
    width_delta = (current_width - 0.1) / MAX_GENERATIONS

# recursion for generation
# for loop iteration is for drawing all the branches in the same generation
generations = 0
def draw_fractal_tree(starting_positions:list[tuple[int, int, int]]):
    global generations, current_color, current_width
    
    # stop if the MAX_GENERATIONS limit is reached (the first branch counts as generation zero)
    if generations >= MAX_GENERATIONS: return
    generations += 1

    # evaluate what the current generation branch length is (exponential by generations)
    current_length = STARTING_LENGTH * LENGTH_MULTIPLIER ** (generations)

    # make the color greener
    current_color = [current_color[0], min(1, current_color[1] + green_delta), current_color[2]]
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
WIDTH, HEIGHT = 800, 600
turtle.setup(WIDTH, HEIGHT)

# turtle setup
turtle.hideturtle()
if ANIMATE:
    turtle.speed("slowest")
else:
    turtle.speed("fastest")
turtle.tracer(0) # disables the automatic screen refresh
turtle.bgcolor(0.1, 0.1, 0.2)
turtle.pensize(STARTING_WIDTH)
turtle.color("brown")

# go to bottom center
move_turtle((0, -HEIGHT / 2))

# draw the first branch
turtle.setheading(90 + STARTING_ANGLE)
turtle.forward(STARTING_LENGTH)
if ANIMATE: turtle.update()
# start recursion
draw_fractal_tree([(turtle.pos(), turtle.heading())])

if not ANIMATE: turtle.update()

# press the ESCAPE key to exit once the tree is drawn
turtle.onkeypress(exit, "Escape")
turtle.listen()
turtle.mainloop()