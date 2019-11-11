# Problem
# The rule of the game are as follows :
# We draw a graph connecting nodes in one direction. The arcs are one direction and clockwise.
# If one node has connected to another node, that other node cannot connect back to it.
# We can only have odd number of nodes in the graph
# We can only skip max_skips number of nodes where max_skips = ((number_of_nodes - 1) modulo 2) - 1
# So for 5 nodes we can skip at most 1 node
# For 7 nodes we can at most 2 nodes
# For 9 nodes we can skip at most 3 nodes
# We draw an arc from one node to the next by skipping either 1,2, or 3 nodes
# At the start we start at any node.
# We start by skipping

import string  # For letters of the alphabet that will label the nodes
import turtle
import tkinter


# This function returns the letters of the alphabet as labels for the nodes. It takes the number of nodes and returns
# the corresponding list
def get_matrix_header_letters(number_of_nodes):
    if number_of_nodes <= 26:
        alphabet = list(string.ascii_lowercase.upper())
    else:
        alphabet = []
        for i in range(1,number_of_nodes + 1):
          alphabet.append(str(i))
    return alphabet[0:number_of_nodes]


# This function prints the matrix generated by joining the nodes base on the rules
# The matrix initially has all zeros in every entries
def print_array(matrix):
    # print empty line
    print("")

    l = matrix  # we use l so we dont type too much

    # The number of entries on any line of the matrix gives us the number of nodes. It is a square matrix anyway
    number_of_nodes = len(l)

    # print header
    headers = get_matrix_header_letters(number_of_nodes)
    for i in range(0, number_of_nodes):
        print("\t", headers[i], sep="", end="")

    # print empty line
    print("")

    # print an underline for the header
    for i in range(0, number_of_nodes):
        print("\t-", sep="", end="")

    # print another empty line
    print("")

    # Below we are printing the content of the matrix
    i = -1  # intialise a counter i
    for sub_list in l:
        i = i + 1
        print("\n", headers[i], "|\t", end="")
        for data in sub_list:
            print(data, "|\t", end="")
        # print empty line
        print("")


# This function returns a matrix with all zeros int the entries
def get_empty_matrix(number_of_nodes):
    l = []
    n = number_of_nodes
    # We need a n by n matrix
    for i in range(0, n):
        l.append([])
        for j in range(0, n):
            l[i].append(0)
    return l


# This function tells us what is the next node for every skips
def get_next_node(current_node, skips, number_of_nodes):
    # current_node is the node we are on
    # next node is the next node we will be
    # number_of_nodes is the number of nodes for our matrix
    return (current_node + skips + 1) % number_of_nodes


# This function fills the matrix respecting the rules of the games
def run(matrix, couples_array):
    # We need to fill in the matrix with respect to the rules of the game
    number_of_nodes = len(matrix)  # so we go from 0 to n-1
    l = matrix
    n = number_of_nodes
    max_skips = ((n - (
            n % 2)) // 2) - 1  # For 5 nodes we can skip 1 node, but it means we are adding 2 to ever current node
    print("max skips",max_skips)
    current_node = 0
    for i in range(1, max_skips+1):  # we will keep increasing the number of skips till we get to the maximum allowed
        skips = i
        start = current_node
        next_node = get_next_node(current_node, skips, number_of_nodes)
        while start != next_node:
            l[current_node][next_node] = 1
            draw_arc_from_origin_to_dest(current_node,next_node,couples_array)
            current_node = next_node
            next_node = get_next_node(current_node, skips, number_of_nodes)
        l[current_node][next_node] = 1
        draw_arc_from_origin_to_dest(current_node,next_node,couples_array)
        current_node = next_node # we go back at the beginning

    for i in range(0, number_of_nodes):
        next_node = get_next_node(i, 0, number_of_nodes)
        l[i][next_node] = 1
        draw_arc_from_origin_to_dest(i, next_node, couples_array)

    for i in range(0,number_of_nodes):
        for j in range(0,number_of_nodes):
            if l[i][j] == 0 and l[j][i] == 0 and i != j: # we missed these two draw_nodes and they are different
                l[i][j] = 1
                draw_arc_from_origin_to_dest(i,j,couples_array)



def get_style_for_writing():
    style = ('Times Rew Romans', 15, 'bold')
    return style


def get_config_data():
    couple = turtle.screensize()
    multiplier = 3 / 2
    screen_length = int(couple[0] * multiplier)
    screen_width = couple[1] * multiplier
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270
    DEGREES_CIRCLE = 360
    RADIUS = (min(screen_length, screen_width) // 2)
    return EAST, NORTH, WEST, SOUTH, DEGREES_CIRCLE, RADIUS


def draw_nodes(number_of_nodes):
    # Now we will draw the graph
    # We want a big screen so we set the screen size as big as possible
    turtle.penup()  # We pick up the pen
    node_labels = get_matrix_header_letters(number_of_nodes)
    couple = turtle.screensize()
    multiplier = 3 / 2
    screen_length = int(couple[0] * multiplier)
    screen_width = couple[1] * multiplier
    EAST, NORTH, WEST, SOUTH, DEGREES_CIRCLE, RADIUS = get_config_data()

    # screen_length, screen_width = turtle.screensize()
    turtle.screensize(screen_length, screen_width)  # We set the screen size
    # now we save the x and y coordinate of where we are
    x_origin = turtle.xcor()
    y_origin = turtle.ycor()

    couples_array = []  # This array will store the different coordinates of where we have our nodes

    angle_division = int(DEGREES_CIRCLE // number_of_nodes)
    angle_to_turn = angle_division
    direction = NORTH
    print("angle_division = ",angle_division)
    # Let's draw the first label
    small_step = 55
    turtle.setheading(NORTH)
    turtle.penup()
    turtle.forward(RADIUS)
    # save this coordinate
    couples_array.append([turtle.xcor(), turtle.ycor()])
   
    # move forward a bit more
    turtle.forward(small_step)
    style = get_style_for_writing()
    turtle.pendown()
    # Now we write the node labels
    turtle.write(str(node_labels[0]), font=style, align='center')
    turtle.penup()  # pull the penup
    turtle.goto(x_origin, y_origin)  # go to origin
    turtle.setheading(NORTH)  # Face north
    small_step = 65
    # Now we draw the remaining labels
    for i in range(1, number_of_nodes):
        turtle.right(angle_to_turn)
        turtle.penup()
        turtle.forward(RADIUS)
        # save this coordinate
        couples_array.append([turtle.xcor(), turtle.ycor()])
        n = number_of_nodes
        if float(i) >= 0.3 * n and float(i) <= 0.55 * n:
            small_step * 1.5
        # move forward a bit more
        turtle.forward(small_step)
        style = get_style_for_writing()
        turtle.pendown()
        # Now we write the node labels
        turtle.write(str(node_labels[i]), font=style, align='center')
        turtle.penup()  # pull the penup
        turtle.goto(x_origin, y_origin)  # go to origin
        turtle.setheading(NORTH)
        angle_to_turn += angle_division
    return couples_array


# This function draws an arc from an (x_start, y_start) coordinate to (x_end, y_end) coordinate
def draw_arcs(x_start, y_start, x_end, y_end):
    couple = turtle.screensize()
    multiplier = 3 / 2
    screen_length = int(couple[0] * multiplier)
    screen_width = couple[1] * multiplier
    EAST, NORTH, WEST, SOUTH, DEGREES_CIRCLE, RADIUS = get_config_data()
    turtle.penup()  # We pull the pen up
    turtle.hideturtle()
    turtle.goto(x_start, y_start)
    turtle.showturtle()
    turtle.pendown()
    turtle.goto(x_end, y_end)
    heading = turtle.heading()
    #print("current heading : ",turtle.heading())
    turtle.shape("turtle")
    turtle.setheading(heading)
    turtle.stamp()
    turtle.penup()



def draw_arc_from_origin_to_dest(current_node,next_node,couples_array):
    i = current_node
    j = next_node
    x_start = couples_array[i][0]
    y_start = couples_array[i][1]
    x_end = couples_array[j][0]
    y_end = couples_array[j][1]

    #turtle.showturtle()
    draw_arcs(x_start, y_start, x_end, y_end)
    #turtle.hideturtle()

def main():
    #turtle.hideturtle()#We hide the turtle/little thing drawing
    number_of_nodes = 999 # anything above 26 nodes will cause an error
    turtle.speed(9)# 1 is the slowest, 10 is faster, and 0 is the fastest
    n = number_of_nodes
    # We need a n by n matrix
    empty_matrix = get_empty_matrix(n)
    couples_array = draw_nodes(number_of_nodes)
    run(empty_matrix, couples_array)
    matrix = empty_matrix  # Matrix is not empty anymore
    print_array(matrix)
    tkinter.mainloop()  # to prevent turtle from closing


main()
