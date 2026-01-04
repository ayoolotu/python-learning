#Importing necessary modules
import turtle
import random
import math

#The used position list ensures that there is no major overlap with the drawings
used_positions = []
#The closest that the used_position coordinates can be to each other, calculated in the too_close() function
min_distance = 150

#Initializes the turtle drawing module and screen
t = turtle.Turtle()
s = turtle.Screen()

#Stores the screen height and screen width
screen_width = s.window_width()
screen_height = s.window_height()

#Creates a randomized hex code
def rand_hex():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    return hex_color

#Calculates whether a new set of coordinates are too close or not based on the Euclidean distance (Pythagorean's Theorem)
def too_close(x, y, used_positions):
    #Checks previous coordinates and compares them to the proposed coordinates before they are used to draw an item
    for (ux, uy) in used_positions:
        if math.dist((x, y), (ux, uy)) < min_distance:
            return True
    return False

#Draws the body of the fish
def draw_body(radius, x, y, angle, color):
    """ Description: Draws the main body of the fish in turtle, 
        along with the eye. Depending on the direction, the eye 
        will be either on the left or the right of the fish. The 
        radius, x, and y position will be used to create the fish 
        body itself, and the x and y position will be adjusted to 
        create the eye.

        Args: 
        radius: int, The random size created for each fish
        x: int, The x position of each fish
        y: int, The y position of each fish
        angle: int, The direction the fish should face
        color: The fill color of the fish

        Returns: Nothing
    """

    #Draws the circle body of the fish
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

    # Eye position based on facing direction
    t.penup()
    t.goto(x, y + radius)
    t.setheading(angle)  # Fish is facing this direction

    # Move forward slightly in the direction of the angle to place the eye
    t.forward(radius * 0.6)
    t.dot(radius * 0.2, "black")

#Draws the tail of the fish
def draw_tail(radius, x, y, angle, color):

    """ Description: Draws the tail of the fish that 
        will be attached to the body. Depending on the 
        direction, the tail will be on an edge of the 
        radius in a certain direction.

        Args: 
        radius: int, The random size created for each fish
        x: int, The x position of each fish
        y: int, The y position of each fish
        angle: int, The direction the fish should face
        color: The fill color of the fish

        Returns: Nothing
    """
    #Sets the color of the tail
    t.penup()
    t.fillcolor(color)
    t.pencolor(color)

    #Moves pen so tail starts on the direct opposite side of the eye
    t.goto(x, y + radius)
    t.setheading(angle - 180)
    t.fd(radius * 0.6)

    #Corrects angle of tail so that it faces properly (E.g. >() ()<)
    t.setheading(angle - 135)

    #Draws the triangle
    t.pendown()
    t.begin_fill()
    for _ in range(3):
        t.forward(radius)
        t.right(120)
    t.end_fill()

#Draws the fish bubbles
def draw_bubbles(radius, x, y, angle):
    """ Description: Draws the bubbles that will 
        come out of the fish's mouth. Depending on 
        the radius, position, and direction of the 
        fish, the bubbles will be created based off 
        that, going up and diagonal in the direction the 
        fish is facing. There will be 3 white bubbles, 
        first bubble closest to the fish will be 
        smallest, and then they will increase gradually.

        Args: 
        radius: int, The random size created for each fish
        x: int, The x position of each fish
        y: int, The y position of each fish
        angle: int, The direction the fish should face

        Returns: Nothing
    """
    t.penup()
    t.fillcolor("white")
    t.pencolor("white")

    t.goto(x, y + radius)

    t.seth(angle)
    t.fd(radius)
    angle = radius + 270
    t.setheading(angle)
    t.fd(5)
    t.seth(angle + 90)
    t.fd(20)

    bx = t.xcor()
    by = t.ycor()

    dx, dy = 0.5 * radius, 0.6 * radius

    # Draw three bubbles
    for size in [radius * 0.08, radius * 0.12, radius * 0.16]:
        t.goto(bx, by)
        t.pendown()
        t.begin_fill()
        t.circle(size)
        t.end_fill()
        t.penup()
        bx += dx
        by += dy

#Uses draw_body, draw_tail, and draw_bubbles to draw a fish
def draw_fish(num_fish, colors, angles, bubbles):

    """ Description: Draws the fish, using the parameters 
        and the 3 above functions (draw_bubbles, draw_tail, draw_body). 
        Creates 3 lists of random sizes, and random x and y positions 
        (ensuring no position is the exact same) for each fish not 
        exceeding 1/5 the size of the window, and then in a for loop 
        in the range of num_fish, call on draw_body, draw_tail, and
        draw_bubbles(if wanted), using the color, direction and 
        the newly created size list. These three functions will 
        be used to create each fish.

        Args: 
        num_fish: int, How many fish the user wants
        colors: string list, The color of each fish
        angles: int list, The directions each fish will face
        bubbles: boolean list, whether or not there should be bubbles for the fish

        Returns: Nothing
    """

    #For loop repeats for however many fish there are
    for i in range(num_fish):
        while True:
            x = random.randint(-screen_width // 2 + 100, screen_width // 2 - 100)
            y = random.randint(-screen_height // 2 + 100, screen_height // 2 - 100)
            if not too_close(x, y, used_positions):
                used_positions.append((x, y))
                break

        # Fish size is proportional to screen dimensions
        radius = random.randint(int(screen_width * 0.02), int(screen_width * 0.05))

        #Calls on draw_body, draw_tail, and draw_bubbles if the user requested it
        draw_body(radius, x, y, angles[i], colors[i])
        draw_tail(radius, x, y, angles[i], colors[i])
        if bubbles[i]:
            draw_bubbles(radius, x, y, angles[i])

#Draws the starfish
def draw_starfish(num_starfish, outlines, fills):
    """ Description: Draws the starfish using the parameters given. 
        Uses a for loop to create each starfish, using the 
        outline color, fill color, and checking the array of 
        previously used positions (from the fish) to make sure 
        there's nothing that is the exact same.

        Args: 
        num_starfish: int, The number of starfish the user wants
        outlines: list, the outline color for each starfish
        fills: list, the fill colors for each starfish

        Returns: Nothing
    """

    for i in range(num_starfish):
        t.penup()
        t.pencolor(outlines[i])
        t.fillcolor(fills[i])
        
        while True:
            x = random.randint(-screen_width//2 + 60, screen_width//2 - 60)
            y = random.randint(-screen_height//2 + 60, 0)
            if not too_close(x, y, used_positions):
                used_positions.append((x, y))
                break

        t.goto(x, y)

        t.pendown()
        t.pensize(3)
        t.begin_fill()
        for i in range(5):
            t.forward(20)
            t.right(120)
            t.forward(20)
            t.right(-48)
        t.end_fill()

#Draws the sea grass
def draw_grass():
    """ Description: Draws grass along the bottom of the 
        aquarium/screen, with its screen_height not exceeding 1/4 
        of the screen_height of the screen.

        Args: None

        Returns: Nothing
    """
    hex = "#00a400"
    t.pencolor(hex)
    
    x = int((screen_width / 2 * -1))
    y = int((screen_height / 2 * - 1))

    while x < screen_width:
        grass_height = random.randint(0, int(y/4 * -1))
        t.penup()
        t.setpos(x+10, y)
        t.pendown()
        t.setheading(90)
        t.pensize(10)
        t.fd(grass_height)
        x += random.randint(10, 20)

    t.penup()  

#Draws the treasure chest
def draw_chest():
    """ Description: Draws the treasure chest, including the 
        rectangle body, the semicircle top, the keyhole, and 
        the keypad (of sorts) that the keyhole is on. Checks 
        the position array to make sure the position does not 
        overlap any of the fish/starfish positions.

        Args: None

        Returns: Nothing
    """
    #Sets colors and coordinates
    fill = "#471b00"
    outline = "#752d00"
    keyhole = "#ffc340"
    chest_height = screen_height/3
    x = random.randint(int(-screen_width/2), int((screen_width/2) - 200))
    y = int((screen_height / 2 * - 1))

    #Sets starting position of the chest
    t.penup()
    t.setpos(x, y)
    t.setheading(90)
    t.pencolor(outline)
    t.fillcolor(fill)
    t.pendown()
    t.pensize(3)
    
    #Draws the rectangular base of the chest
    t.begin_fill()
    for i in range(0, 2):
        t.fd(chest_height/ 3)
        t.right(90)
        t.fd(chest_height * 2 / 3)
        t.right(90)
    t.end_fill()

    #Draws the semicircle lid of the chest
    t.penup()
    t.fd(chest_height/ 3)
    t.left(90)
    t.back(chest_height* 2 / 3)
    #Saving this position to use for the backing of the keyhole
    corner_x = t.xcor()
    corner_y = t.ycor()
    t.right(90)
    t.pendown()
    t.begin_fill()
    t.circle(chest_height/3, 180)
    t.end_fill()

    #Draws the backing of the keyhole
    t.penup()
    t.left(90)
    t.fd(chest_height*5/12)
    t.right(90)
    t.pendown()
    t.fillcolor(outline)
    t.begin_fill()
    for i in range(4):
        t.fd(chest_height/6)
        t.right(90)
    t.end_fill()

    #Draws the keyhole
    t.penup()
    t.pencolor(keyhole)
    t.fillcolor(keyhole)
    t.fd(chest_height/18)
    t.right(90)
    t.fd((chest_height/12)-6)
    t.setheading(90)
    t.pendown()
    t.begin_fill()
    t.circle(6)
    t.end_fill()

    t.penup()
    t.left(90)
    t.fd(6)
    t.setheading(315)
    t.right(75)
    t.pendown()
    t.begin_fill()
    for i in range(3):
        t.fd(16)
        t.left(120)
    t.end_fill()


if __name__ == "__main__":
    fish_colors = []
    fish_directions = []
    fish_bubbles = []
    starfish_outlines = []
    starfish_colors = []
    
    num_fish = 4
    num_starfish = 4
    if_r = "r"

    
    #Asks user for the number of fish they want, and if it is less than 1 or more than 5, a random number is selected
    num_fish = int(input("How many fish would you like to be drawn? (Input a number between 1 and 5)"))
    if num_fish < 1 or num_fish > 5:
        num_fish = random.randint(1,5)

    
    #The number of fish is used to iterate through the fish_colors, fish_directions and fish_bubbles lists so that each fish will have colors and bubbles(if wanted), and a direction
    for i in range(num_fish):
        yes_or_no = {
            "yes": True,
            "no": False
        }
        
        color = input(f"Fish #{i + 1}:\nEnter a color name or hex code for the fish, or type R for random: ")
        if if_r.lower() == 'r':
            color = rand_hex()
        angler = input(f"Enter a number between 0 and 360 to determine the direction of your fish, or press r for a random number: ")
        angle = 0
        try:
            if int(angler) < 0 or int(angler) > 360:
                angle = random.randint(0, 360)
            if int(angler) >= 0 and int(angler) <= 360:
                angle = int(angler)
        except:
            angle = random.randint(0, 360)

        bubbles = input("Would you like the fish to have bubbles? (Type yes or no): ")
        bubble_bool = False
        if bubbles.lower() not in list(yes_or_no.keys()):
            bubble_bool = yes_or_no.get(random.choice(list(yes_or_no.keys())))
        else:
            bubble_bool = yes_or_no.get(bubbles.lower())
          
        fish_colors.append(color)
        fish_directions.append(angle)
        fish_bubbles.append(bubble_bool)

    #The process for fish is repeated for starfish, but it needs outline and fill color instad of direction and bubbles
    num_starfish = int(input("How many starfish would you like to be drawn? (Input a number between 1 and 3)"))
    if num_starfish < 1 or num_starfish > 3:
        num_starfish = random.randint(1,3)
    
    for i in range(num_starfish):
        outline = input(f"Starfish #{i + 1}:\nEnter a color name or hex code for the OUTLINE of the starfish, or type R for a randomized color: ")
        fill = input("Enter a color name or hex code for the FILL COLOR of the starfish, or type R for a randomized color: ")
        if outline == 'r':
            outline = rand_hex()
        if fill == 'r':
            fill = rand_hex()
        starfish_colors.append(fill)
        starfish_outlines.append(outline)
    

    #Sets the screen's background color
    s = turtle.Screen()
    s.bgcolor("#2374a7")
    
    #Sets the speed of the pen to be the fastest possible speed, and draws all the parts of the code based on user input
    t.speed(0)
    draw_grass()
    draw_chest()
    draw_fish(num_fish, fish_colors, fish_directions, fish_bubbles)
    draw_starfish(num_starfish, starfish_outlines, starfish_colors)
    
    #Keeps turtle window open until manually closed by user
    t.hideturtle()
    turtle.done()
